\
from ultralytics import YOLO
from PIL import Image

model = YOLO("yolov8n.pt")

def detect_ingredients_from_pil(pil_img, conf_threshold=0.35):
    results = model.predict(pil_img, conf=conf_threshold)
    names = model.names
    ingredients = []
    for r in results:
        for box in r.boxes:
            cls = int(box.cls[0])
            ingredients.append(names[cls])
    return ingredients
