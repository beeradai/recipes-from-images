\
from openai import OpenAI
import json

client = OpenAI()

def generate_recipes(ingredients):
    ingredients_str = ", ".join(ingredients)
    prompt = f"Create 2 creative recipes using the following ingredients: {ingredients_str}. Return JSON with a list of recipes, each having a 'title' and 'steps' list."
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )
    recipes = response.choices[0].message.content
    try:
        data = json.loads(recipes)
        return data.get("recipes", [])
    except Exception:
        return [{"title": "Generated Recipe", "steps": [recipes]}]
