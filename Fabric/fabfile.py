#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from fabric.api import run

def host_type():  #將"uname -s"以方法run()執行
    run('uname -s')
