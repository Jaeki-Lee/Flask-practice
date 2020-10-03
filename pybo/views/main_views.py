from flask import Blueprint, url_for
from werkzeug.utils import redirect

bp = Blueprint('main', __name__, url_prefix='/')

@bp.route('/hello')
def hello_pybo():
    return 'Hello, Pybo!'

@bp.route('/')
def index():
    # question 객체가 없는데 어떻게 인식을 하지? -> question_views 의 bp 객체의 이름이 question
    return redirect(url_for('question._list'))

