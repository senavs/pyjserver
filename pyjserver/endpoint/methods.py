from typing import MutableSequence, Callable

from flask import jsonify, request
from werkzeug.exceptions import NotFound, BadRequest

from ..database.connector import Connector


def make_default_method(endpoints: MutableSequence, *, method: str) -> Callable:
    """HTTP method for default pages

    :param endpoints: all endpoints
        :type MutableSequence:
    :param method: function/method name
        :type str:

    :return Callable:
    """

    def homepage():
        response = {'endpoints': [], 'methods': ['GET', 'POST', 'PUT', 'DELETE']}
        for endpoint in endpoints:
            response['endpoints'].append({'name': endpoint, 'route': f'/{endpoint}'})
        return jsonify(response), 200

    return locals()[method]


def make_crud_method(conn_file_path: str, endpoint: str, *, method: str) -> Callable:
    """CRUD HTTP method factory

    :param conn_file_path: .json data file path
        :type str:
    :param endpoint: which endpoint this function will be
        :type str:
    :param method: function/method name
        :type str:

    :return Callalble:
    """

    def get(identifier: int = None):
        with Connector(conn_file_path) as conn:
            result = conn.json_data.select(endpoint, identifier)
            if identifier and not result:
                raise NotFound(f'id {identifier} not found')
        return jsonify(result), 200

    def post():
        with Connector(conn_file_path) as conn:
            try:
                result = conn.json_data.insert(endpoint, request.get_json(force=True))
            except ValueError as err:
                raise BadRequest(str(err))
        return jsonify(result), 201

    def put(identifier: int):
        with Connector(conn_file_path) as conn:
            result = conn.json_data.update(endpoint, identifier, request.get_json(force=True))
        return jsonify(result), 200

    def delete(identifier: int):
        with Connector(conn_file_path) as conn:
            conn.json_data.delete(endpoint, identifier)
        return jsonify({}), 200

    return locals()[method]
