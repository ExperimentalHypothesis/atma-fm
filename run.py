from application import create_app
from prometheus_client import Counter, make_wsgi_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware
from flask import request

app = create_app()

# Define Prometheus metrics
REQUEST_COUNT = Counter('web_requests_total', 'Total number of web requests')


@app.before_request
def before_request():
    if request.endpoint != 'static':
        REQUEST_COUNT.inc()


app.wsgi_app = DispatcherMiddleware(app.wsgi_app, {
    '/metrics': make_wsgi_app()
})

if __name__ == "__main__":
    app.run(port=5555)
