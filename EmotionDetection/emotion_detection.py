import requests, json

def emotion_detector(text_to_analyze):
    url = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
    myobj = {"raw_document": {"text": text_to_analyze}}
    header = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

    r = requests.post(url, json=myobj, headers=header)

    result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    if r.status_code != 200:
        return result

    formatted_response = json.loads(r.text)

    # Extract the required emotions + scores
    prediction = formatted_response.get("emotionPredictions", [{}])[0]
    emotions = prediction.get("emotion", {})

    anger_score = emotions.get("anger")
    disgust_score = emotions.get("disgust")
    fear_score = emotions.get("fear")
    joy_score = emotions.get("joy")
    sadness_score = emotions.get("sadness")

    result['anger'] = anger_score
    result['disgust'] = disgust_score
    result['fear'] = fear_score
    result['joy'] = joy_score
    result['sadness'] = sadness_score

    # Find dominant emotion (highest score)
    scores = {
        "anger": anger_score,
        "disgust": disgust_score,
        "fear": fear_score,
        "joy": joy_score,
        "sadness": sadness_score
    }

    available_scores = {k: v for k, v in scores.items() if v is not None}
    if available_scores:
        result['dominant_emotion'] = max(available_scores, key=available_scores.get)

    return result