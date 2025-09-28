import streamlit as st
from PIL import Image
from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes
import json

st.set_page_config(page_title="�� Recipes from Images", layout="wide")

st.title("�� Recipes from Your Ingredients")
st.write("Upload ingredient photos and/or type them manually, then generate recipes!")

# --- Upload multiple images ---
uploaded_files = st.file_uploader(
    "�� Upload 1–5 ingredient images", 
    type=["jpg", "jpeg", "png"], 
    accept_multiple_files=True
)

all_detected = []
if uploaded_files:
    for file in uploaded_files:
        pil_img = Image.open(file).convert("RGB")
        detected = detect_ingredients_from_pil(pil_img)
        normalized = normalize_detected(detected)
        all_detected.extend(normalized)

# --- Deduplicate ingredients ---
all_detected = sorted(set(all_detected))

# --- Checkbox selection for detected ingredients ---
selected_ingredients = []
if all_detected:
    st.subheader("✅ Select detected ingredients to include")
    for ing in all_detected:
        if st.checkbox(ing, value=True, key=f"chk_{ing}"):
            selected_ingredients.append(ing)

# --- Manual text input ---
manual_input = st.text_area("✍️ Add ingredients manually (comma-separated)")
if manual_input.strip():
    manual_ingredients = [i.strip() for i in manual_input.split(",") if i.strip()]
    selected_ingredients.extend(manual_ingredients)

# --- Constraints (e.g., vegan, gluten-free) ---
constraints = st.text_input("⚙️ Optional cooking constraints (e.g., vegan, gluten-free, 30 min max)")

# --- Generate Recipes button ---
if not selected_ingredients:
    st.warning("�� Please select or add at least one ingredient before generating recipes.")
else:
    if st.button("�� Generate Recipes"):
        with st.spinner("Cooking up ideas..."):
            out = generate_recipes(selected_ingredients, constraints=constraints)

        if "recipes" in out:
            for r in out["recipes"]:
                st.subheader(r.get("title", "Untitled"))
                st.write(f"⏱ Estimated time: {r.get('estimated_time_minutes', '—')} minutes")

                st.markdown("**Ingredients:**")
                st.write(", ".join(r.get("ingredients", [])))

                st.markdown("**Steps:**")
                steps = r.get("steps", [])
                if isinstance(steps, list):
                    for i, step in enumerate(steps, 1):
                        st.write(f"{i}. {step}")
                else:
                    st.write(steps)
        else:
            st.error("⚠️ No recipes generated. Please try again.")
