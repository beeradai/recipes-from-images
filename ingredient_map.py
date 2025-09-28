from openai import OpenAI

client = OpenAI()

# Basic label → canonical ingredient mapping
MAP = {
    "banana": "banana",
    "apple": "apple",
    "orange": "orange",
    "broccoli": "broccoli",
    "carrot": "carrot",
    "wine glass": "wine",
    "knife": None,
    "cup": None,
    "bottle": None,
}

def normalize_detected(detected_list):
    """
    detected_list: [{"label": "banana", "conf": 0.9}, ...]
    returns: list of canonical ingredient strings
    """
    normalized = []
    for d in detected_list:
        lab = d["label"]
        if lab in MAP:
            mapped = MAP[lab]
            if mapped:
                normalized.append(mapped)
        else:
            normalized.append(lab)
    return list(dict.fromkeys(normalized))
