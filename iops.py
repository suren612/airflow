import base64
import json
import os
import psutil
import signal
import time

from pathlib import Path
PARENT_STDOUTS=os.environ["PARENT_STDOUTS"]

b64 = PARENT_STDOUTS
utf8 = base64.b64decode(b64)
pouts = utf8.decode('utf-8')
pouts_json = json.loads(pouts)
task1_out = json.loads(pouts_json[0])
for k in task1_out:
    disk_out = task1_out[k]["stdout"]
    #print(disk_out)
    disk = disk_out["path"]
    break

disk = str(Path(disk).resolve())
disk = os.path.basename(disk)
terminate = False

def signal_handler(sig, frame):
    global terminate
    terminate = True

signal.signal(signal.SIGINT, signal_handler)

iops_r = []
iops_w = []
iops = psutil.disk_io_counters(perdisk=True)
prev_r = iops[disk].read_count
prev_w = iops[disk].write_count

while not terminate:
    iops = psutil.disk_io_counters(perdisk=True)
    r = iops[disk].read_count - prev_r
    w = iops[disk].write_count - prev_w
    iops_r.append(r)
    iops_w.append(w)
    prev_r = iops[disk].read_count
    prev_w = iops[disk].write_count
    time.sleep(1)

res = {
    "read": sum(iops_r)/len(iops_r),
    "write": sum(iops_w)/len(iops_w)
}
print(json.dumps(res))
