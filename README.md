# 🍳 Multimodal Recipe Assistant

An AI-powered app that generates recipe ideas from a photo of your fridge/pantry.

## ✨ Features
- Upload an image → detects ingredients using YOLOv8.
- User edits/approves the ingredient list.
- LLM suggests recipes (title, steps, substitutions, shopping list).
- Optional dietary preferences (vegetarian, vegan, etc.).

## 🛠 Tech Stack
- **Computer Vision**: YOLOv8 (Ultralytics)
- **NLP**: OpenAI GPT-3.5 (recipe generation)
- **Frontend**: Streamlit
- **Language**: Python

## 🚀 Quickstart
```bash
git clone <this-repo-url>
cd multimodal-recipe-assistant
pip install -r requirements.txt
export OPENAI_API_KEY="your_api_key_here"
streamlit run app.py
```

Upload a fridge photo, edit ingredients, and let the AI suggest recipes! 🎉

## 🔮 Future Improvements
- Fine-tuned food detection model (GroZi/Food-101 dataset).
- Nutrition analysis.
- Recipe retrieval + adaptation (reduce hallucinations).
- Shopping list optimizer.


## 🧪 Demo
A sample fridge image (`sample_fridge.jpg`) is included for testing.

Run the app and upload it:
```bash
streamlit run app.py
```
Then upload `sample_fridge.jpg` when prompted.
