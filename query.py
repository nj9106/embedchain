import os

from embedchain import App
from embedchain.config import AppConfig
from embedchain.config import QueryConfig

appConfig = AppConfig(log_level='DEBUG')
qa = App(config=appConfig)
q = "this is an example question."
queryConfig = QueryConfig(number_documents=3)
print(qa.retrieve_from_database(q, config=queryConfig))