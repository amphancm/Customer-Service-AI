from fastapi import FastAPI, Request
from pydantic import BaseModel
from openai import OpenAI

app = FastAPI()

# Use Ollama-compatible OpenAI client
ollama = OpenAI(
    api_key="ollama",  # fake key, Ollama ignores it
    base_url="http://localhost:11434/v1"
)

class ChatRequest(BaseModel):
    messages: list
    model: str = "phi4-mini:latest"

# @app.post("/chat")
# async def chat_endpoint(req: ChatRequest):
#     response = ollama.chat.completions.create(
#         model=req.model,
#         messages=req.messages
#     )

    # print("Response from Ollama:", response.choices[0].message.content)
    # return {"response": response.choices[0].message.content}

if __name__ == "__main__":
    # Example usage: simple chat loop
    model = "phi4-mini:latest"
    messages = []
    print("Type 'exit' to quit.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        response = ollama.chat.completions.create(
            model=model,
            messages=messages
        )
        reply = response.choices[0].message.content
        print("AI:", reply)
        messages.append({"role": "assistant", "content": reply})