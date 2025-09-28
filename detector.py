from openai import OpenAI

client = OpenAI()

from ultralytics import YOLO
import numpy as np
from PIL import Image

# Load YOLOv8 nano model (small & fast)
model = YOLO("yolov8n.pt")

def detect_ingredients_from_pil(pil_img, conf_threshold=0.35):
    """
    Input: PIL.Image
    Output: list of dicts: [{"label": "apple", "conf": 0.82}, ...]
    """
    img = np.array(pil_img.convert("RGB"))
    results = model(img)
    r = results[0]
    names = model.names

    detected = []
    try:
        cls_tensor = r.boxes.cls.cpu().numpy()
        conf_tensor = r.boxes.conf.cpu().numpy()
        for cls_id, conf in zip(cls_tensor, conf_tensor):
            label = names[int(cls_id)]
            if conf >= conf_threshold:
                detected.append({"label": label, "conf": float(conf)})
    except Exception:
        pass

    # Deduplicate
    best = {}
    for d in detected:
        if d["label"] not in best or d["conf"] > best[d["label"]]:
            best[d["label"]] = d["conf"]
    return [{"label": k, "conf": v} for k, v in best.items()]
