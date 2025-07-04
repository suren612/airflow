import base64
import json
import os
import requests
import time

HEADERS = {}
def delete_linode(linode_id):
    url = f"https://api.linode.com/v4/linode/instances/{linode_id}"
    resp = requests.delete(url, headers=HEADERS)
    #print(resp.text)
    resp.raise_for_status()
    return resp.json()

def detach_volume(vol_id):
    url = f"https://api.linode.com/v4/volumes/{vol_id}/detach"
    resp = requests.post(url, headers=HEADERS)
    #print(resp.text)
    resp.raise_for_status()
    return resp.json()

def delete_volume(vol_id):
    url = f"https://api.linode.com/v4/volumes/{vol_id}"
    resp = requests.delete(url, headers=HEADERS)
    #print(resp.text)
    resp.raise_for_status()
    return resp.json()

def wait_for_volume_detachment(volume_id, timeout=120):
    url = f"https://api.linode.com/v4/volumes/{volume_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=HEADERS)
        resp.raise_for_status()
        if "linode_id" not in resp.json():
            return
        if resp.json()["linode_id"] == None:
            return
        time.sleep(3)
    raise TimeoutError(f"Volume {volume_id} was not detached within timeout.")

if __name__ == "__main__":
    PARENT_STDOUTS=os.environ["PARENT_STDOUTS"]

    b64 = PARENT_STDOUTS
    utf8 = base64.b64decode(b64)
    pouts = utf8.decode('utf-8')
    pouts_json = json.loads(pouts)
    task1_out = json.loads(pouts_json[0])
    for k in task1_out:
        prov_out = task1_out[k]["stdout"]
        LINODE_ID = prov_out["linode"]
        VOLUME_ID = prov_out["volume"]
        break

    LINODE_API_TOKEN = os.environ["TOKEN"]
    """
    LINODE_API_TOKEN = ""
    LINODE_ID = "79183117"
    VOLUME_ID = "10030444"
    """
    #print(LINODE_API_TOKEN)
    HEADERS = {
        "Authorization": f"Bearer {LINODE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    detach_volume(VOLUME_ID)
    wait_for_volume_detachment(VOLUME_ID)
    delete_volume(VOLUME_ID)
    delete_linode(LINODE_ID)
    #print("Volume attached successfully.")
