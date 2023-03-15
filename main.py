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

    prompt = PROMPT + question
    response = await model.generate_response(prompt)

    return {"response": response}
