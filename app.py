from flask import Flask
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess
import os
import time
from email_programs import *
from email_programs.address import email_resister
# my_usr = ""
# my_pass = ""
# gmail_address = ""
# gmail_pass = ""

ADDRESS_FILE = "email_programs/address/email_address.txt"


#まいくらすのユーザーid/パスワード
print("まいくらすのユーザid :",end="")
my_usr = input()
print("まいくらすのpssword :",end="")
my_pass = input()
#gmailのadress/パスワード入力
print("gmailのaddress :",end="")
gmail_address = input()
print("gmailのpssword :",end="")
gmail_pass = input()

#サブプロセスを起動.
def inti_systems():
    return 0

print(gmail_address)
print(gmail_pass)
app = Flask(__name__)
#初期値
exe_date = "一日前"
exe_time = "22:00"
#プロセス初期化
cmd = "python email_programs/main.py {} {} {} {} {} {}".format(exe_date,exe_time,my_usr,my_pass,gmail_address,gmail_pass)
p = subprocess.Popen(cmd.split(" "))


    

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
        cmd = "python email_programs/main.py {} {} {} {} {} {}".format(exe_date,exe_time,my_usr,my_pass,gmail_address,gmail_pass)
        p = subprocess.Popen(cmd.split(" "))
        print(os.getcwd())

        return redirect("/")
        
#メールアドレスを追加する
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

#メールアドレスを削除する
@app.route("/del_email",methods=["GET","POST"])
def del_email():
    if request.method == "GET":
        #現在のメールアドレスと名前の情報を取得(info[name] = addres)
        info_dict = email_resister.read_file(ADDRESS_FILE)
        return render_template("del_email.html",info_dict=info_dict)
    else:
        #選択されたアドレスを削除する
        address = request.form["address"] 
        
        email_resister.del_info(ADDRESS_FILE,address)
        return redirect("/")

        
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


