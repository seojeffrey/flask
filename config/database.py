DB_USERNAME = 'developer'
DB_PASSWORD = 'devpassword'
DB_DEFAULT = 'developer'
DB_HOST = 'localhost'
DB_PORT = 25000

DB_POOL_SIZE = 20
DB_POOL_RECYCLE = 500
DB_MAX_OVERFLOW = 20


CONFIG_DATABASE_DB_URI = f'postgresql+psycopg2://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DEFAULT}'
