import re
import os
import sys
from embedchain import App
from embedchain.config import AppConfig

appConfig = AppConfig(log_level='DEBUG')
qa = App(config=appConfig)
meta = {"id":"1131690354001020772","summary":"this is an example summary."}
qa.add_local("text", "this is an example question.", metadata=meta)