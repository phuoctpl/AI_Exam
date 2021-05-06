import flask
from services import craw_data_tgdd

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    return craw_data_tgdd.get_data()


app.run()
