import sys

from fabric.api import env, local, settings
from fabric.operations import prompt
from fabric.colors import red, green

def message(msg, colour):
    bar = '+' + '-' * (len(msg) + 2) + '+'
    print colour('')
    print colour(bar)
    print colour("| %s |" % msg)
    print colour(bar)
    print colour('')

def error(msg):
    message(msg, red)

def notify(msg):
    message(msg, green)

def _general_setup():
    tag = prompt(red('Enter git tag to build'))
    with settings(warn_only=True):
        result = local('git diff --exit-code')
        result1 = local('git diff --cached --exit-code')
        result2 = local('git ls-files --other --exclude-standard --directory', capture=True)
        if any((result.return_code==1, result1.return_code==1, result2!="")):
            error("Unclean copy")
            sys.exit()
    env.tag = local('git describe --exact-match %s' % tag, capture=True)
    env.registry = 'abbas123456'

def localhost():
    _general_setup()

def live():
    _general_setup()
    hostname = 'ec2-54-77-192-73.eu-west-1.compute.amazonaws.com'
    env.hosts=[hostname]
    env.user = 'ubuntu'
    env.nginx_config = '/etc/nginx/sites-enabled/default'
    env.public_folder = '/var/django-projects/vanspr_public'
    env.uwsgi_port = '49153'
    env.server_name = hostname
    env.settings_file = 'conf.ec2_test'
    env.app_run_command = ('docker rm -f appserver memcached;'
                       'docker run -d --name memcached %(registry)s/memcached &&'
                       'docker run -d -e DJANGO_SETTINGS_MODULE=%(settings_file)s -p %(uwsgi_port)s:8000 --name appserver --link memcached:memcached --link dbserver:dbserver '
                       '-v %(public_folder)s:/var/django-projects/vanspr/public %(registry)s/vanspr_app:%(tag)s' % env)
    env.db_run_command = ('docker rm -f mysql_data dbserver;'
                       'docker run --name mysql_data -v ~/Documents/vanspr_mysql:/var/lib/mysql busybox true && '
                       'docker run -d --name dbserver -p 3306:3306 --volumes-from mysql_data %(registry)s/vanspr_db:%(tag)s' % env)
    env.adhoc_command = ('docker run -e DJANGO_SETTINGS_MODULE=%(settings_file)s -t -i --rm --link dbserver:dbserver -v %(public_folder)s:/var/django-projects/vanspr/public %(registry)s/vanspr_app:%(tag)s' % env)
    env.key_filename = '/home/mohammad/Downloads/docker-server.pem'