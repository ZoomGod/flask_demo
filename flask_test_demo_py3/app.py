from flask import Flask, render_template, request, redirect, url_for, session
from models import User, Question
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

        user = User.query.filter(User.telephone == telephone, User.password == password).first()
        if user:
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
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()

        return redirect(url_for('index'))
 

@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return {'user': user}
    return {}


if __name__ == '__main__':
    app.run()




