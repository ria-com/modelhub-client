import json
import argparse
from .models_example import models_example


class PrintModelsExampleAction(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super().__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        print(json.dumps(models_example, indent=4, sort_keys=False))
        setattr(namespace, self.dest, values)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config_format',
                        help='Show models config example',
                        action=PrintModelsExampleAction)
    parser.add_argument('config_format',
                        help='Show models config example',
                        action=PrintModelsExampleAction)
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    print("modelhub_client", args)
