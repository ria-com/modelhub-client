import os
import urllib.request
import requests
import pathlib
import sys
import glob
import json
import shutil
import ujson
import warnings
from git import Repo
from git.remote import RemoteProgress
from tqdm import tqdm
from zipfile import ZipFile, ZIP_DEFLATED
from typing import Dict, List


def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


class CloneProgress(RemoteProgress):
    def __init__(self) -> None:
        super().__init__()
        self.pbar = tqdm()

    def update(self, op_code: int, cur_count: int, max_count: int = None, message: str = '') -> None:
        self.pbar.total = max_count
        self.pbar.n = cur_count
        self.pbar.refresh()


class DownloadProgressBar(tqdm):
    def update_to(self, b: int = 1, bsize: int = 1, tsize: int = None) -> None:
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


class ModelHub:
    def __init__(self,
                 models: Dict[str, Dict[str, str]] = None,
                 model_config_urls: List = None,
                 local_storage: str = None,
                 remote_storage: str = None,
                 postfix: str = "./modelhub",
                 ) -> None:
        if local_storage is None:
            local_storage = os.path.join(
                os.path.dirname(os.path.realpath(__file__)),
                postfix
            )
        self.local_storage = local_storage
        self.remote_storage = remote_storage
        if self.remote_storage is None:
            self.get_auth()
        if models is None:
            models = {}
        self.models = models
        if model_config_urls is not None:
            self.load_models_configs(model_config_urls)

    def load_models_configs(self, models_config_urls):
        cache_dir = os.path.join(self.local_storage, "configs")
        for models_config_url in models_config_urls:
            head_url, filename = os.path.split(models_config_url)
            head_url, subdir = os.path.split(head_url)
            cache_path = os.path.join(cache_dir, subdir, filename)
            os.makedirs(os.path.join(cache_dir, subdir), exist_ok=True)
            if os.path.exists(cache_path):
                with open(cache_path) as fp:
                    res = json.load(fp)
                self.models[res["name"]] = res
            else:
                response = requests.get(models_config_url)
                response.raise_for_status()
                data = response.json()
                with open(cache_path, "w") as fp:
                    json.dump(data, fp)
                self.models[data["name"]] = data
        return self.models

    def save_auth(self, remote_storage: str = None) -> None:
        if remote_storage is None:
            remote_storage = self.remote_storage
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        auth_path = os.path.join(current_file_dir, "auth.txt")
        with open(auth_path, "w") as auth_file:
            auth_file.write(remote_storage)

    def get_auth(self) -> None:
        current_file_dir = os.path.dirname(os.path.abspath(__file__))
        auth_path = os.path.join(current_file_dir, "auth.txt")
        if os.path.exists(auth_path):
            with open(auth_path, "r") as auth_file:
                self.remote_storage = auth_file.read()

    def ls(self, subdir: str = "./") -> List[str]:
        dirs_list = []
        for model_name in self.models:
            info = self.models[model_name]
            path = os.path.join(self.local_storage,
                                subdir,
                                info["application"],
                                model_name)
            if os.path.exists(path):
                dir_list = os.listdir(path)
                dirs_list.extend(dir_list)
        return dirs_list

    def rm(self, subdir: str = "./") -> None:
        models_dir = os.path.join(self.local_storage, subdir)
        shutil.rmtree(models_dir, ignore_errors=True)

    def ls_models_local(self) -> List[str]:
        return self.ls("./models")

    def ls_datasets_local(self) -> List[str]:
        return self.ls("./datasets")

    def ls_repos_local(self) -> List[str]:
        return self.ls("./repos")

    def rm_models_local(self) -> None:
        self.rm("./models")

    def rm_datasets_local(self) -> None:
        self.rm("./datasets")

    def rm_repos_local(self) -> None:
        self.rm("./repos")

    @staticmethod
    def download(url, output_path):
        print("Downloaded model path:", output_path)
        with DownloadProgressBar(unit='B',
                                 unit_scale=True,
                                 miniters=1,
                                 desc=url.split('/')[-1]) as t:
            urllib.request.urlretrieve(url,
                                       filename=output_path,
                                       reporthook=t.update_to)

    def download_model_by_url(self, url: str, application: str, model_name: str) -> Dict[str, str]:
        models = {
            model_name: {
                "application": application,
                "url": url
            }
        }
        return self.download_model_by_name(model_name, models)

    def download_model_by_name(self,
                               model_name: str,
                               models: Dict = None,
                               path: str = None) -> Dict[str, str]:
        if models is None:
            info = self.models[model_name]
        else:
            info = models[model_name]
        if path is None:
            info["path"] = os.path.join(self.local_storage,
                                        "./models",
                                        info["application"],
                                        model_name,
                                        os.path.basename(info["url"]))
        else:
            info["path"] = path

        p = pathlib.Path(os.path.dirname(info["path"]))
        p.mkdir(parents=True, exist_ok=True)

        output_path = info['path']
        _, file_extension = os.path.splitext(info['path'])
        if file_extension == '.zip':
            archive_name = os.path.basename(info["path"])
            archive_dir_name, _ = os.path.splitext(archive_name)
            archive_dir_path = os.path.join(os.path.dirname(info['path']), archive_dir_name)
            if os.path.exists(archive_dir_path):
                info['path'] = archive_dir_path
                return info
        elif os.path.exists(info['path']):
            return info

        self.download(info["url"], info["path"])
        if file_extension == '.zip':
            info['path'] = archive_dir_path
            if not os.path.exists(output_path):
                return info
            with ZipFile(output_path, 'r') as zipObj:
                dir_to_extract = os.path.join(os.path.dirname(info['path']))
                zipObj.extractall(dir_to_extract)
            if not os.path.exists(output_path):
                return info
            os.remove(output_path)
        return info

    def download_dataset_for_model(self,
                                   model_name: str,
                                   delete_source: bool = False) -> Dict[str, str]:
        info = self.models[model_name]
        info["dataset_path"] = os.path.join(self.local_storage,
                                            "./dataset",
                                            info["application"],
                                            model_name,
                                            os.path.basename(info["dataset"]))
        p = pathlib.Path(os.path.dirname(info["dataset_path"]))
        p.mkdir(parents=True, exist_ok=True)

        dataset_path = info['dataset_path']
        check_dir, file_extension = os.path.splitext(info['dataset_path'])
        archive_dir_path = os.path.dirname(info['dataset_path'])
        if os.path.exists(check_dir):
            info['dataset_path'] = check_dir
            return info

        if file_extension != '.zip':
            raise Exception("Not supported file extension!")

        self.download(info["dataset"], dataset_path)
        info['dataset_path'] = check_dir
        with ZipFile(dataset_path, 'r') as zipObj:
            dir_to_extract = archive_dir_path
            zipObj.extractall(dir_to_extract)
            if delete_source:
                os.remove(dataset_path)
        return info

    def download_repo_for_model(self, model_name: str) -> Dict[str, str]:
        info = self.models[model_name]
        pre_repo_path = os.path.join(self.local_storage,
                                     "./repos",
                                     info["application"])
        info["repo_path"] = os.path.join(pre_repo_path,
                                         model_name)
        if not os.path.exists(info["repo_path"]):
            print("git clone", info["repo"])
            repo = Repo.clone_from(
                info["repo"],
                info["repo_path"],
                progress=CloneProgress(),
                no_checkout="commit_id" in info)
            if "commit_id" in info:
                repo.git.checkout(info["commit_id"])
        sys.path.append(pre_repo_path)
        sys.path.append(info["repo_path"])
        return info

    def save_remote_file(self, update_file: str, filename: str) -> None:
        url = os.path.join(self.remote_storage, update_file)
        response = requests.put(url, data=open(filename, 'rb').read(), headers={})
        response.raise_for_status()

    def rm_remote(self, dir_for_remove):
        url = os.path.join(self.remote_storage, dir_for_remove)
        response = requests.request('DELETE', url)
        response.raise_for_status()

    def mkdir_remote(self, new_dir):
        if new_dir[-1] != "/":
            new_dir = f"{new_dir}/"
        url = os.path.join(self.remote_storage, new_dir)
        response = requests.request('MKCOL', url)
        response.raise_for_status()

    def store_remote_file(self, local_dir, server_dir, filename):
        upload_from = os.path.join(local_dir, filename)
        upload_to = os.path.join(server_dir, filename)
        return self.save_remote_file(upload_to, upload_from)

    def store_remote(self, local_dir: str, server_dir: str = "./", remove_source: bool = False):
        server_dir_path = ""
        for server_d in server_dir.split("/"):
            server_dir_path = os.path.join(server_dir_path, server_d)
            print(server_dir_path)
            self.mkdir_remote(server_dir_path)

        for file in glob.glob(os.path.join(local_dir, "*")):
            print("Store remote", file)
            self.store_remote_file(local_dir, server_dir, os.path.basename(file))

        if remove_source:
            shutil.rmtree(local_dir)

    def store_remote_by_json(self, json_path: str) -> None:
        """
        TODO: Add remove remote before save
        :param json_path:
        :return:
        """
        with open(json_path, 'r') as json_file:
            models = json.load(json_file)
        for model_name in models:
            print("[SAVE]", model_name)
            info = models[model_name]
            if models[model_name].get("path", None):
                basename = os.path.basename(models[model_name]["path"])
                dirname = os.path.dirname(models[model_name]["path"])
                if os.path.isdir(models[model_name]["path"]):
                    with ZipFile(f'{basename}.zip', 'w', ZIP_DEFLATED) as zipf:
                        zipdir(models[model_name]["path"], zipf)
                    basename = f'{basename}.zip'
                server_dirname = os.path.join(
                    "models",
                    info["application"],
                    model_name
                )
                print("[MODEL URL]", os.path.join(self.remote_storage, server_dirname, basename))
                self.store_remote_file(dirname, server_dirname, basename)
            if models[model_name].get("dataset_path", None):
                basename = os.path.basename(models[model_name]["dataset_path"])
                dirname = os.path.dirname(models[model_name]["dataset_path"])
                if os.path.isdir(models[model_name]["path"]):
                    with ZipFile(f'{basename}.zip', 'w', ZIP_DEFLATED) as zipf:
                        zipdir(models[model_name]["path"], zipf)
                    basename = f'{basename}.zip'
                server_dirname = os.path.join(
                    "dataset",
                    info["application"],
                    model_name
                )
                print("[DATASET URL]", os.path.join(self.remote_storage, server_dirname, basename))
                self.store_remote_file(dirname, server_dirname, basename)
