import os
import sys

from embedchain import App
from embedchain.config import AppConfig
from embedchain.config import QueryConfig

if len(sys.argv) < 2:
    print("没有提供问题")
    sys.exit(0)

appConfig = AppConfig(log_level='DEBUG')
qa = App(config=appConfig)
q = sys.argv[1]
queryConfig = QueryConfig(number_documents=3)
print(qa.retrieve_from_database(q, config=queryConfig))
