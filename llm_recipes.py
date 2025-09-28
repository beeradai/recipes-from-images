import os
import json
import streamlit as st
from openai import OpenAI

# �� Initialize OpenAI client
if "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

MODEL = "gpt-4o-mini"  # fast + multimodal

def generate_recipes(ingredients, constraints=None, n_recipes=2, model=MODEL):
    """
    Generate structured recipes from a list of ingredients using OpenAI.
    Always returns JSON with 'recipes' → list of dicts containing
    title, estimated_time_minutes, ingredients, steps.
    """
    prompt = f"""
You are a recipe generator. 
Create {n_recipes} recipes using the following available ingredients:

Ingredients: {ingredients}

Constraints: {constraints if constraints else "None"}

⚠️ OUTPUT FORMAT: Return ONLY valid JSON. No commentary, no markdown.
Schema:
{{
  "recipes": [
    {{
      "title": "string",
      "estimated_time_minutes": number,
      "ingredients": ["item1", "item2"],
      "steps": ["First step...", "Second step...", "..."]
    }}
  ]
}}
    """

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    content = resp.choices[0].message.content.strip()

    try:
        return json.loads(content)  # ✅ parse JSON output
    except json.JSONDecodeError:
        # fallback if the model outputs invalid JSON
        return {
            "recipes": [
                {
                    "title": "Parsing error",
                    "estimated_time_minutes": 0,
                    "ingredients": ingredients,
                    "steps": [content],  # fallback: dump raw text
                }
            ]
        }

