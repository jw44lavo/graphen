import yaml
import os
from os import listdir
import glob

dictionary = {'samples':[]}

path = f"{os.getcwd()}/data"

dirs = glob.glob(str(path)+"/EC_*")

for d in dirs:
    for EC in os.listdir(d):
        dictionary['samples'].append({EC.replace('.json',''):d})

with open("structures.yaml","w") as file:
    doc = yaml.dump(dictionary,file)
