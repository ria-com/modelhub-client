# RIA ModelHub Client

## Installation
```bash
pip3 install git+https://github.com/ria-com/modelhub-client.git
```
or
```bash
git clone https://github.com/ria-com/modelhub-client.git
cd ./modelhub-client
python3 setup.py install
```

## Quick Start
```python3
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

# ls local storage
models_list = model_hub.ls_models_local()
print(models_list)
```

## Config Example
```python3
{   
    # unique model name
    "numberplate_options": {
        # application name 
        "application": "Numberplate Options Application",
        
        # model url for downloading 
        # model will be downloaded into 
        # [local_storage]/models/[application]/[model_name] dir
        "url": "https://nomeroff.net.ua/models/options/torch/numberplate_options_2021_05_23.pt",
        
        # model dataset url for downloading
        # dataset will be downloaded into 
        # [local_storage]/datasets/[application]/[model_name] dir
        "dataset": "https://nomeroff.net.ua/datasets/autoriaNumberplateOptionsDataset-2021-05-17.zip",
        
        # model repo url for cloning
        # and pushing into PATH
        # repo will be cloned into 
        # [local_storage]/repos/[application]/[model_name] dir
        "repo": "https://github.com/ria-com/nomeroff-net",
        
        # model description (not required)
        "description": "Numberplate Options Classification",
        
        # model task (not required)
        "task": "Classification",
        
        # model type (not required)
        "type": "Supervised Learning",
        
        # model architecture (not required)
        "architecture": "CNN",
    }
}
```

## Tests
```bash
python3 ./tests/test.py
```