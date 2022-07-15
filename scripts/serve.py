import os
import yaml
import logging
import subprocess
from flask import Flask, request
from flask_json import FlaskJSON, JsonError, as_json
from werkzeug.utils import secure_filename
from spanish_qa import SpanishQA


CONFIG_FILE = "config/config.yaml"


log_level = os.getenv("LOG_LEVEL", "INFO")
log_file = os.getenv("LOG_FILE", None)

handlers = [logging.StreamHandler()]
if log_file is not None:
    handlers.append(logging.FileHandler(log_file))

logging.basicConfig(
    level=log_level, format="%(levelname)s: %(name)20s: %(message)s", handlers=handlers
)

with open(CONFIG_FILE, "r") as f_stream:
    config = yaml.load(f_stream, Loader=yaml.FullLoader)

processor = SpanishQA(config)


app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True
APP_ROOT = "./"
app.config["APPLICATION_ROOT"] = APP_ROOT
app.config["JSON_ADD_STATUS"] = False
app.config["JSON_SORT_KEYS"] = False
json_app = FlaskJSON(app)


@as_json
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()

    if data["type"] != "text":
        return generate_failure_response(
            status=400,
            code="elg.request.type.unsupported",
            text="Request type {0} not supported by this service",
            params=[data["type"]],
            detail=None,
        )
    if "content" not in data:
        return invalid_request_error(
            None,
        )

    content = data.get("content")
    params = data.get("params", {})
    if "question" not in params:
        # Standard message code for missing parameter
        return generate_failure_response(
            status=400,
            code="elg.request.parameter.missing",
            text="Required parameter {0} missing from request",
            params=["question"],
            detail=None,
        )

    context = content
    question = params["question"]
    try:
        result = processor.evaluate(question=question, context=context)
        output = generate_successful_text_response(result)
        return output
    except Exception as e:
        text = (
            "Unexpected error. If your input text is too long, this may be the cause."
        )
        # Standard message for internal error - the real error message goes in params
        return generate_failure_response(
            status=500,
            code="elg.service.internalError",
            text="Internal error during processing: {0}",
            params=[text],
            detail=None,
        )


@json_app.invalid_json_error
def invalid_request_error(e):
    """Generates a valid ELG "failure" response if the request cannot be parsed"""
    raise JsonError(
        status_=400,
        failure={
            "errors": [
                {"code": "elg.request.invalid", "text": "Invalid request message"}
            ]
        },
    )

def generate_successful_text_response(result):
    response = {"type": "texts", "texts": [{"content": result["answer"]}]}
    output = {"response": response}
    return output

@json_app.invalid_json_error
def generate_failure_response(status, code, text, params, detail):
    """Generate a wrong response indicating the failure

    :param status: api error code
    :param code: ELG error type
    :param text: not used
    :param params: not used
    :param detail: detail of the exception

    """

    error = {}
    if code:
        error["code"] = code
    if text:
        error["text"] = text
    if params:
        error["params"] = params
    if detail:
        error["detail"] = {"message": detail}

    raise JsonError(status_=status, failure={"errors": [error]})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8866)
