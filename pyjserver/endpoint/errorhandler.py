from flask import jsonify


def make_errorhandler():
    """Flask error handler factory"""

    return lambda e: (jsonify(message=str(e)), e.code)
