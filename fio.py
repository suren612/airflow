import base64
import json
import os
import subprocess

PARENT_STDOUTS=os.environ["PARENT_STDOUTS"]
DISK=""
FIO_RUNTIME=os.environ["FIO_RUNTIME"]
FIO_OP=os.environ["FIO_OP"]

b64 = PARENT_STDOUTS
utf8 = base64.b64decode(b64)
pouts = utf8.decode('utf-8')
pouts_json = json.loads(pouts)
task1_out = json.loads(pouts_json[0][0])
for k in task1_out:
    disk_out = task1_out[k]["stdout"]["stdout"]
    DISK = disk_out["path"]
    break

#print(f"{DISK=}, {FIO_RUNTIME=}, {FIO_OP=}")
out = subprocess.check_output(["fio", "--filename", DISK, "--direct", "1", "--rw", FIO_OP, "--bs", "4k", "--ioengine", "libaio", "--iodepth", "16","--runtime", FIO_RUNTIME, "--numjobs", "1", "--time_based", "--group_reporting", "--name", "iops-test", "--output-format", "json"])

print(out.decode("utf-8"))
