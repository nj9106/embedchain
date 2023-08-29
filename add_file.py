import re
import os
import sys
import json5
from embedchain import App
from embedchain.config import AppConfig

if len(sys.argv) < 2:
    print("没有文件路径")
    sys.exit(0)
filename = sys.argv[1]

appConfig = AppConfig(log_level='DEBUG',collect_metrics=False)
qa = App(config=appConfig)
# meta = {"id":"1131690354001020772","summary":"this is an example summary."}
i = 0
with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        i = i +1
        print(f"Processing {i} record ... ...")
        q = json5.loads(line)
        # {'id': '1131690354001021028', 'desc': '', 'summary': ''}
        meta = {"id":q['id'],"summary":q['summary']}
        print(meta)
        qa.add_local("text", q['desc'], metadata=meta)
