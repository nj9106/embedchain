import re
import os
import sys
import json
from embedchain import App
from embedchain.config import AppConfig


appConfig = AppConfig(log_level='DEBUG')
qa = App(config=appConfig)
meta = {"id":"1131690354001020772","summary":"this is an example summary."}
qa.add_local("text", "this is an example question.", metadata=meta)
filename = '/root/tapd/tapd.txt'
i = 0
with open(filename, 'r') as file:
    lines = file.readlines()
    for line in lines:
        i = i +1
        print(f"Processing {i} record ... ...")
        q = json.loads(line)
        # {'id': '1131690354001021028', 'desc': '', 'summary': ''}
        qa.add_local("text", q['desc'], metadata={"id":q['id'],"summary":q['summary']})
