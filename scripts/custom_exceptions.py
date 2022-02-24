import logging


logger = logging.getLogger(__name__)


class QAError(Exception):
    """Base class of the exceptions in this module"""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class QAQuestionError(QAError):
    """It captures errors related to bad question prompts"""

    def __str__(self):
        return f"Error QA (question) -> {self.message}"


class QAContextError(QAError):
    """It captures errors related to bad context prompts"""

    def __str__(self):
        return f"Error QA (context) -> {self.message}"


class QAExecError(QAError):
    """It captures errors related to problems during execution"""

    def __str__(self):
        return f"Error QA (context) -> {self.message}"
