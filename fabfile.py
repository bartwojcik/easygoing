from fabric.context_managers import settings
from fabric.decorators import task
from fabric.operations import run, local, put


@task
def install_docker_debian(skip_group_assignment=False):
    with settings(warn_only=True):
        run('apt-get remove docker docker-engine')
    with settings(warn_only=True):
        result = run('dpkg-query -l "docker-ce" | grep -q ^.i')
    if result.failed:
        run('apt-get install apt-transport-https ca-certificates '
            'curl software-properties-common')
        run('curl -fsSL https://download.docker.com/linux/debian/gpg | '
            ' apt-key add -')
        run('add-apt-repository -y'
            '"deb [arch=amd64] https://download.docker.com/linux/debian '
            '$(lsb_release -cs) '
            'stable"')
        run('apt-get update -y')
        run('apt-get install -y docker-ce')
        # TODO change when (if?) docker-compose is available in debian repo
        run(
            'curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)"'
            ' -o /usr/local/bin/docker-compose')
        run('chmod +x /usr/local/bin/docker-compose')
        run('systemctl enable docker')
        run('systemctl start docker')


@task
def build():
    local('docker-compose -f docker-compose.yml build')


@task
def upload():
    # TODO check if docker compose bundle is appropriate instead of copying docker-compose file
    local('docker image save easygoing -o easygoing.image')
    run('mkdir -p ~/easygoing')
    put(local_path='docker-compose.yml', remote_path='~/easygoing/docker-compose.yml')
    put(local_path='easygoing.image', remote_path='~/easygoing/easygoing.image')
    local('rm easygoing.image')
    run('docker image import ~/easygoing/easygoing.image easygoing:latest')
    run('rm ~/easygoing/easygoing.image')


@task
def deploy_production():
    build()
    install_docker_debian()
    # install_socat_debian()
    upload()
    # TODO tu skonczylem
    script = '''
    gunicorn mkdir -p /var/easygoing/logs &&
    touch /var/easygoing/logs/gunicorn.log &&
    touch /var/easygoing/logs/nginx-access.log &&
    touch /var/easygoing/logs/nginx-error.log &&
    chown -R user:user /var/easygoing &&
    python wait_for.py db 5432 &&
    python wait_for.py cache &&
    python manage.py migrate &&
    python manage.py collectstatic
    '''
    run("docker-compose run -u root gunicorn {}".format(script))




@task
def disable_webserver():
    run('systemctl disable nginx')
    run('systemctl stop nginx')


@task
def up():
    disable_webserver()
    run('/usr/local/bin/docker-compose -f ~/easygoing/docker-compose.yml up -d')


@task
def down():
    run('docker-compose -f ~/easygoing/docker-compose.yml down')


@task
def remove():
    down()
    run('docker image rm easygoing')
    run('rm -rf ~/easygoing')

@task
def uninstall_docker_debian():
    run('docker rm $(docker ps -aq)')
    run('docker rmi $(docker image ls -aq)')
    run('docker volume rm $(docker volume ls -q)')
    run('systemctl disable docker')
    run('systemctl stop docker')
    run('apt-get uninstall -y docker-ce')
    run('rm /usr/local/bin/docker-compose')
    run('add-apt-repository -r -y'
        '"deb [arch=amd64] https://download.docker.com/linux/debian '
        '$(lsb_release -cs) '
        'stable"')

@task
def clean():
    down()
    remove()
    uninstall_docker_debian()
