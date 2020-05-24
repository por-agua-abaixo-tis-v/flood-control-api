from flask import Blueprint, jsonify, request
from flood.utils import query_param_validations, tweepy
import logging
logging.basicConfig(level=logging.INFO)
_logger = logging.getLogger(__name__)

blueprint = Blueprint('twitter', __name__)


@blueprint.route('/twitter', methods=['GET', 'OPTIONS'])
def get_tweets():
    query_param_validations.validate_twitter(request.args)
    return jsonify(tweepy.get_user_timeline_tweets(int(request.args['num']), request.args['user'])), 200