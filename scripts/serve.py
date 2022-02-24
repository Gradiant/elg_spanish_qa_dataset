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
json_app = FlaskJSON(app)


@as_json
@app.route("/process", methods=["POST"])
def process():
    data = request.get_json()
    if (
        (data is None or data.get("type") != "structuredText")
        or ("texts" not in data)
        or (len(data.get("texts")) != 2)
    ):

        output = invalid_request_error(None)
        return output

    try:
        context = data.get("texts")[0].get("content")
        question = data.get("texts")[1].get("content")

        result = processor.evaluate(question=question, context=context)
        output = generate_successful_response(result)
        return output
    except Exception as e:
        return generate_failure_response(
            status=404,
            code="elg.service.internalError",
            text=None,
            params=None,
            detail=e.__str__(),
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


def generate_successful_response(result):
    """Generates the dict with the text classification reponse

    :param label: the answer of the system
    :return: a dict with the response in annotations format

    """

    response = {
        "type": "annotations",
        "annotations": {
            "answers": [
                {
                    "start": result["start"],
                    "end": result["end"],
                    "features": {"answer": result["answer"], "score": result["score"]},
                }
            ]
        },
    }

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
