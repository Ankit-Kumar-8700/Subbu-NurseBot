from flask import Flask, render_template, request, jsonify
import random
import re


from intents import greet,closing_phrases,thankful
from response import greetRes,closeConversationRes,thankfulRes,fallback_responsesRes
from helper import findDrugs,findDrugDisease,findDiseaseRemedies,find_symptoms,findSymptomsDisease
# from spacy.lang.en.stop_words import STOP_WORDS

intents = {
    "diseaseToDrug": r"(medication|medic|drug|treatment|suppressant|relief products|medicine)",
    "remedy": r"(remedy|remedies|home treatment|self treatment|help myself|can i do for|shall i do)",
    "drugToDisease": r"(relevance to|relevant|related|associated|help|used to treat|used for treatment|can i take|to take|consume)",
    # "disease": r"^(disease|medical condition|health issue|health condition|medical issue|problem|illness)$",
    "diseaseToSymptoms": r"(signs of|describe symptom|describe the symptom|usually present|typical manifestations|characteristics of|warning signs|usual traits|cues for identifying|symptoms of|features of|signs for|symptoms for)",
    "symptomsToDisease": r"(behind|signify|hint|possible|match|indicate|imply|suggest|linked to)"
}

def classify_intent(user_input):
    for intent, pattern in intents.items():
        if re.search(pattern, user_input, re.IGNORECASE):
            return intent
    return "unknown"




app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    user_message = request.form['user_message']

    intent=classify_intent(user_message)

    print(intent)

    if intent=="diseaseToDrug":
        return jsonify({'response': findDrugs(user_message)})
    elif intent=="remedy":
        return jsonify({'response': findDiseaseRemedies(user_message)})
    elif intent=="drugToDisease":
        return jsonify({'response': findDrugDisease(user_message)})
    elif intent=="diseaseToSymptoms":
        return jsonify({'response': find_symptoms(user_message)})
    elif intent=="symptomsToDisease":
        return jsonify({'response': findSymptomsDisease(user_message)})
    else:
        for i in greet:
            if i.lower() in user_message.lower():
                return jsonify({'response': random.choice(greetRes[i])})
            
        for i in closing_phrases:
            if i.lower() in user_message.lower():
                return jsonify({'response': random.choice(closeConversationRes)})
            
        for i in thankful:
            if i.lower() in user_message.lower():
                return jsonify({'response': random.choice(thankfulRes)})
    
    return jsonify({'response': random.choice(fallback_responsesRes)})


if __name__ == '__main__':
    app.run(debug=True)
