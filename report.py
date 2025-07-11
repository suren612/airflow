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
report["cpu_average"] = cpu_out

iops_out = json.loads(task3_out["stdout"])
report["read_iops_average"] = iops_out["read"]
report["write_iops_average"] = iops_out["write"]

#for k in task1_out:
#    cpu_out = task1_out[k]["stdout"]["stdout"]
#    report["cpu_average"] = cpu_out
#    break

#for k in task2_out:
#    iops_out = json.loads(task2_out[k]["stdout"]["stdout")
#    report["read_iops_average"] = iops_out["read"]
#    report["write_iops_average"] = iops_out["write"]
#    break

#for k in task3_out:
fio_out = json.loads(task1_out["stdout"])
jobr = fio_out["jobs"][0]["read"]
jobw = fio_out["jobs"][0]["write"]
lat_key = ""
unit = ""
if "lat_ns" in jobr:
    lat_key = "lat_ns"
    unit = "ns"
if "lat_us" in jobr:
    lat_key = "lat_us"
    unit = "us"
if "lat_ms" in jobr:
    lat_key = "lat_ms"
    unit = "ms"
report[f"read_latency_{unit}"] = jobr[lat_key]
if "lat_ns" in jobw:
    lat_key = "lat_ns"
    unit = "ns"
if "lat_us" in jobw:
    lat_key = "lat_us"
    unit = "us"
if "lat_ms" in jobw:
    lat_key = "lat_ms"
    unit = "ms"
report[f"write_latency_{unit}"] = jobw[lat_key]
#    break

msg = json.dumps(report)

url = DUMP_URL
bash_command = ["curl", "-vvv", "--header", "Content-Type: application/json", "--request", "POST", "--data", msg, url]
res = subprocess.check_output(bash_command)
print(report)
