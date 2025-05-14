import google.generativeai as genai
from django.conf import settings

# Configura Gemini con tu API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Usa el modelo Gemini Pro
model = genai.GenerativeModel("gemini-2.0-flash")

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
