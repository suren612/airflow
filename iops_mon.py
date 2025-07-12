import json
import os
import signal
import subprocess
import time

terminate = False
child = None

def signal_handler(sig, frame):
    global child
    global terminate
    if child != None:
        try:
            os.kill(child, signal.SIGTERM)
        except Exception as e:
            pass
    terminate = True

signal.signal(signal.SIGINT, signal_handler)

iops = []
while not terminate:
    p = subprocess.Popen(["rbd", "perf", "image", "iostat", "--pool", "block-volumes", "--format", "json"], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    child = p.pid
    out, err = p.communicate()
    if err:
        print(err)
        time.sleep(1)
        continue
    out = out.decode("utf-8")
    if out.startswith("rbd:"):
        #print(out)
        continue
    iops.append(json.loads(out))
    time.sleep(1)

iops_wr = 0
iops_rd = 0
lat_wr = 0
lat_rd = 0
for stat in iops:
    for img in stat:
        iops_wr += img["write_ops"]
        iops_rd += img["read_ops"]
        lat_wr += img["write_latency"] * iops_wr
        lat_rd += img["read_latency"] * iops_rd

report = {
    "write_iops_average": iops_wr / len(iops) if len(iops) > 0 else 0,
    "read_iops_average": iops_rd / len(iops) if len(iops) > 0 else 0,
    "write_latency_us": (lat_wr / iops_wr) if iops_wr > 0 else 0,
    "read_latency_us": (lat_rd / iops_rd) if iops_rd > 0 else 0,
}

print(json.dumps(report))

"""
import base64
import json
import os

PARENT_STDOUTS=os.environ["PARENT_STDOUTS"]
DISK=""

b64 = PARENT_STDOUTS
utf8 = base64.b64decode(b64)
pouts = utf8.decode('utf-8')
pouts_json = json.loads(pouts)
task1_out = pouts_json[0][0]["stdout"]

disk_out = json.loads(task1_out["stdout"])
disk = disk_out["path"]
vol_id = disk_out["volume"]

stats = {
  "image": vol_id,
  "disk": disk,
  "iops": 12000
}
print(json.dumps(stats))
"""
