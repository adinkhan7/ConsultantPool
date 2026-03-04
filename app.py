import json
import os
from flask import Flask, jsonify, request, render_template, after_this_request

app = Flask(__name__)


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response

DATA_FILE = os.path.join(os.path.dirname(__file__), "data", "consultants.json")

SEED_DATA = [
    {"id": 1, "name": "Ahsan Rahman", "age": 42, "expertise": "Data Analytics", "yearsExp": 15, "location": "Dhaka", "hourlyRate": 65, "availability": "Available"},
    {"id": 2, "name": "Farzana Kabir", "age": 37, "expertise": "Public Health", "yearsExp": 12, "location": "Chittagong", "hourlyRate": 60, "availability": "Available"},
    {"id": 3, "name": "Mahmud Hasan", "age": 45, "expertise": "Supply Chain", "yearsExp": 18, "location": "Dhaka", "hourlyRate": 70, "availability": "Busy"},
    {"id": 4, "name": "Nusrat Jahan", "age": 33, "expertise": "Gender Studies", "yearsExp": 9, "location": "Rajshahi", "hourlyRate": 55, "availability": "Available"},
    {"id": 5, "name": "Tanvir Alam", "age": 39, "expertise": "IT Systems", "yearsExp": 14, "location": "Dhaka", "hourlyRate": 75, "availability": "Available"},
    {"id": 6, "name": "Rezaul Karim", "age": 51, "expertise": "Agriculture Policy", "yearsExp": 25, "location": "Bogura", "hourlyRate": 68, "availability": "Busy"},
    {"id": 7, "name": "Sadia Islam", "age": 34, "expertise": "Education Reform", "yearsExp": 10, "location": "Dhaka", "hourlyRate": 58, "availability": "Available"},
    {"id": 8, "name": "Arif Chowdhury", "age": 48, "expertise": "Financial Consulting", "yearsExp": 20, "location": "Sylhet", "hourlyRate": 85, "availability": "Busy"},
    {"id": 9, "name": "Tasnim Ahmed", "age": 31, "expertise": "UX Research", "yearsExp": 7, "location": "Dhaka", "hourlyRate": 50, "availability": "Available"},
    {"id": 10, "name": "Kamrul Hasan", "age": 44, "expertise": "Infrastructure Planning", "yearsExp": 16, "location": "Khulna", "hourlyRate": 72, "availability": "Busy"},
    {"id": 11, "name": "Rafiq Ahmed", "age": 52, "expertise": "Development Economics", "yearsExp": 24, "location": "Dhaka", "hourlyRate": 90, "availability": "Available"},
    {"id": 12, "name": "Sharmin Akter", "age": 36, "expertise": "Nutrition Programs", "yearsExp": 11, "location": "Barisal", "hourlyRate": 57, "availability": "Available"},
    {"id": 13, "name": "Imran Hossain", "age": 40, "expertise": "Market Research", "yearsExp": 14, "location": "Dhaka", "hourlyRate": 62, "availability": "Busy"},
    {"id": 14, "name": "Shaila Noor", "age": 29, "expertise": "Social Research", "yearsExp": 6, "location": "Dhaka", "hourlyRate": 48, "availability": "Available"},
    {"id": 15, "name": "Moinul Haque", "age": 47, "expertise": "Energy Policy", "yearsExp": 19, "location": "Dhaka", "hourlyRate": 82, "availability": "Busy"},
    {"id": 16, "name": "Fahmida Sultana", "age": 35, "expertise": "Climate Adaptation", "yearsExp": 11, "location": "Khulna", "hourlyRate": 63, "availability": "Available"},
    {"id": 17, "name": "Ziaur Rahman", "age": 50, "expertise": "Project Management", "yearsExp": 22, "location": "Dhaka", "hourlyRate": 88, "availability": "Busy"},
    {"id": 18, "name": "Tamanna Rahman", "age": 32, "expertise": "Monitoring & Evaluation", "yearsExp": 8, "location": "Dhaka", "hourlyRate": 56, "availability": "Available"},
    {"id": 19, "name": "Hasan Mahmud", "age": 43, "expertise": "Transport Planning", "yearsExp": 16, "location": "Chittagong", "hourlyRate": 74, "availability": "Busy"},
    {"id": 20, "name": "Lamiya Haque", "age": 30, "expertise": "Policy Analysis", "yearsExp": 7, "location": "Dhaka", "hourlyRate": 52, "availability": "Available"},
    {"id": 21, "name": "Shafayat Khan", "age": 46, "expertise": "Water Resources", "yearsExp": 18, "location": "Rajshahi", "hourlyRate": 77, "availability": "Busy"},
    {"id": 22, "name": "Nafisa Karim", "age": 34, "expertise": "Behavioral Research", "yearsExp": 10, "location": "Dhaka", "hourlyRate": 59, "availability": "Available"},
    {"id": 23, "name": "Badiul Alam", "age": 53, "expertise": "Governance Reform", "yearsExp": 25, "location": "Dhaka", "hourlyRate": 92, "availability": "Busy"},
    {"id": 24, "name": "Rukhsana Begum", "age": 41, "expertise": "Rural Development", "yearsExp": 15, "location": "Rangpur", "hourlyRate": 61, "availability": "Available"},
    {"id": 25, "name": "Farhan Siddique", "age": 38, "expertise": "Digital Transformation", "yearsExp": 13, "location": "Dhaka", "hourlyRate": 73, "availability": "Available"},
    {"id": 26, "name": "Adnan Chowdhury", "age": 45, "expertise": "Logistics Strategy", "yearsExp": 17, "location": "Dhaka", "hourlyRate": 79, "availability": "Busy"},
    {"id": 27, "name": "Tania Ahmed", "age": 33, "expertise": "Communications Strategy", "yearsExp": 9, "location": "Dhaka", "hourlyRate": 55, "availability": "Available"},
    {"id": 28, "name": "Zarin Tasnim", "age": 28, "expertise": "Data Visualization", "yearsExp": 5, "location": "Dhaka", "hourlyRate": 46, "availability": "Available"},
    {"id": 29, "name": "Omar Faruq", "age": 49, "expertise": "Industrial Policy", "yearsExp": 21, "location": "Chittagong", "hourlyRate": 86, "availability": "Busy"},
    {"id": 30, "name": "Shakil Ahmed", "age": 37, "expertise": "Impact Evaluation", "yearsExp": 12, "location": "Dhaka", "hourlyRate": 64, "availability": "Available"},
    {"id": 31, "name": "Nabila Sultana", "age": 35, "expertise": "Gender & Inclusion", "yearsExp": 10, "location": "Dhaka", "hourlyRate": 58, "availability": "Available"},
    {"id": 32, "name": "Foysal Rahman", "age": 42, "expertise": "Business Strategy", "yearsExp": 15, "location": "Sylhet", "hourlyRate": 71, "availability": "Busy"},
    {"id": 33, "name": "Lubna Karim", "age": 39, "expertise": "Education Technology", "yearsExp": 13, "location": "Dhaka", "hourlyRate": 67, "availability": "Available"},
    {"id": 34, "name": "Ashiqur Rahman", "age": 44, "expertise": "Risk Management", "yearsExp": 16, "location": "Dhaka", "hourlyRate": 75, "availability": "Busy"},
    {"id": 35, "name": "Saima Noor", "age": 31, "expertise": "Health Systems", "yearsExp": 8, "location": "Dhaka", "hourlyRate": 54, "availability": "Available"},
    {"id": 36, "name": "Touhid Islam", "age": 47, "expertise": "Economic Policy", "yearsExp": 20, "location": "Dhaka", "hourlyRate": 83, "availability": "Busy"},
    {"id": 37, "name": "Rashed Ahmed", "age": 36, "expertise": "Market Expansion", "yearsExp": 11, "location": "Chittagong", "hourlyRate": 62, "availability": "Available"},
    {"id": 38, "name": "Fahad Karim", "age": 40, "expertise": "IT Security", "yearsExp": 14, "location": "Dhaka", "hourlyRate": 78, "availability": "Busy"},
    {"id": 39, "name": "Meherun Nessa", "age": 34, "expertise": "NGO Management", "yearsExp": 9, "location": "Khulna", "hourlyRate": 56, "availability": "Available"},
    {"id": 40, "name": "Parvez Alam", "age": 48, "expertise": "Infrastructure Finance", "yearsExp": 19, "location": "Dhaka", "hourlyRate": 87, "availability": "Busy"},
    {"id": 41, "name": "Sabrina Islam", "age": 30, "expertise": "Youth Development", "yearsExp": 7, "location": "Dhaka", "hourlyRate": 49, "availability": "Available"},
    {"id": 42, "name": "Javed Hasan", "age": 46, "expertise": "Trade Policy", "yearsExp": 18, "location": "Dhaka", "hourlyRate": 81, "availability": "Busy"},
    {"id": 43, "name": "Samia Chowdhury", "age": 33, "expertise": "Environmental Policy", "yearsExp": 9, "location": "Dhaka", "hourlyRate": 57, "availability": "Available"},
    {"id": 44, "name": "Muntasir Rahman", "age": 41, "expertise": "Data Engineering", "yearsExp": 15, "location": "Dhaka", "hourlyRate": 76, "availability": "Busy"},
    {"id": 45, "name": "Sharmeen Akter", "age": 35, "expertise": "Community Engagement", "yearsExp": 11, "location": "Barisal", "hourlyRate": 58, "availability": "Available"},
    {"id": 46, "name": "Rakib Hasan", "age": 38, "expertise": "Urban Planning", "yearsExp": 13, "location": "Dhaka", "hourlyRate": 69, "availability": "Busy"},
    {"id": 47, "name": "Dilruba Sultana", "age": 43, "expertise": "Social Protection", "yearsExp": 16, "location": "Rangpur", "hourlyRate": 65, "availability": "Available"},
    {"id": 48, "name": "Tanmoy Das", "age": 29, "expertise": "Digital Marketing", "yearsExp": 6, "location": "Dhaka", "hourlyRate": 47, "availability": "Available"},
    {"id": 49, "name": "Jannatul Ferdous", "age": 32, "expertise": "Monitoring Systems", "yearsExp": 8, "location": "Dhaka", "hourlyRate": 53, "availability": "Available"},
    {"id": 50, "name": "Mahfuz Rahman", "age": 45, "expertise": "Financial Modeling", "yearsExp": 17, "location": "Dhaka", "hourlyRate": 84, "availability": "Busy"},
]


