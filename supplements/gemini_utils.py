import google.generativeai as genai
from django.conf import settings

# Configura Gemini con tu API key
genai.configure(api_key=settings.GEMINI_API_KEY)

# Usa el modelo Gemini Pro
model = genai.GenerativeModel("gemini-2.0-flash")

base_prompt = """
You are a professional assistant specializing in supplementation. Your role is to provide expert advice strictly related to supplements. 
You will be given information about a customer, such as their age, gender, activity level, dietary preferences, and specific goals or concerns. 
Based on this information, recommend a type of supplement that aligns with their needs. Avoid mentioning any specific brands in your recommendations.
Your responses should be concise, informative, and focused on the supplement type recommended according to the user's needs.
Do not include any disclaimers or unnecessary information. Only provide the supplement type and its benefits. 
Always ask the user if they have any other questions or need further assistance.
Always remind the user to consult a healthcare professional before starting any new supplement regimen.
Before answering anything, you will detect wether the users concern is written in Spanish or English, and you will answer in the same language.
If the user is asking about a specific supplement, provide a brief overview of its benefits and potential side effects.
If the user doesnt provide sufficient information, ask them to provide more details about their health status, goals, and any specific concerns they may have.
Do not provide any medical advice or recommendations outside of supplementation. Do not recommend illegal or banned substances.
"""

def generate_prompt(user):
    """
    Generate a prompt for Gemini based on user information.
    :param user_info: Dictionary containing user information.
    :return: Formatted prompt string.
    """
    user_info = {
        user.first_name: user.first_name,
        user.last_name: user.last_name,
        user.email: user.email,
        user.username: user.username,
        user.profile.phone: user.profile.phone,
    }
    prompt = base_prompt
    prompt += f"\nUser Info: {user_info}\n"
    prompt += "User's Concerns: "
    return prompt

def ask_gemini(user_prompt):
    try:
        response = model.generate_content(user_prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"
