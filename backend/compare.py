#pip install -q -U google-genai

from google import genai

client = genai.Client(api_key="api key here")
response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Evaluating a resume"
)
print(response.text)