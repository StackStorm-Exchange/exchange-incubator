from __future__ import with_statement
from fabric.api import local, lcd


def local_cmd(loc, dest="/opt/stackstorm/packs/boto3"):
    local("cp -rv {0}/* {1}/{0}".format(loc, dest))


def vpc():
    with lcd('/root/stackstorm-boto3'):
        local_cmd(loc='actions')


def pack_install():
    with lcd('/root/stackstorm-boto3'):
        local('rm -rf /opt/stackstorm/virtualenvs/boto3')
        local('st2 pack install file:///$PWD')
