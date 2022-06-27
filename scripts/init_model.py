import yaml
from spanish_qa import SpanishQA

CONFIG_FILE = "config/config.yaml"

class Initializer:
    def __init__(self):
        with open(CONFIG_FILE, "r") as f_stream:
            config = yaml.load(f_stream, Loader=yaml.FullLoader)
        SpanishQA(config)
