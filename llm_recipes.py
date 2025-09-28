import os
import json
import streamlit as st
from openai import OpenAI

# Initialize OpenAI client
if "OPENAI_API_KEY" in os.environ:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
elif "OPENAI_API_KEY" in st.secrets:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
else:
    raise RuntimeError("❌ OPENAI_API_KEY not found in environment or Streamlit secrets")

def generate_recipes(ingredients, constraints="", n_recipes=2, model="gpt-4o-mini"):
    """
    Generate structured recipes given a list of ingredients and optional constraints.
    Ensures steps are returned as a list.
    """
    prompt = f"""
You are a helpful AI chef. 
Generate {n_recipes} creative recipes using ONLY the following ingredients (and pantry basics like salt, pepper, oil, water if needed):

Ingredients: {', '.join(ingredients)}

Constraints: {constraints if constraints else 'none'}

Return JSON strictly in this format:
{{
  "recipes": [
    {{
      "title": "string",
      "estimated_time_minutes": int,
      "ingredients": ["item1", "item2", ...],
      "steps": ["step 1", "step 2", "step 3", ...]
    }}
  ]
}}
Make sure "steps" is always a JSON list of strings, never a single block of text.
"""

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
    )

    content = resp.choices[0].message.content.strip()

    try:
        return json.loads(content)  # ✅ structured dict
    except json.JSONDecodeError:
        # fallback: wrap raw text
        return {
            "recipes": [
                {
                    "title": "Parsing error",
                    "ingredients": ingredients,
                    "steps": [content],
                    "estimated_time_minutes": "—"
                }
            ]
        }

