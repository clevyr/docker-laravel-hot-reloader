import json
import sys
import urllib.request
from datetime import datetime

nodeScheduleUrl = (
    "https://raw.githubusercontent.com/nodejs/Release/master/schedule.json"
)
now = datetime.now()
matrix = {"include": []}
repo = sys.argv[1]

with urllib.request.urlopen(nodeScheduleUrl) as response:
    jsonResponse = json.loads(response.read())

ltsRelease = None
for key, value in jsonResponse.items():
    if "lts" in value:
        lts = datetime.strptime(value["lts"], "%Y-%m-%d")
        if lts < now:
            ltsRelease = key

for key, value in jsonResponse.items():
    version = key.lstrip("v")

    start = datetime.strptime(value["start"], "%Y-%m-%d")
    end = datetime.strptime(value["end"], "%Y-%m-%d")

    if start < now < end:
        extra_tags = ""

        if key == ltsRelease:
            extra_tags += f"{repo}:lts"

        matrix["include"].append({"node_version": version, "extra_tags": extra_tags})

matrix["include"][-1]["extra_tags"] += f",{repo}:latest"

print(json.dumps(matrix))
