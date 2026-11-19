from dotenv import load_dotenv

env_file = '/srv/env/sync-api.env'
load_dotenv(env_file)

bind = '0.0.0.0:8848'
chdir = '/srv/sync-api'
pidfile = '/srv/run/sync-api.pid'

workers = 1
worker_class = 'gthread'   # 启用多线程
threads = 20              # 单 worker 开启 20 线程

errorlog = '/srv/logs/gunicorn.log'
