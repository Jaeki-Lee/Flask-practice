from flask import Blueprint, url_for, render_template, flash, request, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect

from pybo import db
from pybo.forms import UserCreateForm, UserLoginForm
from pybo.models import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

# 라우트 함수 실행전에 항상 먼저 실행된다.
@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    # g변수는 플라스크가 제공하는 컨텍스트 변수로 request변수와 마찬가지로 요청과 응답이라는 한 사이클에서만 유효한 컨텍스트 변수이다.
    # 이렇게 하면 이제 사용자가 로그인이 되었는지 체크하기 위해서 session을 찾을 필요없이 g.user에 값이 있는지만 조사하면 될 것
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.get(user_id)

@bp.route('/signup/', methods=('GET', 'POST'))
def signup():
    form = UserCreateForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user:
            user = User(username=form.username.data, password=generate_password_hash(form.password1.data), email=form.email.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.index'))
        else:
            flash('이미 존재하는 사용자입니다.')

    return render_template('auth/signup.html', form=form)

@bp.route('/login/', methods=('GET', 'POST'))
def login():
    form = UserLoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        error = None
        user = User.query.filter_by(username=form.username.data).first()
        print(user)
        print(form.username)
        if not user:
            error = "존재하지 않는 사용자 입니다."
        elif not check_password_hash(user.password, form.password.data):
            error = "비밀번호가 올바르지 않습니다."
        if error is None:
            # 플라스크 세션(session)에 user_id라는 키에 조회된 사용자의 id값을 저장한다. 세션은 request와 마찬가지로 플라스크가 자동으로 생성하여 제공하는 변수이다.
            # 세션은 플라스크 메모리에 저장되기 때문에 플라스크 서버가 구동중인 동안에는 영구적으로 사용할 수 있는 값이다
            # 세션은 영구적이지만 타임아웃이 설정되어 있어서 타임아웃 시간동안 접속이 없으면 세션정보가 삭제된다.
            # session 변수에 User의 id값을 저장하면 브라우저 요청이 발생할 경우 이 세션값으로 사용자가 로그인한 사용자인지 아닌지를 판별할 수 있게 된다.
            # 그리고 세션(session)은 이 쿠키당 하나씩 생성되는 서버의 메모리 공간이라고 할 수 있다.
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('main.index'))
        flash(error)
    return render_template('auth/login.html', form=form)

@bp.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('main.index'))
