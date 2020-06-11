#!/usr/bin/env python3

from flask import Flask, request, jsonify
from EmoPy.src.fermodel import FERModel
from pkg_resources import resource_filename
from base64 import b64decode

app = Flask(__name__)

@app.route("/")
def hello():
  return "Emotion Server"

@app.route("/image", methods=['POST'])
def image():
  content = request.json
  target_emotions = ['anger', 'calm', 'happiness']
  model = FERModel(target_emotions, verbose=True)
  data_uri = content['image']
  header, encoded = data_uri.split(",", 1)
  image_data = b64decode(encoded) 
  prediction = model.predict(image_data)
  sum = 0
  for i in range(len(prediction[0])):
      sum = sum + prediction[0][i]
  return {"anger": prediction[0][0] / sum, "calm": prediction[0][1] / sum, "happiness": prediction[0][2] / sum}
  #return str(prediction)        
  

if __name__ == "__main__":
  app.run()
