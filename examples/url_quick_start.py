# import python modules
import os
import sys

# add package root
sys.path.append(os.getcwd())

from modelhub_client import ModelHub

# initial
model_hub = ModelHub(model_config_urls=[
                        "http://models.vsp.net.ua/config_model/nomeroff-net-np-classification/model-2.json"
                     ],
                     local_storage=os.path.join(os.getcwd(), "./data"))

# download model
model_hub.download_model_by_name("numberplate_options")

# ls local storage
models_list = model_hub.ls_models_local()
print(models_list)
