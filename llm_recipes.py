import os
import json
from openai import OpenAI

client = OpenAI()

openai.api_key = os.environ.get("OPENAI_API_KEY")

BASE_SYSTEM = (
    "You are a helpful, precise recipe assistant. "
    "Given a list of available ingredients and optional dietary constraints, "
    "produce up to 3 recipe suggestions. For each recipe return the following fields: "
    "title, ingredients (list of ingredient+quantity), estimated_time_minutes, difficulty, "
    "steps (list), substitutions, and shopping_list. "
    "Return ONLY JSON with top-level key 'recipes'."
)

def generate_recipes(ingredients, constraints="", n_recipes=2, model="gpt-3.5-turbo", temperature=0.7):
    ing_text = ", ".join(ingredients)
    user_prompt = (
        f"Available ingredients: {ing_text}\n"
        f"Dietary constraints: {constraints}\n"
        f"Produce {n_recipes} recipe suggestions."
    )

    messages = [
        {"role": "system", "content": BASE_SYSTEM},
        {"role": "user", "content": user_prompt},
    ]

    resp = client.chat.completions.create(
        model=model,
        messages=messages,
        max_tokens=800,
        temperature=temperature,
        n=1,
    )

    text = resp["choices"][0]["message"]["content"].strip()
    try:
        return json.loads(text)
    except:
        try:
            first, last = text.index("{"), text.rindex("}") + 1
            return json.loads(text[first:last])
        except:
            return {"error": "Failed to parse", "raw": text}
