import random
import json

import torch
from Recommendation import NaiveBayes
from model import NeuralNet
from nltk_utils import bag_of_words, tokenize

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

with open(r'intents.json', 'r') as json_data:
    intents = json.load(json_data)
FILE = "data.pth"
data = torch.load(FILE)
symp=[]
input_size = data["input_size"]
hidden_size = data["hidden_size"]
output_size = data["output_size"]
all_words = data['all_words']
tags = data['tags']
model_state = data["model_state"]

model = NeuralNet(input_size, hidden_size, output_size).to(device)
model.load_state_dict(model_state)
model.eval()

bot_name = "Sam"

def get_response(msg):
    #print(msg)
    sentence = tokenize(msg)
    X = bag_of_words(sentence, all_words)
    X = X.reshape(1, X.shape[0])
    X = torch.from_numpy(X).to(device)
    
    output = model(X)
   
    _, predicted = torch.max(output, dim=1)
    tag = tags[predicted.item()]
    #print(tags)
    probs = torch.softmax(output, dim=1)
    prob = probs[0][predicted.item()]
    #print(prob.item())
    if prob.item() > 0.85:
        for intent in intents['intents']:
            if tag == intent["tag"]:
                print(tag)
                if tag=="symptom"or tag=="symptoms":
                    spmsg=msg.replace(" ","_")
                    symp.append(spmsg)
                elif tag=="no":
                    bloc = NaiveBayes(symp)
                    return "May be a Symptom of "+bloc
                elif tag=="clear":
                    symp.clear()
                return random.choice(intent['responses'])
    return "I do not understand... please help me by typing only the symptoms for better understanding"


if __name__ == "__main__":
    print("Let's chat! (type 'quit' to exit)")
    while True:
        #sentence = "do you use credit cards?"
        sentence = input("You: ")
        if sentence == "quit":
            break

        resp = get_response(sentence)
        print(resp)

