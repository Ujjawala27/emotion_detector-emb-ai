"""Flask application for emotion detection."""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detector")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detect():
    """Handle emotion detection requests and return the system response."""
    # Read input from either query string (GET) or JSON (POST)
    if request.method == "GET":
        text_to_analyze = request.args.get("textToAnalyze")
    else:
        data = request.get_json(silent=True) or {}
        text_to_analyze = data.get("statement") or data.get("textToAnalyze")

    # Blank input -> required message
    if text_to_analyze is None or text_to_analyze.strip() == "":
        return "Invalid text! Please try again!.", 200

    result = emotion_detector(text_to_analyze)

    # dominant_emotion None -> required message
    if result.get("dominant_emotion") is None:
        return "Invalid text! Please try again!.", 200

    anger = result["anger"]
    disgust = result["disgust"]
    fear = result["fear"]
    joy = result["joy"]
    sadness = result["sadness"]
    dominant_emotion = result["dominant_emotion"]

    return (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant_emotion}."
    ),200


@app.route("/")
def render_index_page():
    """Render the home page."""
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
