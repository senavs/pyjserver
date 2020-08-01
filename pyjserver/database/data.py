from typing import KeysView, Any, Union, List
from typing import Mapping


class JSONData:
    _data: dict = None

    def __init__(self, data: Mapping):
        """ JSONData constructor

        :param data: json data as mapping object
            :type Mapping:
        """

        self._data = dict(data)

    @property
    def data(self) -> dict:
        """Getter for original JSON data

        :return dict:
        """

        return self._data

    @property
    def endpoints(self) -> KeysView:
        """Getter for JSON Data endpoint (main json keys)

        :return KeysViwe:
        """

        return self.data.keys()

    def is_valid_id(self, endpoint: str, identifier: int) -> bool:
        """Validate ID for an endpoint. The ID must be greater than 0 and not in endpoint array

        :param endpoint: main json key
            :type str:
        :param identifier: record ID
            :type int:

        :return bool:
        """

        if identifier > 0:
            return not self.select(endpoint, identifier)
        return False

    def validate_id(self, endpoint: str, identifier: int):
        """Verify if the ID is valid and raise if is not

        :raise ValueError:
        """

        if not self.is_valid_id(endpoint, identifier):
            raise ValueError(f'id {identifier} is already in database')

    @classmethod
    def validate_data(cls, data: dict):
        """Validate JSON data schema"""

        raise NotImplementedError()

    def last_inserted_id(self, endpoint: str) -> int:
        """Get the last inserted ID in an endpoint

        :param endpoint: json main key

        :return int:
        """

        return max((record.get('id') for record in self[endpoint]), default=0)

    def _set_id(self, endpoint: str, value: dict) -> dict:
        """Set ID for new record data

        :param endpoint: json main key
            :type str:
        :param value: record data
            :type dict:

        :return dict: same dictionary with ID key
        """

        value = dict(value)
        if not value.get('id'):
            value['id'] = self.last_inserted_id(endpoint) + 1
        else:
            self.validate_id(endpoint, value.get('id'))
        return value

    def select(self, endpoint: str = None, identifier: int = None) -> Union[dict, List[dict]]:
        """Search record in JSON data

        To get all json data: endpoint == None and identifier == None
        To get all json data in an endpoint: endpoint != None and identifier == None
        To get one record data in an endpoint: endpoint != None and identifier != None

        :param endpoint: main json key
            :type str:
            :optional:
        :param identifier: record ID
            :type dict:
            :optional: endpoint must be declared to declare identifier

        :return dict: if identifier is not None
        :return List[dict]: if identifier is None
        """

        # get all json data
        if not endpoint:
            return self.data

        # get all json data from an endpoint
        if not identifier:
            if not endpoint:
                raise ValueError(f'specify endpoint for select an ID')
            return self.data[endpoint]

        # get one record json data. {} if none was found
        try:
            return list(filter(lambda x: x.get('id') == identifier, self.data[endpoint]))[0]
        except IndexError:
            return {}

    def insert(self, endpoint: str, value: dict) -> dict:
        """Insert new record data to endpoint

        :param endpoint: main json key
            :type str:
        :param value: new record data:
            :type dict:

        :return dict: inserted record with ID key
        """

        value = self._set_id(endpoint, value)
        self[endpoint].append(value)
        return value

    def update(self, endpoint: str, identifier: int, value: dict) -> dict:
        """Update record data

        If identifier not in endpoint, it will be created

        :param endpoint: main json key
            :type str:
        :param identifier: record ID to update
            :type int:
        :param value: new record data:
            :type dict:

        :return dict: updated record
        """

        record = self.select(endpoint, identifier)
        value.update(id=identifier)

        if not record:
            self.insert(endpoint, value)
        else:
            record.update(**value)

        return record

    def delete(self, endpoint: str, identifier: int) -> bool:
        """Delete record json data

        :param endpoint: main json key
            :type str:
        :param identifier: record ID to remove
            :type int:

        :return bool: if was deleted
        """

        result = self.select(endpoint, identifier)
        if result:
            self[endpoint] = [record for record in self[endpoint] if result != record]
            return True
        return False

    def copy(self) -> 'JSONData':
        """Get an object copy

        :return JSONData:
        """

        return type(self)(self.data)

    def __iter__(self):
        return iter(self)

    def __getitem__(self, item) -> Any:
        return self.data[item]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __repr__(self):
        return f'{type(self).__qualname__}({self.data})'
