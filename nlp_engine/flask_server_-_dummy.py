from flask import Flask, request, jsonify
from flask_cors import CORS

## Refer - https://www.analyticsvidhya.com/blog/2017/09/machine-learning-models-as-apis-using-flask/
## Refer - https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/2
## Refer - https://www.youtube.com/results?search_query=machine+learning+model+deployment+using+flask

app = Flask(__name__) 
CORS(app)
## __name__ refers to main

@app.route('/') 
## Route '/' refers to http://127.0.0.1:5000/ i.e localhost
## Can also run localhost pages on devices in the same network. 
## Refer - https://howchoo.com/g/mte2zgrhmjf/how-to-access-a-website-running-on-localhost-from-a-mobile-phone
def index(): ## main webpage
    return 'Hello World'

@app.route('/test/<name>') ## Another webpage 
## http://127.0.0.1:5000/test/<name> e.g http://127.0.0.1:5000/test/Shreyam
def test(name):
    print ("HI") ## prints on console
    return ("Hello {}!".format(name)) ## prints on browser


@app.route('/json_description/<string>', methods=['POST']) ## Webpage which accepts POST json data and also prints the string in url
## http://127.0.0.1:5000/json_description/shrke 
## Refer - http://toolsqa.com/postman/post-request-in-postman/
## Refer - https://stackoverflow.com/questions/20001229/how-to-get-posted-json-in-flask
def json_description(string):
    print ("Hey") ## prints on console
    content = request.json ## request json data from body
    print (content['description']) ## print on console, json data which has"description" as key
    #return jsonify(content) ## prints on browser, json syntax that was POSTed
    return string ## prints on browser


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    ## host='0.0.0.0' is the localhost

