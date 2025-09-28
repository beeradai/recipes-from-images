import os
from openai import OpenAI
import streamlit as st
from PIL import Image
from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes
import json

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="AI Recipe Assistant", page_icon="��", layout="centered")
st.title("�� Multimodal Recipe Assistant")
st.caption("Upload fridge/pantry photos + add ingredients manually to generate creative recipes!")

# --- Image upload ---
uploaded_files = st.file_uploader(
    "�� Upload fridge/pantry images",
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)

ingredient_list = []

if uploaded_files:
    for uploaded_file in uploaded_files:
        img = Image.open(uploaded_file)
        detected = detect_ingredients_from_pil(img)
        ingredient_list.extend(detected)

    # Normalize & deduplicate
    ingredient_list = list(set(normalize_detected(ingredient_list)))

    st.subheader("�� Detected Ingredients")
    st.caption("Uncheck any items you don’t want to include:")

    # Multi-select with checkboxes
    selected_ingredients = []
    for ing in ingredient_list:
        if st.checkbox(ing, value=True):
            selected_ingredients.append(ing)

    ingredient_list = selected_ingredients

# --- Manual ingredient entry ---
manual_text = st.text_area("✍️ Add extra ingredients (comma-separated):")
if manual_text:
    manual_ings = [x.strip() for x in manual_text.split(",") if x.strip()]
    ingredient_list.extend(manual_ings)

ingredient_list = list(set(ingredient_list))  # deduplicate again

if ingredient_list:
    st.success("✅ Ingredients ready: " + ", ".join(ingredient_list))

# --- Dietary constraints ---
constraints = st.text_input("⚡ Any dietary preferences or constraints? (e.g. vegan, gluten-free, low-carb)")

# --- Generate recipes ---
if st.button("�� Generate Recipes"):
    if not ingredient_list:
        st.warning("Please provide at least one ingredient!")
    else:
        with st.spinner("Cooking up ideas..."):
            out = generate_recipes(ingredient_list, constraints=constraints, n_recipes=2)

        if "recipes" in out:
            for r in out["recipes"]:
                st.subheader(r.get("title", "Untitled"))
                st.markdown(f"⏱ {r.get('estimated_time_minutes', '—')} minutes")
                st.markdown("**Ingredients:**")
                st.write(", ".join(r.get("ingredients", [])))

                st.markdown("**Steps:**")
                steps = r.get("steps", [])
                if isinstance(steps, list):
                    for i, step in enumerate(steps, 1):
                        st.markdown(f"{i}. {step}")
                else:
                    st.write(steps)

                st.divider()
        else:
            st.error("⚠️ Could not parse recipe output. Here’s the raw response:")
            st.text(out)

