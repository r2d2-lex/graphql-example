from fabric.api import local, run, sudo, cd
from fabric.api import env
from fabric.contrib import files

USER = 'user9'
SERVER = 'devserver'
GITHUB = 'https://github.com/r2d2-lex/graphql-example.git'
PROJECT_DIR_NAME = 'graphql-example'
PROJECT_APP_NAME = 'gqlshop'

env.hosts = [USER+'@'+SERVER]
PROJECT_PATH = '/home/{user_name}/{project_name}'.format(user_name=USER, project_name=PROJECT_DIR_NAME)
NGINX_BACKUP_SITES = '/etc/nginx/sites-enabled/{app_name}.conf.bak'.format(app_name=PROJECT_APP_NAME)
NGINX_DEFAULT_SITE_PATH = '/etc/nginx/sites-enabled/default'
NGINX_APP_NAME = '/etc/nginx/sites-enabled/{app_name}.conf'.format(app_name=PROJECT_APP_NAME)
MANAGE_PY_PATH = '{project_dir_name}/{app_name}'.format(project_dir_name=PROJECT_DIR_NAME, app_name=PROJECT_APP_NAME)


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
        with cd(PROJECT_DIR_NAME):
            run('python3 -m venv venv')


def install_project_code():
    if not files.exists(PROJECT_PATH):
        run('git clone '+GITHUB)
    else:
        with cd(PROJECT_DIR_NAME):
            run('git pull')


def install_project_requirements():
    with cd(PROJECT_DIR_NAME):
        run('{project_path}/venv/bin/pip install -r requirements.txt --upgrade'.format(project_path=PROJECT_PATH))


def configure_uwsgi():
    sudo('python3 -m pip install uwsgi')
    sudo('mkdir -p /etc/uwsgi/sites')
    files.upload_template(
        'templates/uwsgi.ini',
        '/etc/uwsgi/sites/{app_name}.ini'.format(app_name=PROJECT_APP_NAME),
        use_sudo=True
    )
    files.upload_template('templates/uwsgi.service', '/etc/systemd/system/uwsgi.service', use_sudo=True)


def configure_nginx():
    if files.exists(NGINX_DEFAULT_SITE_PATH):
        sudo(NGINX_DEFAULT_SITE_PATH)
    files.upload_template(
        'templates/nginx.conf',
        NGINX_APP_NAME,
        use_sudo=True,
    )
    # Удаляет backup файл из директории nginx, чтобы не было ошибки конфигурации
    if files.exists(NGINX_BACKUP_SITES):
        sudo('rm '+NGINX_BACKUP_SITES)


def migrate_database():
    with cd(MANAGE_PY_PATH):
        run(PROJECT_PATH+'/venv/bin/python manage.py makemigrations')
        run(PROJECT_PATH+'/venv/bin/python manage.py migrate')


def create_super_user():
    with cd(MANAGE_PY_PATH):
        run(PROJECT_PATH+'/venv/bin/python manage.py createsuperuser')

def restart_all():
    sudo('systemctl daemon-reload')
    sudo('systemctl reload nginx')
    # journalctl -u uwsgi.service
    sudo('systemctl restart uwsgi')


def bootstrap():
    install_packages()
    install_project_code()
    create_venv()
    install_project_requirements()
    configure_uwsgi()
    configure_nginx()
    migrate_database()
    restart_all()
