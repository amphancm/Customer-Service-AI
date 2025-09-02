import openai

# Configure OpenAI client to connect to Ollama server running on 192.168.1.4
openai.api_base = "http://192.168.1.4:11434/v1"
openai.api_key = "ollama"  # Ollama uses a dummy key

def get_embedding(text):
    response = openai.Embedding.create(
        input=text,
        model="bge-m3"
    )
    return response['data'][0]['embedding']

if __name__ == "__main__":
    text = "Your text string goes here"
    embedding = get_embedding(text)
    print(embedding)