from flask import abort, make_response, jsonify
def endpoints_exception(code, msg):
    abort(make_response(jsonify(message=msg), code))
