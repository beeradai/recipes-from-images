from openai import OpenAI

client = OpenAI()

import streamlit as st
from PIL import Image
from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes
import json

st.set_page_config(page_title="🍳 Multimodal Recipe Assistant", layout="centered")
st.title("🍳 Multimodal Recipe Assistant")

uploaded = st.file_uploader("Upload a fridge/pantry photo", type=["jpg", "jpeg", "png"])
constraints = st.text_input("Dietary preferences (optional)", "")

if uploaded:
    img = Image.open(uploaded)
    st.image(img, caption="Uploaded image", use_container_width=True)

    st.write("🔎 Detecting ingredients...")
    detected = detect_ingredients_from_pil(img)
    st.write("Detections:", detected)

    normalized = normalize_detected(detected)
    st.write("Normalized ingredient candidates:")
    editable = st.text_area("Edit ingredient list (comma-separated)", value=", ".join(normalized))
    ingredient_list = [i.strip() for i in editable.split(",") if i.strip()]

    if st.button("🍲 Generate Recipes"):
        with st.spinner("Cooking up ideas..."):
            out = generate_recipes(ingredient_list, constraints=constraints, n_recipes=2)
        if "recipes" in out:
            for r in out["recipes"]:
                st.subheader(r.get("title", "Untitled"))
                st.markdown(f"⏱ {r.get('estimated_time_minutes', '—')} min • 🎚 {r.get('difficulty', '—')}")
                st.markdown("**Ingredients:**")
                for ingr in r.get("ingredients", []):
                    st.write(f"- {ingr}")
                st.markdown("**Steps:**")
                for i, step in enumerate(r.get("steps", []), 1):
                    st.write(f"{i}. {step}")
                if r.get("substitutions"):
                    st.markdown("**Substitutions:**")
                    for s in r["substitutions"]:
                        st.write(f"- {s}")
                if r.get("shopping_list"):
                    st.markdown("**Shopping list:**")
                    for s in r["shopping_list"]:
                        st.write(f"- {s}")
        else:
            st.error("Recipe generation failed.")
            st.code(json.dumps(out, indent=2))
