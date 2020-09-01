from fabric.api import local, run, sudo, cd
from fabric.api import env
from fabric.contrib import files

USER = 'user9'
SERVER = 'devserver'
GITHUB = 'https://github.com/r2d2-lex/graphql-example.git'
PROJECT_NAME = 'graphql-example'

env.hosts = [USER+'@'+SERVER]
PROJECT_PATH = '/home/{user_name}/{project_name}'.format(user_name=USER, project_name=PROJECT_NAME)


def hello():
    local('hello')


def who():
    run('who')


def install_packages():
    packages = [
        'python3-pip',
        'python3-dev',
        'python3-venv',
        'nginx',
        'git-core',
    ]
    sudo('apt-get install -y {}'.format(' '.join(packages)))


def create_venv():
    if not files.exists(PROJECT_PATH+'/venv'):
        with cd(PROJECT_NAME):
            run('python3 -m venv venv')


def install_project_code():
    if not files.exists(PROJECT_PATH):
        run('git clone '+GITHUB)
    else:
        with cd(PROJECT_NAME):
            run('git pull')


def install_project_reqirements():
    with cd(PROJECT_NAME):
        run('{project_path}/venv/bin/pip install -r requirements.txt --upgrade'.format(project_path=PROJECT_PATH))


def configure_uwsgi():
    sudo('python3 -m pip install uwsgi')
    sudo('mkdir -p /etc/uwsgi/sites')
    files.upload_template('templates/uwsgi.ini', '/etc/uwsgi/sites/gqlshop.ini', use_sudo=True)
    files.upload_template('templates/uwsgi.service', '/etc/systemd/system/uwsgi.service', use_sudo=True)


def configure_nginx():
    pass


def migrate_database():
    pass


def restart_all():
    pass


def bootstrap():
    install_packages()
    install_project_code()
    create_venv()
    install_project_reqirements()
    configure_uwsgi()
    configure_nginx()
    migrate_database()
    restart_all()
