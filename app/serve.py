import json
import sys
import predict
from multipart import create_form_parser

def app(environ, start_response):
    try:
        request_size = int(environ.get('CONTENT_LENGTH', 0))
        if request_size == 0:
            raise ValueError('Zero sized request received')

        files = {}

        def on_file(file):
            key = file.field_name.decode() if isinstance(file.field_name, bytes) else file.field_name
            if key is not None:
                files[key] = file

        content_type = environ.get('CONTENT_TYPE', '')
        parser = create_form_parser(
            {'Content-Type': content_type, 'Content-Length': str(request_size)},
            lambda field: None,
            on_file,
        )
        parser.write(environ['wsgi.input'].read(request_size))
        parser.finalize()

        if 'file' not in files:
            raise ValueError('No file field found in request')

        image = files['file'].file_object.read()
        
        prediction = predict.predict(image)

        response_code = '200 OK'
        response = json.dumps(prediction).encode('utf-8')
    except Exception:
        response_code = '400 Bad Request'
        etype, value, traceback = sys.exc_info()
        response = json.dumps(etype.__name__+': '+str(value)).encode('utf-8')

    start_response(response_code, [
        ("Content-Type", "text/plain"),
        ("Content-Length", str(len(response)))
    ])

    return iter([response])
