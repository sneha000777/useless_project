import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("gas_air_data.csv")
X = df.drop(columns="air_type")
y = df["air_type"]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, "gas_air_classifier_model.pkl")

# Mood Mapping (for interpretation)
mood_map = {
    "Oxygen": "Refreshing Breeze",
    "Hydrogen": "Featherlight Whiff",
    "Carbon Dioxide": "Heavy Atmosphere",
    "Nitrogen": "Neutral Calm",
    "Helium": "Lighthearted Joy"
}

# Description Dictionary
description_map = {
    "Oxygen": "A crisp, cool breath that whispers through the trees, bringing life to all it touches.",
    "Hydrogen": "A playful puff that floats like laughter, a reminder of the lightness in every breath.",
    "Carbon Dioxide": "A dense, grounding air that lingers, adding a touch of seriousness to the day.",
    "Nitrogen": "The steady, reliable calm that fills the atmosphere, unnoticed but essential.",
    "Helium": "A buoyant spirit, light and free, dancing away without a care."
}

# Visualization Colors
color_map = {
    "Oxygen": "skyblue",
    "Hydrogen": "pink",
    "Carbon Dioxide": "gray",
    "Nitrogen": "beige",
    "Helium": "lightyellow"
}

# Function to detect "mood" based on user input
def detect_mood(density, humidity, temperature, mystery_feature):
    user_data = pd.DataFrame({
        "density": [density],
        "humidity": [humidity],
        "temperature": [temperature],
        "mystery_feature": [mystery_feature]
    })
    prediction = model.predict(user_data)[0]
    mood = mood_map.get(prediction, "Unknown Mood")
    description = description_map.get(prediction, "No description available.")
    
    print(f"\nDetected Mood: {mood}")
    print(f"Description: {description}")
    visualize_mood(prediction)
    return mood, description

# Function to visualize the "mood"
def visualize_mood(prediction):
    plt.figure(figsize=(2, 2))
    plt.gca().add_patch(plt.Circle((0.5, 0.5), 0.4, color=color_map[prediction]))
    plt.text(0.5, 0.5, prediction, ha="center", va="center", color="black", fontsize=12)
    plt.axis("off")
    plt.title(f"Air Type Visualization: {mood_map[prediction]}")
    plt.show()

# Future Weather Forecast based on the detected mood
def generate_weather_forecast(mood):
    forecast_map = {
        "Refreshing Breeze": "Expect a refreshing breeze tomorrow with hints of a cool, steady atmosphere.",
        "Featherlight Whiff": "Tomorrow's forecast includes a light, feathery whiff—a day for lightness and ease.",
        "Heavy Atmosphere": "Prepare for a heavy atmosphere as dense clouds roll in, grounding the day.",
        "Neutral Calm": "Expect calm and neutral skies, an even, balanced day ahead.",
        "Lighthearted Joy": "A joyous, lighthearted day with bursts of laughter in the air—perfect for a carefree afternoon."
    }
    forecast = forecast_map.get(mood, "Weather forecast unavailable.")
    print(f"\nFuture Weather Forecast: {forecast}")
    return forecast

# Interactive User Input
def interactive_mood_detector():
    print("\nEnter Air Properties for Mood Detection:")
    density = float(input("Density: "))
    humidity = float(input("Humidity (%): "))
    temperature = float(input("Temperature (°C): "))
    mystery_feature = float(input("Mystery Feature: "))
    
    mood, description = detect_mood(density, humidity, temperature, mystery_feature)
    generate_weather_forecast(mood)

# Main
if __name__ == "__main__":
    print("Gas Air Classifier with Creative Features")
    
    # Testing Sample Predictions
    predictions = model.predict(X_test)
    accuracy = accuracy_score(y_test, predictions)
    print(f"Model Accuracy: {accuracy * 100:.2f}%")
    
    # Run interactive mode
    interactive_mood_detector()
