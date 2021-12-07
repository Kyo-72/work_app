from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess
import os
import time
from email_programs import *
from email_programs.address import email_resister

ADDRESS_FILE = "email_programs/address/email_address.txt"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///email.db'
db = SQLAlchemy(app)
#初期値
exe_date = "一日前"
exe_time = "22:00"
#プロセス初期化
cmd = "python email_programs/main.py {} {}".format(exe_date,exe_time)
p = subprocess.Popen(cmd.split(" "))

#サブプロセスを起動.
def inti_systems():
    return 0
    

@app.route('/',methods=["GET","POST"])
def index():
    #index.html
    global exe_date
    global exe_time
    global p

    #GEtなら現在の設定日時を表示する
    if request.method == "GET":
        return render_template("index.html",exe_date=exe_date,exe_time=exe_time)
        
    #POSTなら、設定時刻を更新してプロセスを再起動する
    else:
        exe_date = request.form.get("exe_day")
        exe_time = request.form.get("exe_time")
        #プロセスをキル、コマンドを再設定後、プロセスを再起動
        p.kill()
        cmd = "python email_programs/main.py {} {}".format(exe_date,exe_time)
        p = subprocess.Popen(cmd.split(" "))
        print(os.getcwd())

        return redirect("/")
        

@app.route("/add_email",methods=["GET","POST"])
def add_email():
    if request.method == "GET":
        #現在のメールアドレスと名前の情報を取得(info[name] = addres)
        info_dict = email_resister.read_file(ADDRESS_FILE)
        return render_template("add_email.html",info_dict=info_dict)
    else:
        #フォームから名前とメールアドレスを取得、txtファイルに書き込む
        last_name = str( request.form.get("last_name") )
        first_name = str( request.form.get("first_name") )

        email = str( request.form.get("email") )
        email_resister.add_info(ADDRESS_FILE,first_name,last_name,email)
        return redirect("/add_email")


        
"""
@app.route('/create',methods=["GET","POST"])
def create():
    #リクエストがGETかPOSTかでふるまいを変える
    if request.method == "POST":
        #formからtitleとbodyを追加
        title = request.form.get("title")
        body = request.form.get("body")

        #データベースをインスタンス化
        post = Post(title=title,body=body)
        #データベースを追加、コミット
        db.session.add(post)
        db.session.commit()

        return redirect('/')
    else:
        return render_template("create.html")
"""


