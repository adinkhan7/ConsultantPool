import os
import psycopg2
import psycopg2.extras
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)


@app.after_request
def add_cors(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    return response


# ─── Database connection ────────────────────────────────────────────────────

def get_db():
    """Open a connection using the DATABASE_URL environment variable."""
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        raise RuntimeError("DATABASE_URL environment variable is not set.")
    # Render provides postgres:// but psycopg2 needs postgresql://
    if db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    return psycopg2.connect(db_url, cursor_factory=psycopg2.extras.RealDictCursor)


# ─── Schema + seed ──────────────────────────────────────────────────────────

SEED_DATA = [
    ("Ahsan Rahman", 42, "Data Analytics", 15, "Dhaka", 65, "Available"),
    ("Farzana Kabir", 37, "Public Health", 12, "Chittagong", 60, "Available"),
    ("Mahmud Hasan", 45, "Supply Chain", 18, "Dhaka", 70, "Busy"),
    ("Nusrat Jahan", 33, "Gender Studies", 9, "Rajshahi", 55, "Available"),
    ("Tanvir Alam", 39, "IT Systems", 14, "Dhaka", 75, "Available"),
    ("Rezaul Karim", 51, "Agriculture Policy", 25, "Bogura", 68, "Busy"),
    ("Sadia Islam", 34, "Education Reform", 10, "Dhaka", 58, "Available"),
    ("Arif Chowdhury", 48, "Financial Consulting", 20, "Sylhet", 85, "Busy"),
    ("Tasnim Ahmed", 31, "UX Research", 7, "Dhaka", 50, "Available"),
    ("Kamrul Hasan", 44, "Infrastructure Planning", 16, "Khulna", 72, "Busy"),
    ("Rafiq Ahmed", 52, "Development Economics", 24, "Dhaka", 90, "Available"),
    ("Sharmin Akter", 36, "Nutrition Programs", 11, "Barisal", 57, "Available"),
    ("Imran Hossain", 40, "Market Research", 14, "Dhaka", 62, "Busy"),
    ("Shaila Noor", 29, "Social Research", 6, "Dhaka", 48, "Available"),
    ("Moinul Haque", 47, "Energy Policy", 19, "Dhaka", 82, "Busy"),
    ("Fahmida Sultana", 35, "Climate Adaptation", 11, "Khulna", 63, "Available"),
    ("Ziaur Rahman", 50, "Project Management", 22, "Dhaka", 88, "Busy"),
    ("Tamanna Rahman", 32, "Monitoring & Evaluation", 8, "Dhaka", 56, "Available"),
    ("Hasan Mahmud", 43, "Transport Planning", 16, "Chittagong", 74, "Busy"),
    ("Lamiya Haque", 30, "Policy Analysis", 7, "Dhaka", 52, "Available"),
    ("Shafayat Khan", 46, "Water Resources", 18, "Rajshahi", 77, "Busy"),
    ("Nafisa Karim", 34, "Behavioral Research", 10, "Dhaka", 59, "Available"),
    ("Badiul Alam", 53, "Governance Reform", 25, "Dhaka", 92, "Busy"),
    ("Rukhsana Begum", 41, "Rural Development", 15, "Rangpur", 61, "Available"),
    ("Farhan Siddique", 38, "Digital Transformation", 13, "Dhaka", 73, "Available"),
    ("Adnan Chowdhury", 45, "Logistics Strategy", 17, "Dhaka", 79, "Busy"),
    ("Tania Ahmed", 33, "Communications Strategy", 9, "Dhaka", 55, "Available"),
    ("Zarin Tasnim", 28, "Data Visualization", 5, "Dhaka", 46, "Available"),
    ("Omar Faruq", 49, "Industrial Policy", 21, "Chittagong", 86, "Busy"),
    ("Shakil Ahmed", 37, "Impact Evaluation", 12, "Dhaka", 64, "Available"),
    ("Nabila Sultana", 35, "Gender & Inclusion", 10, "Dhaka", 58, "Available"),
    ("Foysal Rahman", 42, "Business Strategy", 15, "Sylhet", 71, "Busy"),
    ("Lubna Karim", 39, "Education Technology", 13, "Dhaka", 67, "Available"),
    ("Ashiqur Rahman", 44, "Risk Management", 16, "Dhaka", 75, "Busy"),
    ("Saima Noor", 31, "Health Systems", 8, "Dhaka", 54, "Available"),
    ("Touhid Islam", 47, "Economic Policy", 20, "Dhaka", 83, "Busy"),
    ("Rashed Ahmed", 36, "Market Expansion", 11, "Chittagong", 62, "Available"),
    ("Fahad Karim", 40, "IT Security", 14, "Dhaka", 78, "Busy"),
    ("Meherun Nessa", 34, "NGO Management", 9, "Khulna", 56, "Available"),
    ("Parvez Alam", 48, "Infrastructure Finance", 19, "Dhaka", 87, "Busy"),
    ("Sabrina Islam", 30, "Youth Development", 7, "Dhaka", 49, "Available"),
    ("Javed Hasan", 46, "Trade Policy", 18, "Dhaka", 81, "Busy"),
    ("Samia Chowdhury", 33, "Environmental Policy", 9, "Dhaka", 57, "Available"),
    ("Muntasir Rahman", 41, "Data Engineering", 15, "Dhaka", 76, "Busy"),
    ("Sharmeen Akter", 35, "Community Engagement", 11, "Barisal", 58, "Available"),
    ("Rakib Hasan", 38, "Urban Planning", 13, "Dhaka", 69, "Busy"),
    ("Dilruba Sultana", 43, "Social Protection", 16, "Rangpur", 65, "Available"),
    ("Tanmoy Das", 29, "Digital Marketing", 6, "Dhaka", 47, "Available"),
    ("Jannatul Ferdous", 32, "Monitoring Systems", 8, "Dhaka", 53, "Available"),
    ("Mahfuz Rahman", 45, "Financial Modeling", 17, "Dhaka", 84, "Busy"),
]


def init_db():
    """Create the table if it doesn't exist, then seed it if empty."""
    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS consultants (
            id           SERIAL PRIMARY KEY,
            name         TEXT         NOT NULL,
            age          INTEGER      NOT NULL,
            expertise    TEXT         NOT NULL,
            years_exp    INTEGER      NOT NULL,
            location     TEXT         NOT NULL,
            hourly_rate  NUMERIC(8,2) NOT NULL,
            availability TEXT         NOT NULL DEFAULT 'Available'
        );
    """)

    cur.execute("SELECT COUNT(*) FROM consultants;")
    count = cur.fetchone()["count"]

    if count == 0:
        cur.executemany("""
            INSERT INTO consultants
                (name, age, expertise, years_exp, location, hourly_rate, availability)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, SEED_DATA)

    conn.commit()
    cur.close()
    conn.close()


