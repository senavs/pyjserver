from flask import Flask, Blueprint

from .errorhandler import make_errorhandler
from .methods import make_default_method, make_crud_method
from ..database.connector import Connector


class Endpoint:
    _app: Flask = None
    _db_file_path: str = None

    def __init__(self, name: str, *, db_file_path: str):
        """Endpoint constructor

        :param name: endpoint name
            :type str:

        :param db_file_path: json data file path
            :type str:
        """

        self._app = Flask(name)
        self._db_file_path = str(db_file_path)

        self._register_default()
        self._register_crud()
        self._register_errorhandler()

    @property
    def endpoints(self) -> list:
        """Getter for all json data main keys (endpoints)

        :return list:
        """

        with Connector(self._db_file_path) as conn:
            return list(conn.json_data.endpoints)

    def _register_default(self):
        """Function to register all default pages (pages that will be created independent of json data file)"""

        self._app.add_url_rule('/', 'homepage', make_default_method(self.endpoints, method='homepage'))

    def _register_crud(self):
        """Function to register all dynamic pages (pages that will be created based on json data file)"""

        for endpoint in self.endpoints:
            blueprint = Blueprint(endpoint, endpoint, url_prefix=f'/{endpoint}')

            blueprint.add_url_rule('/', 'get-all', make_crud_method(self._db_file_path, endpoint, method='get'), methods=['GET'])
            blueprint.add_url_rule('/<int:identifier>', 'get-one', make_crud_method(self._db_file_path, endpoint, method='get'), methods=['GET'])
            blueprint.add_url_rule('/', 'post-one', make_crud_method(self._db_file_path, endpoint, method='post'), methods=['POST'])
            blueprint.add_url_rule('/<int:identifier>', 'put-one', make_crud_method(self._db_file_path, endpoint, method='put'), methods=['PUT'])
            blueprint.add_url_rule('/<int:identifier>', 'delete-one', make_crud_method(self._db_file_path, endpoint, method='delete'), methods=['DELETE'])

            self._app.register_blueprint(blueprint)

    def _register_errorhandler(self):
        """Function to register all flask error handlers"""

        for code in [400, 401, 403, 404, 405, 500, 501, 502, 503]:
            self._app.register_error_handler(code, make_errorhandler())

    def run(self, host: str = 'localhost', port: int = 5000, debug: bool = False):
        """Start flask server

        :param host: application host IP
            :type str:
            :default: 'localhost'
        :param port: application port
            :type int:
            :default: 5000
        :param debug: application debug
            :type bool:
            :default: False
        """

        self._app.run(host, port, debug)
