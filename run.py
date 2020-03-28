from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_cors import CORS
import logging
import os

from flood.endpoints.status import blueprint as status_bp
from flood.endpoints.groups import blueprint as groups_bp

_logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)



####################################################################
# Main
####################################################################

@app.route("/")
def hello():
    return "The Horribly Fast Api with Extremely Efficient Endpoints by Lucas Ferreira"

app.register_blueprint(status_bp)
app.register_blueprint(groups_bp)


if __name__ == "__main__":
    app_port = 8080
    try:
        app_port = os.environ['PORT']
    except Exception as e:
        _logger.warning("Running on local environment")

    app.register_blueprint(status_bp)
    app.run(debug=False, port=app_port, host='0.0.0.0', use_reloader=False)