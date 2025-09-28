# llm_recipes.py
import os
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
