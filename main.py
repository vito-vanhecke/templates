from typing import Optional
import json
import subprocess


from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/run/{script_name}")
def read_script(script_name: str):
    # Run script via script-name
    # Error route for non existing script
    subprocess.run(f"cd app/{script_name} && python3 {script_name}.py && cd ../..", shell=True)

    # json to tsv
    result = {}
    files_json = open(f"/code/app/{script_name}/output.json")
    jsonOutput = json.load(files_json)
    for filename in jsonOutput:
        inputfile = f"/code/app/{script_name}/{script_name}/{filename}"
        # clause_....txt
        result[f"{filename}"] = tsv2json(inputfile)

    files_json.close()
    resultfile = f"/code/app/{script_name}/result.json"

    with open(resultfile, 'w', encoding='utf-8') as result_file:
        result_file.write(json.dumps(result, indent=4))

    return JSONResponse(result)
  
  

# helper functions
def tsv2json(input_file):
    arr = []
    file = open(input_file, 'r')
    a = file.readline()

    # The first line consist of headings of the record
    # so we will store it in an array and move to
    # next line in input_file.
    titles = [t.strip() for t in a.split('\t')]
    for line in file:
        d = {}
        for t, f in zip(titles, line.split('\t')):

            # Convert each row into dictionary with keys as titles
            d[t] = f.strip()

        # we will use strip to remove '\n'.
        arr.append(d)

        # we will append all the individual dictionaires into list
        # and dump into file.
    return arr