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

app = Flask(__name__)

ADDRESS_FILE = "email_programs/address/email_address.txt"
#dbのURLを設定
db_uri = os.environ.get('DATABASE_URL') or "postgresql://localhost/email"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
db = SQLAlchemy(app) 

#メールアドレス管理用DB
class Email(db.Model): 
    __tablename__ = "emails" 
    id = db.Column(db.Integer, primary_key=True) # 識別子（特に使わない）
    last_name = db.Column(db.String(), nullable=False) # 姓
    first_name = db.Column(db.String(), nullable=False) # 名
    email_address = db.Column(db.String(), nullable=False) # メールアドレス




#まいくらすのユーザーid/パスワード
# print("まいくらすのユーザid :",end="")
my_usr = "a"#input()
# print("まいくらすのpssword :",end="")
my_pass = "a"#input()
#gmailのadress/パスワード入力
# print("gmailのaddress :",end="")
gmail_address = "a"#input()
# print("gmailのpssword :",end="")
gmail_pass = "a"#input()

#サブプロセスを起動.
def inti_systems():
    return 0

print(gmail_address)
print(gmail_pass)

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
        #DBのすべてのクエリを取得
        emails = Email.query.all()
        return render_template("add_email.html",emails=emails)
    elif request.method == "POST":

         #インスタンス作成
        email = Email()

        #フォームから名前とメールアドレスを取得、txtファイルに書き込む
        email.last_name = str( request.form.get("last_name") )
        email.first_name = str( request.form.get("first_name") )

        email.email_address = str( request.form.get("email") )
        db.session.add(email)
        db.session.commit()
        return redirect("/add_email")

#メールアドレスを削除する
@app.route("/del_email",methods=["GET","POST"])
def del_email():
    if request.method == "GET":
        #DBのすべてのクエリを取得
        emails = Email.query.all()
        return render_template("del_email.html",emails=emails)
    else:
        #選択されたクエリをDBから削除する
        id = request.form["address"] 
        db.session.query(Email).filter_by(id=id).delete()
        db.session.commit()
        return redirect("/")

        



