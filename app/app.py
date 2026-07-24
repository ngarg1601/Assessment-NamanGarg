import logging
import os
from collections import Counter

from flask import Flask, Response, jsonify, render_template_string, request

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logger = logging.getLogger("flask-app")

app = Flask(__name__)

APP_NAME = "Flask SRE Assessment"
APP_VERSION = "1.0.1"
ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
REQUEST_COUNTER = Counter()
ERROR_COUNTER = Counter()


# Log every request
@app.before_request
def log_request():
    REQUEST_COUNTER[request.path] += 1
    logger.info(
        "Request received | method=%s path=%s ip=%s",
        request.method,
        request.path,
        request.remote_addr,
    )


# Log every response
@app.after_request
def log_response(response):
    logger.info(
        "Response sent | status=%s path=%s",
        response.status_code,
        request.path,
    )
    return response


HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Flask SRE Assessment</title>
    <style>
        body{
            font-family: Arial, Helvetica, sans-serif;
            background:#f4f6f9;
            display:flex;
            justify-content:center;
            align-items:center;
            height:100vh;
            margin:0;
        }
        .card{
            background:white;
            padding:30px;
            border-radius:10px;
            box-shadow:0 4px 12px rgba(0,0,0,.15);
            width:520px;
            text-align:center;
        }
        h1{
            color:#2c3e50;
        }
        .status{
            color:green;
            font-size:20px;
            font-weight:bold;
        }
        table{
            width:100%;
            margin-top:20px;
            border-collapse:collapse;
        }
        td{
            padding:10px;
            border-bottom:1px solid #ddd;
            text-align:left;
        }
        td:first-child{
            font-weight:bold;
        }
    </style>
</head>
<body>

<div class="card">
    <h1>{{ app }}</h1>

    <p class="status">Application is Running</p>

    <table>
        <tr>
            <td>Version</td>
            <td>{{ version }}</td>
        </tr>
        <tr>
            <td>Environment</td>
            <td>{{ env }}</td>
        </tr>
        <tr>
            <td>Liveness Endpoint</td>
            <td>/health</td>
        </tr>

        <tr>
            <td>Readiness Endpoint</td>
            <td>/ready</td>
        </tr>
        <tr>
            <td>Version Endpoint</td>
            <td>/version</td>
        </tr>
    </table>

</div>

</body>
</html>
"""


@app.route("/")
def home():
    logger.info("Home page accessed")
    return render_template_string(
        HOME_PAGE,
        app=APP_NAME,
        version=APP_VERSION,
        env=ENVIRONMENT,
    )


@app.route("/health")
def health():
    logger.info("Health check passed")
    return jsonify({"status": "Application is up and working fine"}), 200


@app.route("/metrics")
def metrics():
    lines = [
        "# HELP flask_http_requests_total Total number of HTTP requests",
        "# TYPE flask_http_requests_total counter",
    ]

    for path, count in sorted(REQUEST_COUNTER.items()):
        lines.append(f'flask_http_requests_total{{path="{path}"}} {count}')

    lines.extend(
        [
            "# HELP flask_http_errors_total Total number of HTTP errors",
            "# TYPE flask_http_errors_total counter",
        ]
    )

    for path, count in sorted(ERROR_COUNTER.items()):
        lines.append(f'flask_http_errors_total{{path="{path}"}} {count}')

    return Response("\n".join(lines) + "\n", mimetype="text/plain")


@app.route("/ready")
def ready():
    return {"status": "Ready to Recieve Traffic"}, 200


@app.route("/version")
def version():
    logger.info("Version endpoint accessed")
    return jsonify(
        {
            "application": APP_NAME,
            "version": APP_VERSION,
            "environment": ENVIRONMENT,
        }
    )


@app.errorhandler(Exception)
def handle_exception(error):
    logger.exception("Unhandled exception: %s", error)
    ERROR_COUNTER[request.path] += 1
    status_code = getattr(error, "code", 500)
    return jsonify({"status": "ERROR"}), status_code


if __name__ == "__main__":
    logger.info(
        "Starting %s | version=%s | environment=%s",
        APP_NAME,
        APP_VERSION,
        ENVIRONMENT,
    )

    app.run(host="0.0.0.0", port=5000)
