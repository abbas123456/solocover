import sys
import time
from fabric.api import sudo, local, put


try:
    from fabconfig import *
except ImportError:
    print "You need to define a fabconfig.py file with your project settings"
    sys.exit()

def build_images():
    notify("Building docker images")
    local('git checkout %s' % env.tag)
    local('cp .docker/db/Dockerfile .')
    local('docker build -t %(registry)s/vanspr_db:%(tag)s .' % env)
    local('cp .docker/app/Dockerfile .')
    local('docker build -t %(registry)s/vanspr_app:%(tag)s .' % env)
    local('git checkout -')

def push_images():
    notify("Pushing images to registry")
    local('docker push %(registry)s/vanspr_db:%(tag)s' % env)
    local('docker push %(registry)s/vanspr_app:%(tag)s' % env)

def pull_app_image():
    notify("Pulling app image from registry")
    sudo('docker pull %(registry)s/vanspr_app:%(tag)s' % env)

def pull_db_image():
    notify("Pulling db image from registry")
    sudo('docker pull %(registry)s/vanspr_db:%(tag)s' % env)

def run_app_container():
    notify("Running app containers")
    sudo(env.app_run_command)

def run_db_container():
    notify("Running db containers")
    sudo(env.db_run_command)

def deploy_nginx_config():
    notify("Deploying nginx config")
    put('deploy/nginx.tpl', 'nginx.tpl')
    put('deploy/htpasswd', 'htpasswd')
    sudo('mv nginx.tpl %(nginx_config)s' % env)
    sudo('cp htpasswd /etc/nginx/')
    sudo("sed -i 's#{{ public_folder }}#%(public_folder)s#g' %(nginx_config)s" % env)
    sudo("sed -i 's#{{ uwsgi_port }}#%(uwsgi_port)s#g' %(nginx_config)s" % env)
    sudo("sed -i 's#{{ server_name }}#%(server_name)s#g' %(nginx_config)s" % env)
    sudo("/etc/init.d/nginx reload")

def post_deployment():
    notify("Migrating and collecting static")
    # This is necessary to give the db container enough time to start
    time.sleep(2)
    sudo('%s %s' % (env.adhoc_command, 'make install'))

def adhoc_command():
    notify("Running adhoc command")
    command = prompt(red('Enter command you wish to execute on app container'))
    sudo('%s %s' % (env.adhoc_command, command))

def build():
    build_images()

def push():
    push_images()

def deploy():
    pull_db_image()
    pull_app_image()
    run_db_container()
    run_app_container()
    post_deployment()
    deploy_nginx_config()