import os
import logging
from transformers import pipeline, AutoModelForQuestionAnswering, AutoTokenizer
from custom_exceptions import QAContextError, QAQuestionError, QAExecError


logger = logging.getLogger(__name__)


class SpanishQA(object):
    """Class to handle intialization and processing of new samples"""

    def evaluate(self, context, question):
        """Evaluate a new sample

        :param context: string with the description that contains the answer
        :param question: string with the question that the system must answer

        """

        if context is None or len(context) == 0:
            raise QAContextError("Context is empty")

        if question is None or len(question) == 0:
            raise QAQuestionError("Question is empty")

        try:
            result = self.pipe(question=question, context=context)

        except Exception as e:
            raise QAExecError("Error executing pipe") from e

        return result

    def __init__(self, config):
        """

        :param config: dict with configuration of the model

        """

        model = AutoModelForQuestionAnswering.from_pretrained(
            config["model_name_or_path"]
        )

        tokenizer = AutoTokenizer.from_pretrained(config["model_name_or_path"])

        pipe = pipeline("question-answering", model=model, tokenizer=tokenizer)
        self.pipe = pipe


if __name__ == "__main__":

    import yaml

    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_file = os.getenv("LOG_FILE", None)

    handlers = [logging.StreamHandler()]
    if log_file is not None:
        handlers.append(logging.FileHandler(log_file))

    logging.basicConfig(
        level=log_level,
        format="%(levelname)s: %(name)20s: %(message)s",
        handlers=handlers,
    )

    config_file = "config/config.yaml"

    with open(config_file, "r") as f_stream:
        config = yaml.load(f_stream, Loader=yaml.FullLoader)

    processor = SpanishQA(config)

    result = processor.evaluate(
        question="What is the capital of Spain",
        context="The capital of Spain is Madrid",
    )

    print("Result", result)
