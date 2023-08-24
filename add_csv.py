import csv
import re
import os
import sys
from embedchain import App
from embedchain.config import AppConfig

if len(sys.argv) < 2:
    print("没有输入文件")
    sys.exit(0)

def read_csv_file(file_path):
    with open(file_path, 'r') as file:
        csv_reader = csv.reader(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_ALL)
        next(csv_reader)  # 跳过第一行
        data = []
        for row in csv_reader:
            processed_row = [field.replace("\\n", "") for field in row]  # 去除单引号
            data.append(processed_row)
        return data

results = read_csv_file(sys.argv[1])

appConfig = AppConfig(collection_name='knowledge',log_level='DEBUG',collect_metrics=False)
qa = App(config=appConfig)

i=0
id=0
path=1
title=2
content=3
for item in results:
    i=i+1
    print(f"Processing {i} record ... ...")
    meta = {"id":item[id],"path":item[path],"summary":""}
    print(meta)
    qa.add_local("text", item[path]+"/"+item[title], metadata=meta)

