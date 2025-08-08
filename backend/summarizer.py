from google.genai import GenerationServiceClient
from google.genai.types import ModelName, TextPrompt

# Initialize the client
client = GenerationServiceClient()

# Define your project and location
PROJECT_ID = "YOUR_GCP_PROJECT_ID"
LOCATION = "us-central1"

# Define the model you want to use
MODEL = "models/gemini-1.5-pro"

def generate_summary(text: str, max_chars: int = 10000, max_output_tokens: int = 512) -> str:
    if len(text) > max_chars:
        text = text[:max_chars] + "\n... [truncated]"

    prompt_text = f"Please provide a concise summary of the following content:\n\n{text}"

    model_name = ModelName(project=PROJECT_ID, location=LOCATION, model=MODEL)

    prompt = TextPrompt(text=prompt_text)

    response = client.generate_text(
        model=model_name,
        prompt=prompt,
        max_output_tokens=max_output_tokens,
        temperature=0.2,
    )

    return response.text if response.text else ""
