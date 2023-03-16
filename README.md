# AI Assistant

This is an AI Assistant application that uses FastAPI, React, and the [llama.cpp](https://github.com/ggerganov/llama.cpp) library, which uses [Meta's LLaMa](https://github.com/facebookresearch/llama) large language model.. The llama.cpp library provides a lightweight implementation of the OpenAI GPT-3-like models. The application automatically pulls the llama.cpp repo, as well as the models and weights.

## Backend

The backend is implemented using FastAPI. It has a single endpoint `/chat` for interacting with the AI Assistant. The application automatically downloads the required models and weights for the specified model size during startup.

### Running the backend

To run the backend, first install the required dependencies:

```bash
pip install -r requirements.txt
```

Then, start the FastAPI server:

```bash
uvicorn main:app --host 0.0.0.0 --port 5437
```

## Frontend

The frontend is a basic React application that interacts with the backend using the `/chat` endpoint. It shows a loading symbol while waiting for a reply from the FastAPI server.

### Running the frontend

First, make sure you have Node.js and `yarn` installed. Then, create a new React app:

```bash
cd ai-assistant-front-end
yarn install
```

Run the following command to start the development server:

```bash
yarn start
```

This will start the development server, and you can access the React app at `http://localhost:3000`.

## Docker

You can also run the AI Assistant using Docker. A `Dockerfile` and `docker-compose.yml` file are provided for this purpose. To run the application using Docker, execute the following command:

```bash
docker-compose up --build
```

This will build the Docker image and start the container. You can then access the AI Assistant API at `http://localhost:5437`.
