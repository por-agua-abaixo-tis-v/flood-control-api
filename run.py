from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_cors import CORS

from flood.endpoints.status import blueprint as status_bp

app = Flask(__name__)
CORS(app)


####################################################################
# Main
####################################################################

@app.route("/")
def hello():
    return "The Horribly Fast Api with Extremely Efficient Endpoints by Lucas Ferreira"

app.register_blueprint(status_bp)


if __name__ == "__main__":
    app.register_blueprint(status_bp)
    app.run(debug=False, port=8080, host='0.0.0.0', use_reloader=False)