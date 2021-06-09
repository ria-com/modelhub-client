import json
import argparse
from . import (ModelHub,
               models_example)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_format',
                        help='Show models config example')
    parser.add_argument('auth',
                        help='Save modelhub remote url')
    parser.add_argument('show_auth',
                        help='Show modelhub remote url')
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()

    if args.get("config_format", None):
        print(json.dumps(models_example, indent=4, sort_keys=False))
    if args.get("auth", None):
        model_hub = ModelHub()
        model_hub.save_auth(args["auth"])
        print("Changed remote storage:", args["auth"])
    if args.get("show_auth", None):
        model_hub = ModelHub()
        model_hub.get_auth()
        print("Current remote storage", model_hub.remote_storage)
    print("modelhub_client", args)
