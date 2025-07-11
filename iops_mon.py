import base64
import json

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
print(stats)
