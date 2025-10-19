\
def normalize_detected(ingredients):
    mapping = {
        "tomato": "tomatoes",
        "onion": "onions",
        "carrot": "carrots"
    }
    return [mapping.get(i.lower(), i.lower()) for i in ingredients]
