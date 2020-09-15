

import os
import json
import jsonschema
from jsonschema import validate
import yaml
import requests

def checkStackml(schema, system):
    with open(system, 'r') as f:
        f = yaml.load(f, Loader=yaml.FullLoader)
        try :
            validate(f, schema)
        except Exception as e:
            raise e
        else:
            return f

def get_stackml_schema() -> dict or None:
    request = requests.get('https://stackml.stackeo.io/_static/stackml.schema.json')
    schema = None
    if request.status_code == 200:
        schema = json.loads(request.content.decode("utf-8"))
    else:
        exit('Warning: Stackml schema does not find')
    request.close()
    return schema

if __name__ == "__main__":
    system = 'Examples/Test/main.stkml.yaml'
    schema = get_stackml_schema()
    stackml = checkStackml(schema, system)
    path = os.path.abspath(system).split('main.stkml.yaml')[0]
    for o in stackml['import']:
        imports = os.path.join(path, f'{o}{system.split("main")[-1]}')
        if os.path.isfile(imports):
            try: 
                checkStackml(schema, imports)
            except jsonschema.exceptions.ValidationError as e:
                raise e
        else:
            raise FileNotFoundError