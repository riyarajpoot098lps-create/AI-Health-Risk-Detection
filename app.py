from flask import Flask, render_template, request, jsonify
import pickle
from google import genai   # ✅ correct import

# ---------- GEMINI SETUP ----------
client = genai.Client(api_key="AIzaSyD46LLYgo6bxBRlul9tW1fz0Q0INuMLTVQ")  # ⚠️ replace

app = Flask(__name__)

# ---------- LOAD MODEL ----------
model = pickle.load(open("diabetes_model.pkl", "rb"))

# ---------- HOME ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- PREDICT ----------
@app.route("/predict", methods=["POST"])
def predict():
    try:
        age = int(request.form["age"])
        weight = float(request.form["weight"])
        height = float(request.form["height"])
        bp = float(request.form["bp"])
        smoking = request.form["smoking"]

        bmi = round(weight / ((height / 100) ** 2), 2)

        input_data = [[0,120,bp,20,80,bmi,0.5,age]]
        prediction = model.predict(input_data)

        diabetes = ("High", 80) if prediction[0] == 1 else ("Low", 30)
        heart = ("High", 75) if smoking == "Yes" else ("Medium", 40)
        bp_risk = ("High", 85) if bp > 140 else ("Low", 30)

        return render_template(
            "result.html",
            diabetes=diabetes,
            heart=heart,
            bp=bp_risk,
            bmi=bmi
        )

    except Exception as e:
        return f"Error: {e}"

# ---------- CHATBOT ----------
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json['message'].lower()

    # 🔥 SMART LOGIC
    if "bp" in user_msg or "pressure" in user_msg:
        reply = "To reduce BP:\n- Reduce salt\n- Exercise daily\n- Avoid stress\n- Check BP regularly"

    elif "diabetes" in user_msg or "sugar" in user_msg:
        reply = "For diabetes control:\n- Avoid sugar\n- Eat healthy\n- Exercise\n- Monitor glucose"

    elif "heart" in user_msg or "chest" in user_msg:
        reply = "Heart care tips:\n- Daily exercise\n- No smoking\n- Healthy diet\n- Regular checkups"

    elif "walk" in user_msg:
        reply = "Yes! Walking daily improves heart health, fitness, and mood."

    elif "weight" in user_msg:
        reply = "To reduce weight:\n- Eat less junk food\n- Exercise daily\n- Stay hydrated"

    elif "diet" in user_msg:
        reply = "Healthy diet includes:\n- Fruits\n- Vegetables\n- Low sugar\n- Balanced meals"

    else:
        reply = "Stay healthy by eating well, exercising, and sleeping properly."

    return jsonify({'reply': reply})

# ---------- RUN ----------
if __name__ == "__main__":
    app.run(debug=True)