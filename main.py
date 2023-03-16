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
    PROMPT = f"""Transcript of a dialog, where the User ({email}) interacts with an AI Assistant. AI Assistant is knowledgeable, helpful, and efficient, with expertise in various domains. It is always ready to assist the User with any questions or problems they may have. {email} is a Systems Engineer and Software Engineer seeking information and guidance from the AI Assistant.

{email}: Hello, AI Assistant.
AI Assistant: Hello, {email}. It's great to meet you. How can I assist you today in your quest for knowledge or help you solve any challenges you may face?
{email}: What color is peanut butter?
AI Assistant: Peanut butter typically has a brown color, which can vary from light to dark depending on the type of peanuts used and the roasting process. Is there anything else you would like to know or discuss?
{email}: """
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
# 7B Model
PROMPT="Dialogue between a User and an AI Assistant specializing in tech support for non-technical users. The AI Assistant is knowledgeable, helpful, and efficient, always ready to assist the User with their questions or problems within the constraints of their access level. The AI Assistant aims to provide easy-to-understand solutions tailored to the user's needs.

User: Hello, AI Assistant.
AI Assistant: Hello, User. How can I help you with your tech questions or challenges today, keeping in mind your limited technical knowledge and access level? I'm here to provide easy-to-understand solutions.
User: I'm having trouble connecting to the Wi-Fi. What can I do?
AI Assistant: To troubleshoot Wi-Fi connection issues, try these steps: ensure Wi-Fi is enabled on your device, check the Wi-Fi network name and password, move closer to the router, restart your device, and, if possible, restart the router. If the issue persists, contact your network administrator or internet service provider for assistance. Is there anything else you would like to know or discuss?
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