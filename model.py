import os
import asyncio
from aiohttp import ClientSession
from asyncio import subprocess
from typing import Tuple

class ModelInfo:
    def __init__(self, path: str, tokens: int):
        self.path = path
        self.tokens = tokens

    async def generate_response(self, prompt: str) -> str:
        result = await asyncio.create_subprocess_exec(
            "./llama.cpp/main",
            "-m", self.path,
            "-t", "8",
            "-n", str(self.tokens),
            "--repeat_penalty", "1.0",
            "-r", "Josh:",
            "-p", prompt,
            stdout=subprocess.PIPE,
        )

        stdout, _ = await result.communicate()
        response = stdout.decode("utf-8").split(prompt)[1]
        return response

async def download_model():
    url = "https://raw.githubusercontent.com/shawwn/llama-dl/56f50b96072f42fb2520b1ad5a1d6ef30351f23c/llama.sh"
    async with ClientSession() as session:
        async with session.get(url) as response:
            script = await response.text()

    with open("llama.sh", "w") as f:
        f.write(script)

    await asyncio.create_subprocess_exec("bash", "llama.sh")

async def check_and_clone_llama_cpp():
    if not os.path.exists("llama.cpp"):
        await asyncio.create_subprocess_exec("git", "clone", "https://github.com/ggerganov/llama.cpp")
        await asyncio.create_subprocess_exec("make", cwd="llama.cpp")

async def prepare_model(size: int, tokens: int) -> ModelInfo:
    model_path = f"./llama.cpp/models/{size}B/ggml-model-q4_0.bin"

    if not os.path.isfile(model_path):
        await check_and_clone_llama_cpp()
        await download_model()
        await asyncio.create_subprocess_exec("python3", "./llama.cpp/convert-pth-to-ggml.py", f"./llama.cpp/models/{size}B/", "1")
        await asyncio.create_subprocess_exec("./llama.cpp/quantize.sh", f"{size}B")

    return ModelInfo(model_path, tokens)

def get_model_size() -> int:
    """
    Retrieve and validate the model size from the MODEL_SIZE environment variable.
    """
    model_size = int(os.getenv("MODEL_SIZE", "7"))
    if model_size not in [7, 13, 30, 65]:
        raise ValueError("Invalid model size. Available model sizes: 7, 13, 30, 65")
    return model_size

async def prepare_model_instance() -> Tuple[int, ModelInfo]:
    model_size = get_model_size()
    return model_size, await prepare_model(model_size, {7: 128, 13: 256, 30: 512, 65: 1024}[model_size])
