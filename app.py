import socket
from time import sleep
import logging as log
import threading
from BaseHTTPServer import HTTPServer
from flask import Flask, render_template
from prometheus_client import start_http_server, Summary, MetricsHandler, Counter

app = Flask(__name__)
PROMETHEUS_PORT = 9000

# Create a metric to track time spent and requests made.
REQUEST_TIME = Summary('request_processing_seconds', 'DESC: Time spent processing request')
INDEX_TIME = Summary('index_request_processing_seconds', 'DESC: INDEX time spent processing request')

@app.route('/')
@INDEX_TIME.time()
def hello_world():
    return 'Flask Dockerized'

# Decorate function with metric.
@REQUEST_TIME.time()
def process_request():
    """A dummy function that takes some time."""
    sleep(2)
    c = Counter('requests_for_host', 'Number of runs of the process_request method')
    c.inc()  # Increment by 1
    fqdn = socket.getfqdn()
    return fqdn

@app.route('/host')
def metric():
    ret = str(process_request())
    return "The name of this host is: {}".format(ret)


# Seperate web server for prometheus scraping
class PrometheusEndpointServer(threading.Thread):
    """A thread class that holds an http and makes it serve_forever()."""
    def __init__(self, httpd, *args, **kwargs):
        self.httpd = httpd
        super(PrometheusEndpointServer, self).__init__(*args, **kwargs)

    def run(self):
        self.httpd.serve_forever()

# keep the server running
def start_prometheus_server():
    try:
        httpd = HTTPServer(("0.0.0.0", PROMETHEUS_PORT), MetricsHandler)
    except (OSError, socket.error):
        return

    thread = PrometheusEndpointServer(httpd)
    thread.daemon = True
    thread.start()
    log.info("Exporting Prometheus /metrics/ on port %s", PROMETHEUS_PORT)

start_prometheus_server()

if __name__ == '__main__':
    #app.run(debug=True,host='0.0.0.0')
    
    # Start up the server to expose the metrics.
    #start_http_server(9090, '127.0.0.1')
    #print "nefpre"
    #sleep(5)
    #print "after"
    app.run(debug=True,host='0.0.0.0')
    # Generate some requests.
   # while True:
   #     process_request()
