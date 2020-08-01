# Python JSON Server
Python implementation of Node JSON Server (Flask as backend).

![GitHub tag (latest SemVer)](https://img.shields.io/github/v/tag/senavs/pyjserver)
![PyPI](https://img.shields.io/pypi/v/pyjserver)
![PyPI - License](https://img.shields.io/pypi/l/pyjserver)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/pyjserver)

<p align="center">
  <img src="/docs/gif/pyjserver-demonstration.gif" width="50%" alt="demonstraction" />
</p>

## About
Make a full REST API without coding!  
pyjserver is a python implementation of [Node JSON Sever](https://github.com/typicode/json-server), 
which creates a full REST api (with GET, POST, PUT and DELETE methods) based on json file.

## What's Next
- PATCH HTTP method.
- Filter data with GET HTTP method.
- Pagination data with GET HTTP method.

## Install
Python JSON Server library is on PyPi repository, so it can be installed with `pip`.
```sh
>>> pip install pyjserver
```

## Get stated
After install pyjserver, create `db.json` file with the endpoints and data.
```json
{
  "python-libs": [
    {
      "id": 1,
      "name": "pyjserver",
      "version": "1.0.0"
    },
    {
      "id": 2,
      "name": "flask",
      "version": "1.1.0"
    },
    {
      "id": 3,
      "name": "flask-restful",
      "version": "0.3.8"
    }
  ]
}
```

Run the pyjserver cli command.
```sh
>>> python -m pyjserver my-server ./db.json
```
OR
```sh
>>> python3 -m pyjserver my-server ./db.json
```
And the follow output will be displayed:
```
 * Serving Flask app "my-server" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:5000/ (Press CTRL+C to quit)
```

Now to test the API, if you go to http://localhost:5000/python-libs you will get the same json in db.json.
```json
[{"id":1,"name":"pyjserver","version":"1.0.0"},{"id":2,"name":"flask","version":"1.1.0"},{"id":3,"name":"flask-restful","version":"0.3.8"}]
```

With the same URL, you can send POST requests to add, PUT requests to edit and DELETE requests to remove from json file.

`TIP` for each json key, it will be created an endpoint with GET, POST, PUT and DELETE HTTP methods. 
You can also see all available endpoints in root url (http://localhost:5000/).
```json
{
   "endpoints" : [
      {
         "name" : "python-libs",
         "route" : "/python-libs"
      }
   ],
   "methods" : [
      "GET",
      "POST",
      "PUT",
      "DELETE"
   ]
}

```

## JSON file schema
**Format:** JSON object with a list of JSON objects. 

**Main JSON key:** name of the endpoint  
**JSON list value:** list with all records for the endpoint. To start with no data, just place an empty list `[]`  
**JSONs inside the list:** each record for the endpoint. **DO NOT FORGET TO ADD SEQUENTIAL `ID` KEY FOR EACH RECORD**
```json
{
  "endpoint-1": [
    {
      "id": 1,
      "name": "data 01"
    },
    {
      "id": 2,
      "name": "data 02"
    }
  ],
  "endpoint-2": [
    {
      "id": 1,
      "name": "another data 01"
    }
  ],
  "endpoint-3": []
}
```

So the JSON above will create 3 endpoints `/endpoint-1` (with 2 record data), `endpoint-2` (with 1 record data) and `endpoint-3` (with no record data). 
The home page for this json file will display:
```json
{
   "endpoints" : [
      {
         "name" : "endpoint-1",
         "route" : "/endpoint-1"
      },
      {
         "name" : "endpoint-2",
         "route" : "/endpoint-2"
      },
      {
         "name" : "endpoint-3",
         "route" : "/endpoint-3"
      }
   ],
   "methods" : [
      "GET",
      "POST",
      "PUT",
      "DELETE"
   ]
}
```

## HTTP methods
For each endpoint created, is allowed `GET`, `POST`, `PUT` and `DELETE` HTTP method.

  - GET
  ```sh
  >>> curl http://localhost:5000/endpoint-1/
  [{"id":1,"name":"data 01"},{"id":2,"name":"data 02"}]
  ```
  
  - POST
  ```sh
  >>> curl -d '{"name": "data 03"}' -H 'Content-type: application/json' -X POST http://localhost:5000/endpoint-1/
  {"id":3,"name":"data 03"}
  
  >>>  curl http://localhost:5000/endpoint-1/
  [{"id":1,"name":"data 01"},{"id":2,"name":"data 02"},{"id":3,"name":"data 03"}]
  ```

  - PUT
  ```sh
  >>> curl -d '{"name": "data 02 edited"}' -H 'Content-type: application/json' -X PUT http://localhost:5000/endpoint-1/2
  {"id":2,"name":"data 02 edited"}
  
  >>> curl http://localhost:5000/endpoint-1/
  [{"id":1,"name":"data 01"},{"id":2,"name":"data 02 edited"},{"id":3,"name":"data 03"}]
  ```
  
  - DELETE
  ```sh
  >>> curl -X DELETE http://localhost:5000/endpoint-1/2
  {}
  
  >>> curl http://localhost:5000/endpoint-1/
  [{"id":1,"name":"data 01"},{"id":3,"name":"data 03"}]
  ```

**REMEMBER:** all the data is inside the `db.json` file, so any change with the HTTP method it will also change the file. 
Consequently, if change the file, it will change the API.

**NOTE:** if you edit the json file and add an endpoint with pyjserver running, it will be necessary to restat the application to it load the new endpoint.
But it is not necessary if you edit the file and add new records.

## License
MIT
