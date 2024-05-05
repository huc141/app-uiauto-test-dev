import sys
from typing import Iterable
import yaml
import os


class Config:
    __raw_data = dict()

    def __init__(self):
        p = os.path.join(os.getcwd(), '/config')
        print(p)


config = Config()
config.__init__()
