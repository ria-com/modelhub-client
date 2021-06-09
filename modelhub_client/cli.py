import json
import argparse
from . import (ModelHub,
               models_example)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('config_format',
                        action='store_true',
                        help='Show models config example')
    parser.add_argument('auth',
                        action='store_true',
                        help='Show/Save modelhub remote url')
    parser.add_argument('--remote_url',
                        type=str,
                        required=False,
                        help='Save modelhub remote remote_url')
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()

    if args.get("config_format", None):
        print(json.dumps(models_example, indent=4, sort_keys=False))
    if args.get("auth", None):
        model_hub = ModelHub()
        model_hub.get_auth()
        print("Current remote storage", model_hub.remote_storage)
        if args.get("remote_url", None):
            model_hub.save_auth(args["remote_url"])
            print("Changed remote storage:", args["remote_url"])

    print("modelhub_client", args)
