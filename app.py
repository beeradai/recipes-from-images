\
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from PIL import Image
from io import BytesIO
import uvicorn
import os
import json

from detector import detect_ingredients_from_pil
from ingredient_map import normalize_detected
from llm_recipes import generate_recipes

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def upload_form():
    html = """
    <html>
        <head>
            <title>Recipe Generator</title>
            <style>
                body { font-family: sans-serif; max-width: 700px; margin: 30px auto; text-align: center; }
                .image-preview { width: 150px; border-radius: 10px; margin: 10px; }
                textarea { width: 100%; height: 100px; border-radius: 10px; padding: 10px; }
                button { padding: 10px 20px; border-radius: 10px; cursor: pointer; }
            </style>
        </head>
        <body>
            <h1>Upload Images or Enter Ingredients</h1>
            <form action="/generate" enctype="multipart/form-data" method="post">
                <input type="file" name="images" multiple accept="image/*"><br><br>
                <textarea name="ingredients_text" placeholder="Add ingredients manually..."></textarea><br><br>
                <button type="submit">Generate Recipes</button>
            </form>
        </body>
    </html>
    """
    return HTMLResponse(content=html)

@app.post("/generate", response_class=HTMLResponse)
async def generate(images: list[UploadFile] = File(default=[]), ingredients_text: str = Form(default="")):
    detected_all = []

    for image in images:
        contents = await image.read()
        pil_img = Image.open(BytesIO(contents))
        detected = detect_ingredients_from_pil(pil_img)
        detected_all.extend(detected)

    normalized = normalize_detected(list(set(detected_all)))
    if ingredients_text.strip():
        normalized.extend([i.strip() for i in ingredients_text.split(",") if i.strip()])

    recipes = generate_recipes(normalized)

    recipe_html = "<h2>Generated Recipes</h2>"
    for r in recipes:
        recipe_html += f"<div><h3>{r['title']}</h3><ul>" + "".join([f"<li>{step}</li>" for step in r['steps']]) + "</ul></div>"

    return HTMLResponse(content=f"<html><body><a href='/'>⬅️ Back</a>{recipe_html}</body></html>")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
