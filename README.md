# Chat Transcript Summarizer

A FastAPI-based microservice to summarize customer-agent conversation transcripts using the Groq API.

## Setup

1. **Clone the repository** from github link (or create the project structure manually).
2. **move to project directory**, now create an empty file called ".env" and execute the command "cp env.example .env"
3. **verify the docker versions** in your system for compatibility
4. in current terminal execute **docker-compose up --build**
5. also test cases can be run in another terminal, going to same directory and executing this command - "docker-compose exec summarizer pytest tests/"
6.  **go to  http://localhost:8000/docs** in browser (postman page)
7. **start giving transcript inputs**, in the format { "transcript" : "" } (user can fill anything in the place of empty strings)

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
1. link - [https://hub.docker.com/repository/docker/dockani4991/chat-summarizer-summarizer/tags/v2/sha256:0eb0dd769c22a009318fd64f0a9c58804814cfdb37475856f6e584104f4c1f81](https://hub.docker.com/repository/docker/dockani4991/chat-summarizer-summarizer/tags/v3/sha256:a92d2f272d578af37caf64f69d6d92ca642fb0e014c2994ea95ca63cd97510fb) (docker pull dockani4991/chat-summarizer-summarizer:v3)
