from flask import Flask
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pytz
# import sys
# print(sys.version)
# print(sys.path)

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now(pytz.timezone('Asia/Tokyo')))


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        # List形式で取得される
        posts = Post.query.all()
        return render_template('index.html', posts=posts)


@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        title = request.form.get('title')
        body = request.form.get('body')

        post = Post(title=title, body=body)

        db.session.add(post)
        db.session.commit()

        return redirect('/')

    else:
        return render_template('create.html')


@app.route('/<int:id>/update', methods=['GET', 'POST'])
def update(id):
    post = Post.query.get(id)
    # あるアイテムの更新ボタンを押した場合。新規で更新画面へ移動
    if request.method == 'GET':
        return render_template('update.html', post=post)

    # 更新画面で更新内容入力後更新ボタンを押した場合。
    else:
        post.title = request.form.get('title')
        post.body = request.form.get('body')

        db.session.commit()

        return redirect('/')
