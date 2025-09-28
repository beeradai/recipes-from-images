# Multimodal Recipe Assistant

This project is a demo of a multimodal recipe assistant that can parse images of fridge contents and suggest recipes using OpenAI's latest API.

## 🚀 Setup

1. **Clone or download this repository**

```bash
git clone https://github.com/beeradai/recipes-from-images.git
cd recipes-from-images
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Set your OpenAI API key**

On Linux / macOS:
```bash
export OPENAI_API_KEY="your_api_key_here"
```

On Windows PowerShell:
```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

4. **Run the Streamlit app**

```bash
streamlit run app.py
```

---

## 🛠 Tech Stack
- Python 3.9+
- [Streamlit](https://streamlit.io/) for the UI
- [OpenAI Python SDK (>=1.0.0)](https://github.com/openai/openai-python)
- Pillow & Requests for image handling

---

## 📌 Notes
- Ensure you’re using `openai>=1.0.0` (this repo has been migrated to the new API).
- If you encounter issues, check that your API key is correctly set and that dependencies are installed.

Enjoy exploring recipes with your fridge images!
