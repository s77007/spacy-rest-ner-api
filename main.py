import sys
import spacy
import json
import uuid

import pandas as pd

from flask import Flask
from flask_restful import Api, Resource

#new flask app
app = Flask(__name__)

#wrap in an api
api = Api(app)

#API improvements
#Would require full implementation of user authorisation for payload/data security.
#use requestparser to validate request data

#** Service improvements **
#Based on app/user requirements, API can be enhanced to provide functionality such as :
# Analyze multiple texts
# Analyze text from a file (S3 bucket etc.)
# Specify various filters : Language, entity type of interest


#Any other configuration options e.g.:
# Trained model to load for nlp
# additional rulers to specify for matching

#Error handling from api can be improved

#Objective
#An endpoint that accepts an unstructured text of any language, and
#returns a list of named entities recognised by Spacy

#Function to build standard json response for consistency
def buildResponse (ValidEntities):
    jsonStr ="{"
    for entity in ValidEntities:
        print(entity.text, entity.label_)
        jsonStr = jsonStr + "\"" + entity.label_ + "\""   + ":" + "\"" + entity.text + "\"" + ","

    jsonStr = jsonStr[:-1] + "}"

    return jsonStr


class analyzetext(Resource):
    #get implementation
    def get(self,rawtext):
        # Can store text data and results to database for anomaly detection later
        return {"UnStructdata":rawtext}

    #implement post method for security and overcome text limits of GET
    def post(self,rawtext):
        try:
            #Unique API request identifier
            reqid = (uuid.uuid4())
            #Load spacy model
            nlp = spacy.load("en_core_web_sm")
            #Generate doc object
            doc = nlp(rawtext)
            #Check if valid Entities object was created
            if((len(doc.ents)) >0):
                #pandas dataframe implementation to extract key object values
                #Column definition for dataframe
                columns = ("RequestId","text","tag", "lemma", "POS", "explain", "stopword")
                tokensdata = []
                for token in doc:
                    tokendata = [str(reqid)[-5:],token.text,token.tag_, token.lemma_, token.pos_, spacy.explain(token.pos_), token.is_stop]
                    tokensdata.append(tokendata)
                tokendf = pd.DataFrame(tokensdata, columns=columns)
                print(tokendf)

                #data frame can be pushed to database if needed
                #Save the successful document for processing later
                #Could save to S3 bucket in AWS environment
                doc.to_disk("./gooddoc")
                #Alternatively Save data to database local or aws dynamodb etc.
                response = buildResponse(doc.ents)
            else:
                #Bad text or text that did not generate entities object, return application error
                doc.to_disk("./faileddoc")
                response = ({"AppErrorMsg":"No entities found"})
            return response,  200
        except Exception as serviceexception:
            #Any other errors should be handled as API Infrastructure errors
            print("Something went very wrong - " , serviceexception)
            response = ({"AppErrorMsg":"API error please check the payload/text"})
            return response, 404

#define and register the Resource to API
api.add_resource(analyzetext,"/analyzetext/<string:rawtext>")

if __name__ == "__main__":
    #app.run(debug=True)
    app.run(debug=True, host="127.0.0.1", port="5000")
