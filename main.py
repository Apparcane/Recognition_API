from flask import Flask
from flask_restful import Api, Resource, reqparse
import random
from stt import recognite

import vosk
import json
import wave

app = Flask(__name__)
api = Api(app)

# http://localhost:8000

ai_quotes = [
    {
        "id": 0,
        "author": "Kevin Kelly",
        "quote": "The business plans of the next 10,000 startups are easy to forecast: " +
                 "Take X and add AI."
    }
]

class Quote(Resource):
    def get(self, id=0):
        if id == 0:
            return random.choice(ai_quotes), 200
        for quote in ai_quotes:
            if(quote["id"] == id):
                return quote, 200
        return "Quote not found", 404
    
    def post(self, id):
      parser = reqparse.RequestParser()
      parser.add_argument("author")
      parser.add_argument("quote")
      params = parser.parse_args()
      for quote in ai_quotes:
          if(id == quote["id"]):
              return f"Quote with id {id} already exists", 400
      quote = {
          "id": int(id),
          "author": params["author"],
          "quote": params["quote"]
      }
      ai_quotes.append(quote)
      return quote, 201
  
    def put(self, id):
        parser = reqparse.RequestParser()
        parser.add_argument("author")
        parser.add_argument("quote")
        params = parser.parse_args()
        for quote in ai_quotes:
            if(id == quote["id"]):
                quote["author"] = params["author"]
                quote["quote"] = params["quote"]
                return quote, 200
        
        quote = {
            "id": id,
            "author": params["author"],
            "quote": params["quote"]
        }
        
        ai_quotes.append(quote)
        return quote, 201
    
    def delete(self, id):
      global ai_quotes
      ai_quotes = [qoute for qoute in ai_quotes if qoute["id"] != id]
      return f"Quote with id {id} is deleted.", 200
  
  
class Recognite(Resource):
    def get(self, file):
        # return recognite(file), 201
        model = vosk.Model("model_small")
        vosk.SetLogLevel(-1)
        samplerate = 16000
        rec = vosk.KaldiRecognizer(model, samplerate)

        file = wave.open(file, "rb")
        data = file.readframes(file.getnframes())
            
        #Recognition
        rec.AcceptWaveform(data)
        result = json.loads(rec.FinalResult())
            
        return result['text']
    
    
api.add_resource(Quote, "/ai-quotes", "/ai-quotes/", "/ai-quotes/<int:id>")
api.add_resource(Recognite, "/recognite", "/recognite/", "/recognite/<file>")

if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    


# @app.route("/", methods=['GET'])
# def hello():
#     return "Hello!"

# # @app.route('/recognition')
# # def recognition(file):
# #     return recognite(file)

# if __name__ == "__main__":
#     # app.debug = True
#     app.run(host='0.0.0.0', port=8000)