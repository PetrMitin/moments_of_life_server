from wsgiref.util import request_uri, shift_path_info
from urllib.parse import parse_qs
import json

bind = '127.0.0.1:8081'

def application(environ, start_response):
    # Get the query string
    uri = request_uri(environ)
    path_info = shift_path_info(environ)
    query_string = parse_qs(uri[len(path_info):].lstrip('?'))

    # Get the post data
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except ValueError:
        request_body_size = 0
    request_body = environ['wsgi.input'].read(request_body_size)
    if request_body:
        post_data = json.loads(request_body)
    else:
        post_data = {}

    # Print the GET and POST parameters
    print('GET parameters:', query_string)
    print('POST parameters:', post_data)

    # Start the response
    start_response('200 OK', [('Content-Type', 'text/plain')])

    # Return the response body
    return [b'OK']
