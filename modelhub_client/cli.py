import json
import argparse
from . import (ModelHub,
               models_example)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('action',
                        choices=['config_format', 'auth', "remote_store"])
    parser.add_argument('--remote_url',
                        type=str,
                        required=False,
                        help='Save modelhub remote remote_url')
    parser.add_argument('--config_path',
                        type=str,
                        required=False,
                        help='config_path for remote_store action')
    args = vars(parser.parse_args())
    return args


def main():
    args = parse_args()
    if args["action"] == "config_format":
        print(json.dumps(models_example, indent=4, sort_keys=False))
    elif args["action"] == "auth":
        model_hub = ModelHub()
        model_hub.get_auth()
        print("Current remote storage", model_hub.remote_storage)
        if not args.get("remote_url", None):
            return
        model_hub.save_auth(args["remote_url"])
        print("Changed remote storage:", args["remote_url"])
    elif args["action"] == "remote_store":
        if not args.get("config_path", None):
            return
        model_hub = ModelHub()
        if args.get("remote_url", None):
            model_hub.remote_storage = args["remote_url"]
        else:
            model_hub.get_auth()
        config_path = args["config_path"]
        model_hub.store_remote_by_json(config_path)
