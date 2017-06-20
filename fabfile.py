import random

from fabric.context_managers import settings
from fabric.contrib.files import upload_template, exists
from fabric.decorators import task
from fabric.operations import run, local, put
from fabric.state import env

random = random.SystemRandom()


def get_random_string(length=12,
                      allowed_chars='abcdefghijklmnopqrstuvwxyz'
                                    'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
    """
    Returns a securely generated random string.
 
    The default length of 12 with the a-z, A-Z, 0-9 character set returns
    a 71-bit value. log_2((26+26+10)^12) =~ 71 bits.
 
    Taken from the django.utils.crypto module.
    """
    return ''.join(random.choice(allowed_chars) for _ in range(length))


def get_secret_key():
    """
    Create a random secret key.
 
    Taken from the Django project.
    """
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return get_random_string(50, chars)


def escape_docker_strings(string):
    return string.replace('$', '$$')


@task
def install_docker_debian():
    with settings(warn_only=True):
        run('apt-get remove docker docker-engine')
    with settings(warn_only=True):
        result = run('dpkg-query -l "docker-ce" | grep -q ^.i')
    if result.failed:
        run('apt-get install apt-transport-https ca-certificates '
            'curl software-properties-common')
        run('curl -fsSL https://download.docker.com/linux/debian/gpg | '
            ' apt-key add -')
        run('add-apt-repository -y '
            '"deb [arch=amd64] https://download.docker.com/linux/debian '
            '$(lsb_release -cs) '
            'stable"')
        run('apt-get update -y')
        run('apt-get install -y docker-ce')
        # TODO rewrite when (if?) docker-compose is available in debian repo
        run(
            'curl -L "https://github.com/docker/compose/releases/download/1.11.2/docker-compose-$(uname -s)-$(uname -m)"'
            ' -o /usr/local/bin/docker-compose')
        run('chmod +x /usr/local/bin/docker-compose')
        run('systemctl enable docker')
        run('systemctl start docker')


@task
def build():
    docker_running = local('systemctl is-active docker')
    if docker_running == 'inactive':
        local('sudo systemctl start docker')
    local('docker-compose -f docker-compose.yml build')


@task
def upload():
    # TODO check if docker compose bundle is appropriate instead of copying docker-compose files
    local('docker image save easygoing -o easygoing.image')
    local('docker image save nginx-certbot -o nginx-certbot.image')
    run('mkdir -p ~/easygoing')
    run('mkdir -p ~/easygoing/nginx')
    put(local_path='docker-compose.yml', remote_path='~/easygoing/docker-compose.yml')
    put(local_path='easygoing.image', remote_path='~/easygoing/easygoing.image')
    put(local_path='nginx-certbot.image', remote_path='~/easygoing/nginx-certbot.image')
    local('rm easygoing.image')
    local('rm nginx-certbot.image')
    run('docker image load -i ~/easygoing/easygoing.image')
    run('docker image load -i ~/easygoing/nginx-certbot.image')
    run('rm ~/easygoing/easygoing.image')
    run('rm ~/easygoing/nginx-certbot.image')


def request_certificate(context):
    with settings(warn_only=True):
        run('docker stop helper')
        run('docker rm helper')
    run('docker run -d -v easygoing_nginx_conf_d:/conf.d/ -v easygoing_certificates_keys:/keys/'
        ' --name helper busybox tail -f /dev/null')
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml "
        "run nginx /bin/bash -c 'mkdir -p /var/easygoing/acme'")
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml down")
    # certbot certonly --staging for test certificates
    script = '''
    supervisord &
    supervisorctl start nginx &&
    certbot certonly --webroot -d {0} -w {1} --rsa-key-size 4096 --email {2} --verbose --noninteractive --agree-tos &&
    exit
    '''.format(context['fqdn'], '/var/easygoing/acme', context['admin_email'])
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml "
        "run --service-ports nginx /bin/bash -c '{}'".format(script))
    run('docker cp ~/easygoing/nginx.conf helper:/conf.d/{}.conf'.format(env.host))


@task
def create_user(email, username):
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml "
        "run gunicorn python manage.py createsuperuser --email {} --username {}".format(email, username))


