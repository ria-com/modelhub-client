# import python modules
import os
import sys
import unittest

# add package root
sys.path.append(os.getcwd())

from modelhub_client import (ModelHub,
                             models_example)


class ModelHubClientTest(unittest.TestCase):
    def test_download_model_by_name(self) -> None:
        model_hub = ModelHub(models=models_example,
                             local_storage=os.path.join(os.getcwd(), "./data"))
        model_hub.download_model_by_name("numberplate_options")
        models_list = model_hub.ls_models_local()
        self.assertEqual(models_list, ["numberplate_options_2021_05_23.pt"])

    def test_download_repo_for_model(self) -> None:
        model_hub = ModelHub(models=models_example,
                             local_storage=os.path.join(os.getcwd(), "./data"))
        model_hub.download_repo_for_model("numberplate_options")
        repos_list = model_hub.ls_repos_local()
        self.assertEqual(repos_list, ["nomeroff-net"])

    def test_download_dataset_for_model(self) -> None:
        model_hub = ModelHub(models=models_example,
                             local_storage=os.path.join(os.getcwd(), "./data"))
        model_hub.download_dataset_for_model("numberplate_options")
        datasets_list = model_hub.ls_datasets_local()
        self.assertEqual(datasets_list, ["autoriaNumberplateOptionsDataset-2021-05-17"])


if __name__ == '__main__':
    unittest.main()
