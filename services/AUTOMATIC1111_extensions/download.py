import os
import json
from pathlib import Path
from multiprocessing import Pool
import requests



def clone_and_install(url, star, item):
    dirname = Path(url.split("/")[-1]).stem
    username = url.split("/")[-2]
    if star > 300 and not (len(item["tags"])==1 and "UI related" in item["tags"]):
        print(dirname, star)
        os.system(f"git clone {url}")
        if os.path.exists(os.path.join(dirname, "requirements.txt")):
            os.system(f"pip install -r {os.path.join(dirname, 'requirements.txt')}")


with open("index.json", "r") as f:
    js = json.loads(f.read())
    f.close()
    items = js["extensions"]
    p = Pool(10)
    print("total:", len(items))
    for item in items:
        p.apply_async(clone_and_install, args=(item["url"], item["star"], item))
    p.close()
    p.join()