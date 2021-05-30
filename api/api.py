import flask

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    response = flask.Response("Test")
    response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
    return response


app.run()
