#!/usr/bin/python3
"""This module creates and distributes an archive
to your web servers, using the function deploy
"""
from fabric.api import *
from datetime import datetime
from os.path import exists, isfile


env.hosts = ['54.157.148.186', '54.158.189.0']
env.user = 'ubuntu'


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


def do_deploy(archive_path):
    """This function distributes an archive to your web servers.
    """
    if (isfile(archive_path) is False):
        return False
    name_tgz = archive_path.split('/')[-1]
    name_notgz = name_tgz.split('.')[0]
    task = put(archive_path, "/tmp/")
    if task.failed is True:
        return False
    task = run("rm -rf /data/web_static/releases/{}/".format(name_notgz))
    if task.failed is True:
        return False
    task = run("mkdir -p /data/web_static/releases/{}/".format(name_notgz))
    if task.failed is True:
        return False
    task = run("tar -xzf /tmp/{} -C /data/web_static/releases/{}/".format(
        name_tgz, name_notgz))
    if task.failed is True:
        return False
    task = run("rm /tmp/{}".format(name_tgz))
    if task.failed is True:
        return False
    task = run(("mv /data/web_static/releases/{}/web_static/* " +
                "/data/web_static/releases/{}/").format(
                    name_notgz, name_notgz))
    if task.failed is True:
        return False
    task = run("rm -rf /data/web_static/releases/{}/web_static".format(
        name_notgz))
    if task.failed is True:
        return False
    task = run("rm -rf /data/web_static/current")
    if task.failed is True:
        return False
    task = run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
               .format(name_notgz))
    if task.failed is True:
        return False
    return True


def deploy():
    """This function created and distributes an architec to my web servers.
    """
    path = do_pack()
    if path is None:
        return False
    return do_deploy(archive_path=path)
