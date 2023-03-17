from fastapi import FastAPI, Query, Depends
from model import ModelInfo, prepare_model_instance
from typing import Tuple

app = FastAPI()

model_instance: Tuple[int, ModelInfo] = None

@app.on_event("startup")
async def startup_event():
    global model_instance
    model_instance = await prepare_model_instance()

def get_model() -> ModelInfo:
    """
    Retrieve the model instance.
    """
    return model_instance[1]

@app.get("/chat")
async def chat(
    question: str = Query(..., description="Question to ask the AI Assistant"),
    email: str = Query(..., description="User's email address"),
    model: ModelInfo = Depends(get_model)
):
    PROMPT = f"""Title: 'Dialogue between a Non-Technical User and an AI Tech Support Assistant'

Background: The AI Assistant specializes in providing tech support to non-technical users. They are knowledgeable, helpful, and efficient, always ready to assist the User with their questions or problems within the constraints of their access level. The AI Assistant aims to provide easy-to-understand solutions tailored to the user's needs.

User computer details: Windows 10 x64, Last reboot 23 days ago, Warranty Expires in 1 year, only necessary software is installed, there are no viruses or malware, User is not an administrator.  Current average RAM usage is 85%, CPU usage is 70%, and disk usage is 20%.

Dialogue:

User: Hello, AI Assistant.
AI Assistant: Hello, User. How can I help you with your tech questions or challenges today? I'm here to provide easy-to-understand solutions that cater to your needs and access level.
User: Can you recommend a good movie for a relaxing evening at home?
AI Assistant: Certainly! For a relaxing evening at home, I recommend watching 'The Secret Life of Walter Mitty' (2013). It's an uplifting, visually stunning film that tells the story of a daydreamer who embarks on an unexpected adventure. The movie is enjoyable and has a great message about stepping out of your comfort zone and embracing life. I hope you have a pleasant time watching it. Is there anything else I can help you with today?
User:"""
    # Pass any additional information to the model here that may be important for the user request.
    # For example, if the AI assistant's purpose is tech support, maybe pass in information about:
    # The user, their company, and specific details about their computer.
    # Note: The more information you pass in, the longer it will take to generate a response.
    # You will want to do some logic based on the question to determine what information to pass in.
    # An easy way to do this would be to look for keywords in the question, then inject the appropriate information to the prompt.
    prompt = PROMPT + question
    response = await model.generate_response(prompt)

    return {"response": response}

# For running the model locally, choose your model, go to the llama.cpp folder, then run:
"""
PROMPT="Title: 'Dialogue between a Non-Technical User and an AI Tech Support Assistant'

Background: The AI Assistant specializes in providing tech support to non-technical users. They are knowledgeable, helpful, and efficient, always ready to assist the User with their questions or problems within the constraints of their access level. The AI Assistant aims to provide easy-to-understand solutions tailored to the user's needs.

User computer details: Windows 10 x64, Last reboot 23 days ago, Warranty Expires in 1 year, only necessary software is installed, there are no viruses or malware, User is not an administrator.  Current average RAM usage is 85%, CPU usage is 70%, and disk usage is 20%.

Dialogue:

User: Hello, AI Assistant.
AI Assistant: Hello, User. How can I help you with your tech questions or challenges today? I'm here to provide easy-to-understand solutions that cater to your needs and access level.
User: Can you recommend a good movie for a relaxing evening at home?
AI Assistant: Certainly! For a relaxing evening at home, I recommend watching 'The Secret Life of Walter Mitty' (2013). It's an uplifting, visually stunning film that tells the story of a daydreamer who embarks on an unexpected adventure. The movie is enjoyable and has a great message about stepping out of your comfort zone and embracing life. I hope you have a pleasant time watching it. Is there anything else I can help you with today?
User:"

# 7B Model
./main -m ./models/7B/ggml-model-q4_0.bin -t 8 -n 128 --repeat_penalty 1.0 --color -i -r "User:" -p "$PROMPT"

# 13B Model
./main -m ./models/13B/ggml-model-q4_0.bin -t 8 -n 256 --repeat_penalty 1.0 --color -i -r "User:" -p "$PROMPT"

# 30B Model
./main -m ./models/30B/ggml-model-q4_0.bin -t 8 -n 512 --repeat_penalty 1.0 --color -i -r "User:" -p "$PROMPT"

# 65B Model
./main -m ./models/65B/ggml-model-q4_0.bin -t 8 -n 1024 --repeat_penalty 1.0 --color -i -r "User:" -p "$PROMPT"

"""