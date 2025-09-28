# llm_recipes.py
import os
from openai import OpenAI

# Initialize client with API key from environment variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_recipes(ingredients, constraints=None, n_recipes=2, model="gpt-4o-mini"):
    """
    Generate recipes using a list of ingredients and optional constraints.
    """
    prompt = f"Generate {n_recipes} creative and detailed recipes using the following ingredients: {ingredients}."
    if constraints:
        prompt += f" Please follow these constraints: {constraints}."

    messages = [
        {"role": "system", "content": "You are a helpful recipe assistant that generates structured recipes."},
        {"role": "user", "content": prompt}
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return resp.choices[0].message.content

