import spacy
import random
import pandas as pd
import numpy as np
import json
import joblib

nlp = spacy.load("en_core_web_lg")
# # from spacy.lang.en.stop_words import STOP_WORDS

def preprocess(text):
  doc=nlp(text)
  no_stop_words=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
  return ' '.join(no_stop_words)

def preprocessList(text):
  doc=nlp(text)
  no_stop_words=[token.lemma_ for token in doc if not token.is_stop and not token.is_punct and not token.is_space]
  return no_stop_words







diseaseToDrug=pd.read_csv("diseaseToDrug.csv")
drugToDisease=pd.read_csv("drugToDisease.csv")

diseaseToDrug_diseases=diseaseToDrug['disease']
drugToDisease_drugs=drugToDisease['drug']

def findDrugsHelper(disease):
    return " ".join(diseaseToDrug[diseaseToDrug['disease']==disease]['drug'])

def findDrugs(query):
  for i in diseaseToDrug_diseases:
        if i.lower() in query.lower():
            return random.choice(["Medications prescribed for "+i+" are "+", "+findDrugsHelper(i),
              "You can use "+findDrugsHelper(i)+" for "+i,
              "The medicines "+findDrugsHelper(i)+" are effective in "+i,
              "If you have "+i+" disease, then "+", "+findDrugsHelper(i)+" can help.",
              i+" sufferers may find relief via "+findDrugsHelper(i)])
  return "Sorry, we don't have enough data about your disease. Kindly consult a doctor.."

def findDrugDiseaseHelper(drug):
    return " ".join(drugToDisease[drugToDisease['drug']==drug]['disease'])

def findDrugDisease(query):
  for i in drugToDisease_drugs:
        if i.lower() in query.lower():
            return random.choice([i+" is commonly prescribed for "+findDrugDiseaseHelper(i),
              "You can use "+i+" for "+findDrugDiseaseHelper(i),
              findDrugDiseaseHelper(i)+" are often treated with "+i,
              "If you have "+findDrugDiseaseHelper(i)+" disease, then you can take "+i,
              i+" can be helpful to you in case of "+findDrugDiseaseHelper(i)])
  return "Sorry, we don't have enough data about this medic. Kindly check the spelling and try again. If problem persists, kindly consult a medic/doctor.."

# print(findDrugDisease("can you tell me what diseases are related to clobazam"))

# print(findDrugs("I want to know the medications for Asthma"))








diseaseToRemedy=open("diseaseRemedy.json")
diseaseToRemedy=json.load(diseaseToRemedy)["intents"]

def findDiseaseRemedies(text):
    for i in diseaseToRemedy:
        for j in i['patterns']:
            if j.lower() in text.lower() or text.lower() in j.lower():
                return " . ".join(i["responses"])
        if i['tag'].lower() in text:
            return " . ".join(i["responses"])
        
    return "Sorry, but i don't have much idea about this one.."

# print(findDiseaseRemedies("my hand was cut down"))








diseaseSymptoms=pd.read_csv("diseaseSymptoms.csv")

def find_symptoms_helper(query):
  tokens=preprocessList(query)

  for i in tokens:
    if diseaseSymptoms['label'].str.contains(fr'\b{i}\b', regex=True).any():
      for j in diseaseSymptoms['label']:
        if i in j:
          temp=diseaseSymptoms[diseaseSymptoms['label']==j].drop(columns="label",axis=1)
          symptoms=" , ".join(temp.columns[temp.iloc[0] == 1])
          # print(i,j)
          return symptoms,j
        
  return "",""

def find_symptoms(query):
  symptoms,disease=find_symptoms_helper(query)
  if symptoms=="":
    return "Sorry, but our dataset doesn't has info about the disease you mentioned. You can try using another synonym of the disease you mentioned."
  return random.choice([
    "Symptoms associated with "+disease+" include "+symptoms,
    "Common signs of "+disease+" encompass "+symptoms,
    disease+" is characterized by "+symptoms,
    "The following symptoms "+symptoms+" are indicative of "+disease,
    disease+" typically manifests with "+symptoms,
    "Recognizable indicators of "+disease+" involve "+symptoms,
    symptoms+" are the symptoms commonly linked to "+disease,
    "One can identify "+disease+" by "+symptoms,
    "The presence of "+symptoms+" often signifies "+disease
  ])

# print(find_symptoms("diabetes"))










scaler=joblib.load("minMaxScaler")
model=joblib.load("symptomToDisease")
symptomToDiseaseDF=joblib.load("symptomToDiseaseDF")

def findSymptomsDisease(query):
    preProcessed_query=preprocess(query)
    vector_query=[nlp(preProcessed_query).vector]

    test_df=pd.DataFrame([vector_query],columns=['vector'])

    test_df_2d=np.stack(test_df['vector'])

    try:
      test_df_scaled=scaler.transform(test_df_2d)

      ans=model.predict(test_df_scaled)

      dict_df=symptomToDiseaseDF[['label','label_num']].drop_duplicates(subset=['label', 'label_num'])
      disease="".join(dict_df[dict_df['label_num']==ans[0]]['label'])

      return random.choice(["Based on the presented symptoms, it appears to be indicative of "+disease+".",
      "The symptoms you've described are suggestive of "+disease+".",
      "These symptoms are consistent with the diagnosis of "+disease+".",
      "The observed signs point to the presence of "+disease+" ailment.",
      "It seems that the symptoms align with the diagnosis of "+disease+".",
      "From the symptoms you've mentioned, it's likely to be "+disease+" condition.",
      "The symptoms strongly correlate with the presence of "+disease+".",
      "From what you've described, it's probable that you have "+disease+".",
      "These clinical manifestations are characteristic of "+disease+" health issue."])
    
    except:
       return "Sorry, i am unable to diagnose your symptoms. It will be best if you see a clinic or a medical lab.."

# print(findSymptomsDisease("i am suffering from fever, have some cough and body pain."))