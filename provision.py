import json
import os
import requests
import time

HEADERS = {}
def create_linode(domain, password, region="us-east", image="linode/ubuntu24.04", type_="g6-standard-1", label="linode-test-client", firewall=None):
    url = f"https://{domain}/v4/linode/instances"
    payload = {
        "region": region,
        "image": image,
        "type": type_,
        "label": label,
        "root_pass": password,
        "private_ip": False,
        "authorized_keys": ["ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDW3F/rcfXIjElkQ/zL6HIXOfNjUNuFFK4ErGSdXaoByLBB9TBaqIArWNoqktiz8211WXXucLNm1T4kn5LrouFQ/p95li/tBU+rQ+bCNfAiZ6OMnkFIZa7I8r6ENFzbmRbdHs4n0r9CB3LxGaa4+Y8Tw1zGhJAWl1EBdnRKxVLdqIdk4WWv1WRNBt3py87hX+u5yAld/y96SWVpZIZJRnyq1uXz4uwoc5bGGwIchkU9bHESawQWTHDTKXoAX3p7INWKXvHYtopOfohRwyGPTCHP820OM/0m6CRSnwBpUc2+N3Pa9blnqkxuczGjHWZxO8kesBaAfxalJzj+v6PaxMM/ swijeyas-test-2025-06-04"]
    }
    if firewall != None:
        payload["firewall_id"] = firewall
    resp = requests.post(url, json=payload, headers=HEADERS, verify=False)
    #print(resp.text)
    resp.raise_for_status()
    return resp.json()

def wait_for_linode_status(domain, linode_id, target_status="running", timeout=300):
    url = f"https://{domain}/v4/linode/instances/{linode_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=HEADERS, verify=False)
        resp.raise_for_status()
        status = resp.json()["status"]
        if status == target_status:
            return
        time.sleep(5)
    raise TimeoutError(f"Linode {linode_id} did not reach status '{target_status}' within timeout.")

def create_volume(domain, region, linode, size=20, label="my-volume"):
    url = f"https://{domain}/v4/volumes"
    payload = {
        "region": region,
        "size": size,
        "label": label,
        "linode_id": linode
    }
    resp = requests.post(url, json=payload, headers=HEADERS, verify=False)
    #print(resp.text)
    resp.raise_for_status()
    return resp.json()

def wait_for_volume_attachment(domain, volume_id, timeout=120):
    url = f"https://{domain}/v4/volumes/{volume_id}"
    start = time.time()
    while time.time() - start < timeout:
        resp = requests.get(url, headers=HEADERS, verify=False)
        resp.raise_for_status()
        linode_id = resp.json().get("linode_id")
        if linode_id is not None:
            return
        time.sleep(3)
    raise TimeoutError(f"Volume {volume_id} was not attached within timeout.")

if __name__ == "__main__":
    LINODE_API_TOKEN = os.environ["TOKEN"]
    PASSWORD = os.environ["PASSWORD"]
    REGION = os.environ["REGION"]
    IMAGE = os.environ["IMAGE"]
    LINODE_TYPE = os.environ["LINODE_TYPE"]
    LINODE_API_DOMAIN = os.environ["LINODE_API_DOMAIN"]
    LINODE_FIREWALL = None
    if "LINODE_FIREWALL" in os.environ:
        LINODE_FIREWALL = os.environ["LINODE_FIREWALL"]
    #print(LINODE_API_TOKEN)
    #print(PASSWORD)
    HEADERS = {
        "Authorization": f"Bearer {LINODE_API_TOKEN}",
        "Content-Type": "application/json"
    }
    # 1. Create Linode
    linode = create_linode(LINODE_API_DOMAIN, PASSWORD, region=REGION, image=IMAGE, type_=LINODE_TYPE, firewall=LINODE_FIREWALL)
    time.sleep(5)
    #print(f"Created Linode: {linode['id']}")
    # 2. Wait for Linode to boot
    wait_for_linode_status(LINODE_API_DOMAIN, linode['id'])
    #print("Linode is running.")
    # 3. Create Volume
    volume = create_volume(LINODE_API_DOMAIN, linode['region'], int(linode['id']), size=20)
    #print(f"Created Volume: {volume['id']}")
    time.sleep(5)
    # 4. Wait for attachment
    wait_for_volume_attachment(LINODE_API_DOMAIN, volume['id'])
    #print("Volume attached successfully.")
    pcmds = [
        {
            "command": 1,
            "group_role": "client",
            "data": {
                "connection": {
                    "user": {
                        "value": "root"
                    },
                    "sshKey": {
                        "value": "/opt/airflow/config/key"
                    }
                },
                "machines": [
                    linode['ipv4'][0]
                ]
            }
        }
    ]
    disk = {
        "path": volume["filesystem_path"],
        "linode": linode["id"],
        "volume": volume["id"]
    }
    out = {
        "patches": pcmds,
        "stdout": disk
    }
    print(json.dumps(out))
