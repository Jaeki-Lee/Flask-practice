from datetime import datetime

from flask import Blueprint, render_template, request, url_for
from werkzeug.utils import redirect

from .. import db
from pybo.models import Question
from ..forms import QuestionForm, AnswerForm

bp = Blueprint('question', __name__, url_prefix='/question')

# _list 인 이유는 파이썬에 list 라는 함수명이 있음
@bp.route('/list')
def _list():
    # url 에서 page 를 가져온다 기본값 1
    page = request.args.get('page', type=int, default=1)
    question_list = Question.query.order_by(Question.create_date.desc())
    question_list = question_list.paginate(page, per_page=10)
    # main_views 에 이어서 url_for 함수를 list.html 에서 사용 가능하다.
    return render_template('question/question_list.html', question_list=question_list)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# GET과 POST에 의해 템플릿이 렌더링되고 데이터가 저장되는 메커니즘을
@bp.route('/create/', methods=('GET', 'POST'))
def create():
    # get 을 이용해 질문등록 화면이 호출
    form = QuestionForm()
    # 저장하기 버튼을 클릭하여 post 호출  <button type="submit" class="btn btn-primary">저장하기</button>
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now())
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('main.index'))
    # 이곳에서 question_form 을 불러와 덮어주고, 함수 호출 권한은 여전히 question_list 의 질문등록에 있다.
    return render_template('question/question_form.html', form=form)