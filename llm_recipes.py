# llm_recipes.py
import os
import json
import streamlit as st
from openai import OpenAI

def get_api_key():
    try:
        # Works on Streamlit Cloud
        if "OPENAI_API_KEY" in st.secrets:
            return st.secrets["OPENAI_API_KEY"]
    except Exception:
        pass  # st.secrets not available locally

    # Local fallback
    return os.getenv("OPENAI_API_KEY")

api_key = get_api_key()
if not api_key:
    raise ValueError(
        "❌ No OpenAI API key found. Set it in .streamlit/secrets.toml or as an environment variable."
    )

client = OpenAI(api_key=api_key)

def generate_recipes(ingredients, constraints=None, n_recipes=2, model="gpt-4o-mini"):
    constraints_text = constraints or "no constraints"
    prompt = f"""
    You are a recipe generator. Given the following ingredients:
    {ingredients}

    And constraints: {constraints_text}

    Generate {n_recipes} recipes in strict JSON format like this:
    {{
      "recipes": [
        {{
          "title": "Recipe title",
          "ingredients": ["item1", "item2"],
          "instructions": ["Step 1", "Step 2"],
          "estimated_time_minutes": 25
        }}
      ]
    }}
    """

    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )

    content = resp.choices[0].message.content.strip()

    try:
        return json.loads(content)  # ✅ parse LLM output into dict
    except json.JSONDecodeError:
        # fallback: wrap raw text
        return {"recipes": [{"title": "Parsing error", "instructions": [content]}]}
