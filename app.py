#!/usr/bin/env python3
from flask import Flask, request, Response, abort, render_template
from flask_login import LoginManager, login_user, logout_user, login_required, UserMixin
from collections import defaultdict

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = "secret"

class User(UserMixin):
    def __init__(self, id, name, password):
        self.id = id
        self.name = name
        self.password = password

# ログイン用ユーザー作成
users = {
    1: User(1, "user01", "password"),
    2: User(2, "user02", "password"),
    3: User(3, "yorii", "seito")
}

# ユーザーチェックに使用する辞書作成
nested_dict = lambda: defaultdict(nested_dict)
user_check = nested_dict()
for i in users.values():
    user_check[i.name]["password"] = i.password
    user_check[i.name]["id"] = i.id

@login_manager.user_loader
def load_user(user_id):
    return users.get(int(user_id))

@app.route('/')
def home():
    return Response("ログインから入室してください。: <a href='/login/'>ログイン</a> <a href='/logout/'>ログアウト</a>")

# ログインしないと表示されないパス
@app.route('/protected/')
@login_required
def protected():
    return Response('''
    protected<br />
    <a href="/logout/">ログアウト</a>
    ''')

# ログインパス
@app.route('/login/', methods=["GET", "POST"])
def login():
    if(request.method == "POST"):
        # ユーザーチェック
        if(request.form["username"] in user_check and request.form["password"] == user_check[request.form["username"]]["password"]):
            # ユーザーが存在した場合はログイン
            login_user(users.get(user_check[request.form["username"]]["id"]))
            return Response('''
            ログイン中<br />
            <a href="https://sites.google.com/view/r3-yoriidoyojuku/%E3%83%9B%E3%83%BC%E3%83%A0">よりE土曜塾・英検対策講座サイトへ</a><br />
            <a href="/logout/">ログアウト</a>
            ''')
        else:
            return abort(401)
    else:
        return render_template("login.html")

# ログアウトパス
@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return Response('''
    ログアウトしました<br />
    <a href="/login/">ログイン</a>
    ''')

if __name__ == '__main__':
    #app.run(host="0.0.0.0",port=8080,debug=True)
    app.run()