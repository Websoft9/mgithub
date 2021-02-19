#!/usr/bin/env python3
# coding=utf-8
class CustomException(Exception):

    def __init__(self, msg):
        super().__init__()
        self.msg = msg
