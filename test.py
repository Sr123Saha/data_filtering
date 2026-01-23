

from flask import Flask, request, jsonify, render_template
import csv
import json
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

data_storage = []
original_data = []

REQUIRED_FIELDS = ['код', 'наименование', 'категория', 'количество', 'цена']

def load_data(path):

    if path.endswith(".csv") or path.endswith(".txt"):
        with open(path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            data = list(reader)

    elif path.endswith(".json"):
        with open(path, encoding="utf-8") as f:
            data = json.load(f)

    else:
        raise ValueError("Неподдерживаемый формат файла")

    if not data:
        raise ValueError("Файл пуст")

    for field in REQUIRED_FIELDS:
        if field not in data[0]:
            raise ValueError(f"Отсутствует поле: {field}")

    for row in data:
        row["код"] = int(row["код"])
        row["количество"] = int(row["количество"])
        row["цена"] = float(row["цена"])

    return data

def filter_data(data, category=None, min_price=None):

    result = data

    if category and category.strip():
        result = [
            x for x in result
            if category.lower() in x["категория"].lower()
        ]

    if min_price and str(min_price).strip():
        result = [
            x for x in result
            if x["цена"] >= float(min_price)
        ]

    return result

def sort_data(data, field):
    return sorted(data, key=lambda x: x[field])

def calculate_stats(data):
    count = len(data)
    total = sum(x["цена"] * x["количество"] for x in data)
    avg = total / count if count else 0
    return count, total, round(avg, 2)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload():
    try:
        global data_storage, original_data

        file = request.files["file"]
        path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(path)

        data_storage = load_data(path)
        original_data = data_storage.copy()

        return jsonify(data_storage)

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route("/process", methods=["POST"])
def process():

    global data_storage

    params = request.json

    data = filter_data(
        data_storage,
        params.get("category"),
        params.get("min_price")
    )

    if params.get("sort"):
        data = sort_data(data, params["sort"])

    data_storage = data

    count, total, avg = calculate_stats(data_storage)

    return jsonify({
        "data": data_storage,
        "stats": {
            "count": count,
            "sum": total,
            "avg": avg
        }
    })

@app.route("/reset")
def reset():
    global data_storage, original_data

    data_storage = original_data.copy()

    return jsonify(data_storage)

@app.route("/save")
def save():

    with open("result.json", "w", encoding="utf-8") as f:
        json.dump(data_storage, f, ensure_ascii=False, indent=2)

    return render_template("saved.html", data=data_storage)

if __name__ == "__main__":
    app.run(debug=True)
