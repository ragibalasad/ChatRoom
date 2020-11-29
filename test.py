import json

with open("json.json", "r") as jsonFile:
    data = json.load(jsonFile)

data["username"] = "srabon"

with open("json.json", "w") as jsonFile:
    json.dump(data, jsonFile)