#!/usr/bin/python3
"""This script generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, using the
function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import exists


def do_pack():
    """This function generates a .tgz archive from the contents of
    the web_static folder of your AirBnB Clone repo.
    """
    local("mkdir -p versions")
    path = "versions/web_static_{}.tgz".format(
        datetime.now().strftime("%Y%m%d%H%M%S"))
    local("tar -cvzf {} ./web_static".format(path))
    if (exists(path)):
        return path
    return None
