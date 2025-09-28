import os
from openai import OpenAI
import streamlit as st
from PIL import Image
from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes
import json

st.set_page_config(page_title="AI Recipe Generator", page_icon="��", layout="wide")
st.title("�� Multimodal Recipe Assistant")

st.write("Upload one or more fridge images or type in ingredients manually:")

# �� Multiple image uploads
uploaded_images = st.file_uploader(
    "Upload fridge/ingredient images", type=["jpg", "jpeg", "png"], accept_multiple_files=True
)

# �� Manual text input
manual_input = st.text_area("Or enter ingredients manually (comma-separated):", "")

ingredient_list = []

# process uploaded images
if uploaded_images:
    for img_file in uploaded_images:
        pil_img = Image.open(img_file).convert("RGB")
        detected = detect_ingredients_from_pil(pil_img)
        ingredient_list.extend(normalize_detected(detected))

# process manual input
if manual_input.strip():
    manual_items = [i.strip() for i in manual_input.split(",") if i.strip()]
    ingredient_list.extend(manual_items)

# remove duplicates
ingredient_list = sorted(set(ingredient_list))

if ingredient_list:
    st.success(f"✅ Ingredients detected: {', '.join(ingredient_list)}")
else:
    st.info("No ingredients detected yet. Upload an image or type some in!")

constraints = st.text_input("Any dietary constraints? (e.g. vegetarian, gluten-free)")

if st.button("�� Generate Recipes"):
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

            st.markdown("---")
    else:
        st.error("❌ No recipes generated.")

