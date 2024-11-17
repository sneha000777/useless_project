from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib

# Load the model and mood maps
model = joblib.load("gas_air_classifier_model.pkl")

mood_map = {
    "Oxygen": "Refreshing Breeze",
    "Hydrogen": "Featherlight Whiff",
    "Carbon Dioxide": "Heavy Atmosphere",
    "Nitrogen": "Neutral Calm",
    "Helium": "Lighthearted Joy"
}

description_map = {
    "Oxygen": "A crisp, cool breath that whispers through the trees, bringing life to all it touches.",
    "Hydrogen": "A playful puff that floats like laughter, a reminder of the lightness in every breath.",
    "Carbon Dioxide": "A dense, grounding air that lingers, adding a touch of seriousness to the day.",
    "Nitrogen": "The steady, reliable calm that fills the atmosphere, unnoticed but essential.",
    "Helium": "A buoyant spirit, light and free, dancing away without a care."
}

forecast_map = {
    "Refreshing Breeze": "Expect a refreshing breeze tomorrow with hints of a cool, steady atmosphere.",
    "Featherlight Whiff": "Tomorrow's forecast includes a light, feathery whiff—a day for lightness and ease.",
    "Heavy Atmosphere": "Prepare for a heavy atmosphere as dense clouds roll in, grounding the day.",
    "Neutral Calm": "Expect calm and neutral skies, an even, balanced day ahead.",
    "Lighthearted Joy": "A joyous, lighthearted day with bursts of laughter in the air—perfect for a carefree afternoon."
}

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    user_data = pd.DataFrame({
        "density": [data["density"]],
        "humidity": [data["humidity"]],
        "temperature": [data["temperature"]],
        "mystery_feature": [data["mystery_feature"]]
    })
    prediction = model.predict(user_data)[0]
    mood = mood_map.get(prediction, "Unknown Mood")
    description = description_map.get(prediction, "No description available.")
    forecast = forecast_map.get(mood, "Weather forecast unavailable.")
    
    response = {
        "mood": mood,
        "description": description,
        "forecast": forecast
    }
    return jsonify(response)

if __name__ == "__main__":
    app.run(debug=True)
