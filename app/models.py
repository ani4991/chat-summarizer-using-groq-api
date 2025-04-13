from pydantic import BaseModel, Field

# setting the format for input transcript
class TranscriptRequest(BaseModel):
    transcript: str = Field(..., description="The customer-agent conversation transcript to summarize")

# setting the output response format
class SummaryResponse(BaseModel):
    summary: str | None = Field(default=None, description="The summary of the conversation")
    error: str | None = Field(default=None, description="Error message if summarization fails")