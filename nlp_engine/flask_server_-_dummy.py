from flask import Flask

## Refer - https://www.analyticsvidhya.com/blog/2017/09/machine-learning-models-as-apis-using-flask/
## Refer - https://projects.raspberrypi.org/en/projects/python-web-server-with-flask/2

app = Flask(__name__) 
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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    ## host='0.0.0.0' is the localhost

