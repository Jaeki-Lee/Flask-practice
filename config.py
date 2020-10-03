import os

# /myproject
BASE_DIR = os.path.dirname(__file__)

# /myproject 하위
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Flask-WTF를 사용하기 위해서는 플라스크 환경변수 SECRET_KEY가 필요
SECRET_KEY = 'dev'