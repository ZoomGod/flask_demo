from flask import Flask, render_template, request, redirect, url_for, session, g
from models import User, Question, Answer
from exts import db
from decorators import login_required
import config
import pymysql
pymysql.install_as_MySQLdb()


app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by(Question.create_time.desc()).all()
    }
    return render_template('index.html', **context)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        user = User.query.filter(User.telephone == telephone).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            # 31天无需重复登录(session持久化)
            session.permanent = True

            return redirect(url_for('index'))
        else:
            return '手机号或密码有错'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password = request.form.get('password')
        password_check = request.form.get('password_check')

        # 判断手机号是否已经存在
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return '手机号已被注册!'
        else:
            # 确认两次密码输入一致
            if password != password_check:
                return '两次密码不一致，请重新确认'
            else:
                user = User(telephone=telephone, username=username, password=password)
                db.session.add(user)
                db.session.commit()
                # 注册成功，跳转至登录界面
                return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.pop('user_id')
    # del session['user_id']
    session.clear()
    return redirect(url_for('login'))


@app.route('/question', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title, content=content)

        # user_id = session.get('user_id')
        # user = User.query.filter(User.id == user_id).first()

        question.author = g.user
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))


@app.route('/detail/<question_id>')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()
    return render_template('detail.html', question=question_model)


@app.route('/add_answer', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content, question_id=question_id)

    # user_id = session.get('user_id')
    # user = User.query.filter(User.id == user_id).first()

    answer.author = g.user
    questions = Question.query.filter(Question.id == question_id).first()
    answer.question = questions
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail', question_id=question_id))


@app.route('/search/')
def search():
    q = request.args.get('q')
    # title OR content
    questions = Question.query.filter(Question.title.contains(q) | Question.content.contains(q))
    return render_template('index.html', questions=questions)


@app.before_request
def my_before_request():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            g.user = user


@app.context_processor
def my_context_processor():
    if hasattr(g, 'user'):
        return {'user': g.user}
    return {}


if __name__ == '__main__':
    app.run()




