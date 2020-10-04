from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()
# ---------------------------------------- [edit] ---------------------------------------- #
def create_app():
    app = Flask(__name__)

    app.config.from_object(config)

    # ORM
    db.init_app(app)
    migrate.init_app(app, db)
    # models 캐치
    from . import models

    # 블루프린트
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    app.register_blueprint(question_views.bp)
    app.register_blueprint(answer_views.bp)
    app.register_blueprint(auth_views.bp)

    # 필터 이후에 datetime 을 필터로 사용 할 수 있다. question.create_date|datetime
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime

    return app
# ---------------------------------------- [edit] ---------------------------------------- #