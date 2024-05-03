#!/usr/bin/python3
"""This script generates a .tgz archive from the contents of
the web_static folder of your AirBnB Clone repo, using the
function do_pack
"""
from fabric.api import *
from datetime import datetime
from os.path import exists


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
    if not (exists(archive_path)):
        return False
    name_tgz = archive_path.split('/')[1]
    name_notgz = name_tgz.split('.')[0]
    put(archive_path, "/tmp/{}".format(name_tgz))
    sudo("rm -rf /data/web_static/releases/{}".format(name_notgz))
    sudo("mkdir -p /data/web_static/releases/{}".format(name_notgz))
    sudo("tar -xzf /tmp/{} -C /data/web_static/releases/{}".format(
        name_tgz, name_notgz))
    sudo("rm /tmp/{}".format(name_tgz))
    sudo(("mv -f /data/web_static/releases/{}/web_static/* " +
          "/data/web_static/releases/{}/").format(name_notgz, name_notgz))
    sudo("rm -rf /data/web_static/releases/{}/web_static/".format(
        name_notgz))
    sudo("rm -rf /data/web_static/current")
    sudo("ln -sf /data/web_static/releases/{} /data/web_static/current"
         .format(name_notgz))
    return True
