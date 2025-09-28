import os
from openai import OpenAI
import streamlit as st
from PIL import Image
from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes
import json

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
                st.markdown(f"⏱ {r.get('estimated_time_minutes', '—')} minutes")

                st.markdown("**Ingredients:**")
                st.write(r.get("ingredients", []))

                st.markdown("**Steps:**")
                instructions = r.get("instructions", [])
                if instructions:
                    for i, step in enumerate(instructions, 1):
                        st.markdown(f"{i}. {step}")
                else:
                    st.markdown("_No steps generated_")
        else:
            st.error("Recipe generation failed.")
            st.code(json.dumps(out, indent=2))
