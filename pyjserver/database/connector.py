import json
from json import JSONDecodeError

from .data import JSONData


class Connector:
    _file_path: str = None
    _json_data: 'JSONData' = None

    def __init__(self, file_path: str):
        """Connector constructor

        :param file_path: database file path (.json)
            :type str:
        """

        self._file_path = str(file_path)

    @property
    def file_path(self) -> str:
        """Getter for json data file path

        :return str:
        """

        return self._file_path

    @property
    def json_data(self) -> 'JSONData':
        """Getter for json data

        :return JSONData:
        """

        return self._json_data

    def open(self) -> 'Connector':
        """Open connection (read json file and save to _json_data)

        :return Connector:
        """

        with open(self.file_path, 'r', encoding='utf-8') as file:
            try:
                self._json_data = JSONData(json.load(file))
            except JSONDecodeError:
                raise RuntimeError('json file is empty or json file is incorrect. try https://jsonlint.com/ to validate json schema')
        return self

    def close(self):
        """Close connection (save _json_data to json file)"""

        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(self.json_data.data, file, indent=2)

    def __enter__(self) -> 'Connector':
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_type:
            self.close()


