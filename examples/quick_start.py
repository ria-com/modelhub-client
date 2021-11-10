# import python modules
import os
import sys

# add package root
sys.path.append(os.getcwd())

from modelhub_client import (ModelHub,
                             models_example)

# initial
model_hub = ModelHub(models=models_example,
                     local_storage=os.path.join(os.getcwd(), "./data"))

# download model
model_hub.download_model_by_name("numberplate_options")
model_hub.download_repo_for_model("numberplate_options")

# ls local storage
models_list = model_hub.ls_models_local()
print(models_list)
