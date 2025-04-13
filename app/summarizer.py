from groq import Groq
from typing import Tuple, Optional

# initialise and get the api_key
class Summarizer:
    def __init__(self, api_key: str):
        self.client = Groq(api_key=api_key)

    # check intent of the transcript
    def is_summarization_task(self, transcript: str) -> bool:

        # through system prompt, we set the tone of the task
        try:
            system_prompt = (
                "You are an intent classification assistant.\n"
                "You must respond with only one word: True or False.\n"
                "Do NOT include punctuation, explanation, or any additional words.\n"
                "If a user provides a conversation transcript without asking anything else, assume they want it summarized.\n"
                "Examples:\n"
                "- 'Agent: Hi\nCustomer: I need help with an order.' → True\n"
                "- 'Translate this.' → False\n"
                "Again, reply strictly with True or False only."
            )

            user_prompt = f"{transcript.strip()}"

            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                # model = "llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0,
                max_tokens=5,
            )

            result = response.choices[0].message.content.strip().lower()
            # robust normalization in case the model returns multiple outputs
            return result in ["true", "true.", "true\n"]

        except Exception as e:
            return False


    # generate summary of the transcript
    def summarize(self, transcript: str) -> Tuple[Optional[str], Optional[str]]:
        try:
            # making sure to guide the model
            system_prompt = (
                "You are a summarization assistant. Your only task is to provide a concise summary of the "
                "customer-agent conversation transcript provided with a reply constraint of less than or equal to 100 words only. "
                "Do not perform any other tasks."
            )
            
            # getting the desired summary
            user_prompt = f"Summarize the following conversation:\n\n{transcript}\n\nSummary:"

            response = self.client.chat.completions.create(
                model="meta-llama/llama-4-maverick-17b-128e-instruct",
                # model = "llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.3,
                max_tokens=100
            )
            summary = response.choices[0].message.content.strip()
            return summary, None
        except Exception as e:
            return None, f"Failed to summarize transcript: {str(e)}"
