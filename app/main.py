from fastapi import FastAPI
from app.models import TranscriptRequest, SummaryResponse
from app.summarizer import Summarizer
from app.config import settings
import logging
import re
import nltk
from nltk.corpus import words

# ensure the words corpus is downloaded
nltk.download('words', quiet=True)

# create a set of English words in lowercase
english_words = set(word.lower() for word in words.words())

# set the logger level
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# app initialisation
app = FastAPI(
    title="Chat Transcript Summarizer",
    description="A microservice to summarize customer-agent conversations using Groq API",
    version="1.0.0"
)

# create summarizer object 
summarizer = Summarizer(api_key=settings.groq_api_key)

# function to check the junkness in transcript, if found then exit with right response 
def is_junk_transcript(transcript: str) -> bool:
    
    cleaned_transcript = transcript.strip()
    
    # check alphabetic ratio (threshold 30%)
    alphabetic_chars = sum(c.isalpha() for c in cleaned_transcript)
    total_chars = len(cleaned_transcript)
    if total_chars > 0 and (alphabetic_chars / total_chars) < 0.3:
        return True
    
    # check junk patterns
    junk_patterns = [
        r"^[0-9\s\W]+$", 
        r"^[a-zA-Z]{1,3}[\W\s]*$", 
        r"^[\W\s]+$", 
        r"(.)\1{4,}"
    ]
    for pattern in junk_patterns:
        if re.match(pattern, cleaned_transcript):
            return True
    
    # extract alphabetic words
    words = re.findall(r'\b[a-zA-Z]+\b', cleaned_transcript)
    
    if not words:
        return True 
    
    # check if words are in English vocabulary
    lowercase_words = [word.lower() for word in words]
    non_english_count = sum(1 for word in lowercase_words if word not in english_words)
    total_words = len(words)
    
    # more than 50% not in English vocabulary
    if total_words > 0 and (non_english_count / total_words) > 0.5:
        return True  
    
    return False

# function to get the input, check intent and if intent is ok, then call the summarizer()
@app.post("/summarize", response_model=SummaryResponse)
async def summarize_transcript(request: TranscriptRequest) -> SummaryResponse:
    transcript = request.transcript.strip()

    # check 1: input length
    if len(transcript) < 10:
        logger.warning("Transcript too short")
        return SummaryResponse(error="Transcript is too short or invalid for summarization.")

    # check 2:  for junk characters or lack of meaningful content
    if is_junk_transcript(transcript):
        logger.warning(f"Junk transcript detected: {transcript}")
        return SummaryResponse(error="Transcript contains too many invalid characters or lacks meaningful content.")

    # check 3:  if it's a summarization task using Groq AI inference 
    if not summarizer.is_summarization_task(transcript):
        logger.warning(f"Non-summarization attempt detected: {transcript}")
        return SummaryResponse(error="This endpoint is restricted to transcript summarization tasks only.")

    # generate summary
    summary, error = summarizer.summarize(transcript)
    if error:
        logger.error(f"Summarization failed: {error}")
        return SummaryResponse(error=error)

    logger.info("Successfully summarized transcript")
    return SummaryResponse(summary=summary)
