import os

from embedchain import App
from embedchain.config import AppConfig

appConfig = AppConfig(log_level='DEBUG')
qa = App(config=appConfig)
q = "this is an example question."
print(qa.dry_run(q))