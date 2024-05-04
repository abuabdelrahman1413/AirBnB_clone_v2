#!/usr/bin/python3
"""This module defines the function do_clean
"""
from fabric.api import *


env.hosts = ['54.158.189.0', '54.157.148.186']
env.user = 'ubuntu'


def do_clean(number=0):
    """This function deletes out-of-date archives
    """
    output = local("ls -lt ./versions/", capture=True)
    output = output.split('\n')
    output.pop(0)
    if number == "0":
        number = 1
    i = int(number)
    while i <= (len(output) - 1):
        filename = output[i].split(' ')[-1]
        local("rm ./versions/{}".format(filename))
        i += 1

    output = run("ls -lt /data/web_static/releases")
    output = output.split('\n')
    output.pop(0)
    if number == "0":
        number = 1
    i = int(number)
    while i <= (len(output) - 1):
        filename = output[i].split(' ')[-1]
        local("rm /data/web_static/releases/{}".format(filename))
        i += 1