def load_data():
    if not os.path.exists(DATA_FILE):
        save_data(SEED_DATA)
        return SEED_DATA
    with open(DATA_FILE, "r") as f:
        return json.load(f)


def save_data(data):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/consultants", methods=["GET"])
def get_consultants():
    data = load_data()
    return jsonify(data)


@app.route("/api/consultants", methods=["POST"])
def add_consultant():
    body = request.get_json()
    if not body:
        return jsonify({"error": "No data provided"}), 400

    required = ["name", "age", "expertise", "yearsExp", "location", "hourlyRate", "availability"]
    for field in required:
        if field not in body or body[field] == "" or body[field] is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    data = load_data()
    next_id = max((c["id"] for c in data), default=0) + 1

    new_consultant = {
        "id": next_id,
        "name": str(body["name"]).strip(),
        "age": int(body["age"]),
        "expertise": str(body["expertise"]).strip(),
        "yearsExp": int(body["yearsExp"]),
        "location": str(body["location"]).strip(),
        "hourlyRate": float(body["hourlyRate"]),
        "availability": str(body["availability"]),
    }

    data.append(new_consultant)
    save_data(data)
    return jsonify(new_consultant), 201


@app.route("/api/consultants/<int:consultant_id>", methods=["PUT"])
def update_consultant(consultant_id):
    body = request.get_json()
    data = load_data()
    for i, c in enumerate(data):
        if c["id"] == consultant_id:
            data[i].update({k: v for k, v in body.items() if k != "id"})
            save_data(data)
            return jsonify(data[i])
    return jsonify({"error": "Consultant not found"}), 404


@app.route("/api/consultants/<int:consultant_id>", methods=["DELETE"])
def delete_consultant(consultant_id):
    data = load_data()
    new_data = [c for c in data if c["id"] != consultant_id]
    if len(new_data) == len(data):
        return jsonify({"error": "Consultant not found"}), 404
    save_data(new_data)
    return jsonify({"deleted": consultant_id})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
