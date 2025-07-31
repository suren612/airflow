import base64
import json
import os
import subprocess

PARENT_STDOUTS=os.environ["PARENT_STDOUTS"]
DUMP_URL=os.environ["DUMP_URL"]

report = {}

b64 = PARENT_STDOUTS
utf8 = base64.b64decode(b64)
pouts = utf8.decode('utf-8')
pouts_json = json.loads(pouts)
#task1_out = json.loads(pouts_json[0][0])
#task2_out = json.loads(pouts_json[1][0])
#task3_out = json.loads(pouts_json[2][0])


task1_out = pouts_json[0][0]["stdout"]
task2_out = pouts_json[1][0]["stdout"]
task3_out = pouts_json[2][0]["stdout"]

cpu_out = task2_out["stdout"]
report["cpu"] = cpu_out
report["iops"] = json.loads(task3_out["stdout"])
report["fio"] = json.loads(task1_out["stdout"])

msg = json.dumps(report)

url = DUMP_URL
bash_command = ["curl", "-vvv", "--header", "Content-Type: application/json", "--request", "POST", "--data", msg, url]
res = subprocess.check_output(bash_command)
print(report)
