import os
import urllib.request
from tqdm import tqdm
import pathlib
from zipfile import ZipFile

latest_models = {}

# load latest paths
dirpath = os.getcwd()


def show_last_models():
    print(latest_models)


def ls():
    models_list = []
    for r, d, f in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./models")):
        for file in f:
            models_list.append(file)
    return models_list


def rm(model_name):
    for r, d, f in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./models")):
        for file in f:
            if file == model_name:
                os.remove(os.path.join(r, file))
                return True
    return False


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_url(url, output_path):
    print("Downloaded model path:", output_path)
    with DownloadProgressBar(unit='B', unit_scale=True,
                             miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=output_path, reporthook=t.update_to)


def download_latest_model(detector, model_name, ext="zip", mode="gpu", download_root_dir='/data/models'):
    # download_root_dir = os.path.dirname(os.path.realpath(__file__))
    info = latest_models[detector][model_name][ext]
    info["path"] = os.path.join(download_root_dir, "models", detector, model_name, os.path.basename(info[mode]))

    p = pathlib.Path(os.path.dirname(info["path"]))
    p.mkdir(parents=True, exist_ok=True)

    output_path = info['path']
    if ext == 'zip':
        archive_name = info["path"].split('/')[-1]
        archive_dir_name = archive_name.split('.')[0]
        archive_dir_path = os.path.join(os.path.dirname(info['path']), archive_dir_name)
        info['path'] = archive_dir_path

    if not (os.path.exists(info["path"])):
        download_url(info[mode], output_path)
        if ext == 'zip':
            with ZipFile(output_path, 'r') as zipObj:
                dir_to_extract = os.path.join(download_root_dir, "models", detector, model_name)
                zipObj.extractall(dir_to_extract)
                os.remove(output_path)

    return info
