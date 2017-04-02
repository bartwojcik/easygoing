from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import run, local

from dockerfabric.tasks import install_socat


@task
def install_docker_debian(skip_group_assignment=False):
    with settings(warn_only=True):
        run('apt-get remove docker docker-engine')
    run('apt-get install apt-transport-https ca-certificates '
         'curl software-properties-common')
    run('curl -fsSL https://download.docker.com/linux/debian/gpg | '
         ' apt-key add -')
    run('add-apt-repository '
         '"deb [arch=amd64] https://download.docker.com/linux/debian '
         '$(lsb_release -cs) '
         'stable"')
    run('apt-get update -y')
    run('apt-get install -y docker-ce')


@task
def install_socat_debian():
    run('apt-get install -y socat')

@task
def build():
    local('docker-compose -f release-docker-compose.yml build')



@task
def deploy_production():
    install_docker_debian()
    install_socat_debian()
    build()

