from dotenv import load_dotenv

_env_file = '/srv/env/waitress.env'
load_dotenv(_env_file)

bind = '0.0.0.0:8848'
chdir = '/srv/waitress'
pidfile = '/srv/run/waitress.pid'

workers = 1
worker_class = 'gthread'   # 启用多线程
threads = 100              # 单 worker 开启 100 线程

errorlog = '/srv/logs/gunicorn.log'
