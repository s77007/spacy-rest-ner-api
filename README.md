# spacy-rest-ner-api
REST API library to query SpaCy objects for NLP

This app is an simple implementation of REST ful service using:
Flask and Flask_Restful 
Spacy

NOTE:
Code is provided for demonstration purposes only and does not cover security and data governance aspects.
Flask server is set to run in "debug" mode so a user can monitor activities during development and testing. 
This code should not be used for Production deployment.

Pre installation Requirements:
Install Python 3.7 or above

Open command prompt/terminal window and run following commands
>pip install spacy
>spacy download en_core_web_sm
>pip install flask
>pip install flask_restful

Based on the information, i have constructed basic API model that can be expanded further to implement
- various filters 

• A list of assumptions you made :
- This API will receive a line of text 
- Service will return entity object serialised as json object to client application

• A short description of interesting parts of your code 
Implemented service using flask which provides simple micro service framework to implement API 
Code demonstrate use of pandas dataframe to build data frame based on tokens data.
This can be used for in-memory computation/calculations to improve processing speed. 
Code contains comments for future improvements based on application requirements - Scalability, availability, cost-time vs accuracy etc.


• A short description of potential improvements
I have used AWS infrastructure with AWS Lambda however Natural language processing may stretch lambda too far.
Probably we can still use AWS infrastructure to host application as a container and also use other services efficiently:
Client Authorisation can be improved by using AWS cognito along with S3 to store trained models as well as predicted result sets to be analysed by data scientists.

