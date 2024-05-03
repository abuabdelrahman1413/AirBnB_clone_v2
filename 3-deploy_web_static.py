#!/usr/bin/python3
"""This module creates and distributes an archive
to your web servers, using the function deploy
"""
from fabric.api import *


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
    return Nonedef do_pack():
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
