import gunicorn
import json
import cgi
import sys
import predict

def app(environ, start_response):
    try:
        request_size = int(environ.get('CONTENT_LENGTH', 0))
        if request_size == 0:
            raise ValueError('Zero sized request received')
        
        form = cgi.FieldStorage(fp=environ['wsgi.input'], environ=environ)
        f = form['file'].file
        image = f.read()
        
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
