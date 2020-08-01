import argparse

from . import Endpoint, __version__

# main parser
parser = argparse.ArgumentParser(description='Python implementation of Node JSON Server (Flask as backend)')

# group info
group_info = parser.add_argument_group('info', 'Get information about PyJServer')
group_info.add_argument('-v', '--version', action='version', version=__version__)

# group run
group_run = parser.add_argument_group('run', 'Load .json file and create CRUD endpoint')

group_run.add_argument('name', type=str, help='PyJSONServer name')
group_run.add_argument('file_path', type=str, help='JSON data file path')

group_run.add_argument('--host', type=str, default='localhost', help='application host IP')
group_run.add_argument('-p', '--port', type=int, default=5000, help='application port')
group_run.add_argument('-d', '--debug', type=bool, default=False, help='application debug')

# parsing
args = parser.parse_args()

if __name__ == '__main__':
    endpoint = Endpoint(args.name, db_file_path=args.file_path)
    endpoint.run(host=args.host, port=args.port, debug=args.debug)
