import os
import sys

from embedchain import App
from embedchain.config import AppConfig
from embedchain.config import QueryConfig

if len(sys.argv) < 2:
    print("没有提供问题")
    sys.exit(0)

appConfig = AppConfig(log_level='DEBUG',collect_metrics=False)
qa = App(config=appConfig)

urlPrefix = 'https://www.tapd.cn/31690354/bugtrace/bugs/view?bug_id='

q = sys.argv[1]
queryConfig = QueryConfig(number_documents=3)
results = qa.retrieve_from_database(q, config=queryConfig)
out = []
i = 0
while i < len(results['documents'][0]):
    metadata = results['metadatas'][0][i]
    o = {"question": results['documents'][0][i], "summary": metadata['summary'], "url": f"{urlPrefix}{metadata['id']}"}
    out.append(o)
    i = i+1
print(out)


knowledgeConfig = AppConfig(collection_name='knowledge',log_level='DEBUG',collect_metrics=False)
knowledge = App(config=knowledgeConfig)
knowledgePrefix  = 'https://helpy-dev.plaso.cn/zh/'
results = knowledge.retrieve_from_database(q, config=queryConfig)
out = []
i = 0
while i < len(results['documents'][0]):
    metadata = results['metadatas'][0][i]
    o = {"question": results['documents'][0][i], "summary": metadata['summary'], "url": f"{knowledgePrefix}{metadata['path']}"}
    out.append(o)
    i = i+1
print(out)