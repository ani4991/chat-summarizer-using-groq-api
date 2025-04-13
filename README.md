# Chat Transcript Summarizer

A FastAPI-based microservice to summarize customer-agent conversation transcripts using the Groq API.

## Setup

1. **Clone the repository** from github link (or create the project structure manually).
2. **move to project directory**, in current terminal execute docker-compose up --build
3. **go to  http://localhost:8000/docs** in browser (postman page)
4. **start giving transcript inputs**, 

## Important notes:

1. As the question started with this line  - "Accept customer-agent conversation transcripts". 
I have assumed that the input json will have the keyword "transcript", this format is enforced using pydantic settings (refer to models.py file). So the input should be of the format:
{
    "transcript:""
}

2. In summarizer.py file, inside the summarize() function (line 47), I have kept 2 models in use,
one is model="meta-llama/llama-4-maverick-17b-128e-instruct" (currently in use) and other is # model = "llama-3.3-70b-versatile" (commented out), if you face any model error (not found or removed from groq api's mode list, then kindly try using the commentd one please)

3. In def summarize() function (summarizer.py file), line 65, I have set the temperature value to 0.3 so that it remains little focused for the summary task. More tuning can be done here.

4. I have written few test cases (test_summarizer.py file), which can be executed through **docker-compose exec summarizer pytest tests/**

## docker hub:
1. link - https://hub.docker.com/r/dockani4991/chat-summarizer-summarizer/tags (docker pull dockani4991/chat-summarizer-summarizer:latest)
