import json
import os

FILE = "memory.json"

def store_memory(q, a):
    data = []
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
        except:
             data = []

    data.append({"q": q, "a": a})

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_memory():
    if os.path.exists(FILE):
        try:
            with open(FILE, "r") as f:
                data = json.load(f)
                # Return last 5 interactions
                return str(data[-5:])
        except:
            return ""
    return ""