@task
def setup(email, username):
    context = {'fqdn': env.host,
               'secret_key': escape_docker_strings(get_secret_key()),
               'admin_email': email.strip()}
    if not exists('~/easygoing/dhparam.pem'):
        local('openssl dhparam -out dhparam.pem 4096')
        put(local_path='dhparam.pem', remote_path='~/easygoing/dhparam.pem')
    with settings(warn_only=True):
        local('rm -f dhparam.pem')
    upload_template(filename='nginx/nginx.conf', destination='~/easygoing/nginx.conf', context=context, use_jinja=True)
    upload_template(filename='nginx/nginx-certbot.conf', destination='~/easygoing/nginx-certbot.conf', context=context,
                    use_jinja=True)
    upload_template(filename='docker-compose.prod.yml', destination='~/easygoing/docker-compose.prod.yml',
                    context=context, use_jinja=True)
    with settings(warn_only=True):
        run('docker stop helper')
        run('docker rm helper')
    run('docker run -d -v easygoing_nginx_conf_d:/conf.d/ -v easygoing_certificates_keys:/keys/'
        ' --name helper busybox tail -f /dev/null')
    run('docker cp ~/easygoing/nginx-certbot.conf helper:/conf.d/{}.conf'.format(env.host))
    run('docker cp ~/easygoing/dhparam.pem helper:/keys/dhparam.pem'.format(env.host))
    script = '''
    mkdir -p /var/easygoing/logs &&
    touch /var/easygoing/logs/gunicorn.log &&
    touch /var/easygoing/logs/nginx-access.log &&
    touch /var/easygoing/logs/nginx-error.log &&
    chown -R user:user /var/easygoing
    '''
    run("docker-compose -f ~/easygoing/docker-compose.yml  -f ~/easygoing/docker-compose.prod.yml "
        "run -u root gunicorn /bin/bash -c '{}'".format(script))
    script = '''
    python wait_for.py db 5432 &&
    python wait_for.py cache 6379 &&
    python manage.py migrate --noinput &&
    python manage.py collectstatic --noinput
    '''
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml "
        "run gunicorn /bin/bash -c '{}'".format(script))
    request_certificate(context)
    run('docker stop helper')
    run('docker rm helper')
    create_user(email, username)


@task
def update():
    # experimental - risky!
    build()
    down()
    upload()
    context = {'fqdn': env.host}
    upload_template(filename='nginx/nginx.conf', destination='~/easygoing/nginx.conf', context=context, use_jinja=True)
    # upload_template(filename='docker-compose.prod.yml', destination='~/easygoing/docker-compose.prod.yml',
    #                 context=context, use_jinja=True)
    script = '''
    python wait_for.py db 5432 &&
    python wait_for.py cache 6379 &&
    python manage.py migrate --noinput &&
    python manage.py collectstatic --noinput
    '''
    run("docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml "
        "run gunicorn /bin/bash -c '{}'".format(script))
    clear()

@task
def deploy(email, username):
    build()
    install_docker_debian()
    upload()
    setup(email, username)
    clear()


@task
def disable_webserver():
    run('systemctl disable nginx')
    run('systemctl stop nginx')


@task
def up():
    disable_webserver()
    run('/usr/local/bin/docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml up -d')


@task
def down():
    run('docker-compose -f ~/easygoing/docker-compose.yml -f ~/easygoing/docker-compose.prod.yml down')


@task
def clear():
    run('rm -f ~/easygoing/easygoing.image')
    local('rm -f easygoing.image')


@task
def purge_docker_debian():
    run('systemctl start docker')
    with settings(warn_only=True):
        run('docker stop $(docker ps -aq)')
        run('docker rm $(docker ps -aq)')
        run('docker rmi $(docker image ls -aq)')
        run('docker volume rm $(docker volume ls -q)')
    run('systemctl disable docker')
    run('systemctl stop docker')
    run('apt-get remove -y docker-ce')
    run('rm -f /usr/local/bin/docker-compose')
    run('add-apt-repository -r -y '
        '"https://download.docker.com/linux/debian"')


@task
def uninstall():
    with settings(warn_only=True):
        down()
        clear()
        run('docker image rm -f easygoing')
        run('docker image rm -f nginx-certbot')
        # run('docker volume rm -f easygoing_base_data')
        # run('docker volume rm -f easygoing_certificates')
        # run('docker volume rm -f easygoing_certificates_archive')
        # run('docker volume rm -f easygoing_certificates_keys')
        # run('docker volume rm -f easygoing_db_data')
        # run('docker volume rm -f easygoing_nginx_conf_d')
        run('rm -rf ~/easygoing')
        purge_docker_debian()
