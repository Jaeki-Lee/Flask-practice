from datetime import datetime

from flask import Blueprint, url_for, request, render_template
from werkzeug.utils import redirect

from pybo import db
from ..forms import AnswerForm
from pybo.models import Question, Answer

bp = Blueprint('answer', __name__, url_prefix='/answer')

@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        # html file 의 textArea 의 content 키로 되어있는
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now())
        # Question 과 Answer 은 relationship 으로 연결되어 있기때문에 backref 인 answer_set 을 사용할 수 있다.
        # db.session.add(answer) 과 같다
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)