def row_to_dict(row):
    """Convert a DB row to the JSON shape the frontend expects."""
    return {
        "id":           row["id"],
        "name":         row["name"],
        "age":          row["age"],
        "expertise":    row["expertise"],
        "yearsExp":     row["years_exp"],
        "location":     row["location"],
        "hourlyRate":   float(row["hourly_rate"]),
        "availability": row["availability"],
    }


# ─── Routes ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/consultants", methods=["GET"])
def get_consultants():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM consultants ORDER BY id;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify([row_to_dict(r) for r in rows])


@app.route("/api/consultants", methods=["POST"])
def add_consultant():
    body = request.get_json()
    if not body:
        return jsonify({"error": "No data provided"}), 400

    required = ["name", "age", "expertise", "yearsExp", "location", "hourlyRate", "availability"]
    for field in required:
        if field not in body or body[field] == "" or body[field] is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO consultants
            (name, age, expertise, years_exp, location, hourly_rate, availability)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        str(body["name"]).strip(),
        int(body["age"]),
        str(body["expertise"]).strip(),
        int(body["yearsExp"]),
        str(body["location"]).strip(),
        float(body["hourlyRate"]),
        str(body["availability"]),
    ))
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(row_to_dict(new_row)), 201


@app.route("/api/consultants/<int:consultant_id>", methods=["PUT"])
def update_consultant(consultant_id):
    body = request.get_json()
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        UPDATE consultants SET
            name         = COALESCE(%s, name),
            age          = COALESCE(%s, age),
            expertise    = COALESCE(%s, expertise),
            years_exp    = COALESCE(%s, years_exp),
            location     = COALESCE(%s, location),
            hourly_rate  = COALESCE(%s, hourly_rate),
            availability = COALESCE(%s, availability)
        WHERE id = %s
        RETURNING *;
    """, (
        body.get("name"),
        body.get("age"),
        body.get("expertise"),
        body.get("yearsExp"),
        body.get("location"),
        body.get("hourlyRate"),
        body.get("availability"),
        consultant_id,
    ))
    updated = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not updated:
        return jsonify({"error": "Consultant not found"}), 404
    return jsonify(row_to_dict(updated))


@app.route("/api/consultants/<int:consultant_id>", methods=["DELETE"])
def delete_consultant(consultant_id):
    conn = get_db()
    cur = conn.cursor()
    cur.execute("DELETE FROM consultants WHERE id = %s RETURNING id;", (consultant_id,))
    deleted = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    if not deleted:
        return jsonify({"error": "Consultant not found"}), 404
    return jsonify({"deleted": consultant_id})


# ─── Startup ─────────────────────────────────────────────────────────────────
# init_db() runs both when started directly and when gunicorn imports the module

init_db()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
