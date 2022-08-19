from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_programs import main


#DB

app = Flask(__name__)
#dbのURLを設定
db_uri = "postgresql://ucluwtkwtninbh:17c5b354b389b5dc03de208ee3b4e3e0037090e8626e2d7407f444ccb9c3bc8a@ec2-23-23-182-238.compute-1.amazonaws.com:5432/d94kl4sbb8v1ka" or "postgresql://localhost/email"
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
db = SQLAlchemy(app) 

#メールアドレス管理用DB
class Email(db.Model): 
    __tablename__ = "emails" 
    id = db.Column(db.Integer, primary_key=True) # 識別子（特に使わない）
    last_name = db.Column(db.String(), nullable=False) # 姓
    first_name = db.Column(db.String(), nullable=False) # 名
    email_address = db.Column(db.String(), nullable=False) # メールアドレス

class Config(db.Model): 
    __tablename__ = "configs" 
    id = db.Column(db.Integer, primary_key=True) # 識別子（特に使わない）
    exe_date = db.Column(db.Integer(), nullable=False) # メール送信日 0:当日，1:前日，2:2二日前
    exe_hour = db.Column(db.Integer(), nullable=False) # メール送信時間（時間）
    exe_min = db.Column(db.Integer(), nullable=False) # メール送信時間（分）
    
#設定情報をdbから持ってくる
config = db.session.query(Config).filter_by(id=2).first()
exe_date = config.exe_date
exe_hour = config.exe_hour
exe_min = config.exe_min

# exe_date = 1
# exe_hour = 22
# exe_min = 0

 #main.pyをたたく
def task():
    
    #dbからメールアドレスを取る
    email_address = Email.query.all()
    email_dicts = {}
    for email in email_address:
        name = email.last_name + " " + email.first_name
        email_dicts[name] = email.email_address
        
    print(email_dicts)

    main.execute_email_jobs(exe_date,email_dicts)
    print("タスク実行されたな")

def schedule_init():
    #スケジューラをインスタンス化
    sched = BackgroundScheduler(daemon=True)
    #定期実行の時間設定
    sched.add_job(
        task, 'cron', hour=exe_hour, minute=exe_min
    )
    #スケジューラ スタート
    sched.start()

    return sched

#スケジューラを初期化
sched = schedule_init()

#サブプロセスを起動.
def inti_systems():
    return 0
    
@app.route('/',methods=["GET","POST"])
def index():
    #index.html
    global sched
    global exe_date
    global exe_hour
    global exe_min

    #GEtなら現在の設定日時を表示する
    if request.method == "GET":
        config = db.session.query(Config).filter_by(id=2).first()
        exe_date = config.exe_date
        exe_hour = config.exe_hour
        exe_min = config.exe_min

        return render_template("index.html",exe_date=exe_date,exe_hour=exe_hour,exe_min=exe_min )
        
    #POSTなら、設定時刻を更新してスケジューラをシャットダウン，タスクを追加後，起動
    else:

        config = db.session.query(Config).filter_by(id=2).first()
        
        exe_date = int ( request.form.get("exe_date") )
        #hh:mm形式で時間を取得
        exe_time =  request.form.get("exe_time") 
        #TODO　正しくスプリットできなかった際のエラー処理を書くべき
        time = exe_time.split(":")
        exe_hour = int( time[0] )
        exe_min = int( time[1] )
        #現在稼働しているタスクを強制終了
        sched.shutdown(wait=False)
        #タスクを再設定
        sched = schedule_init()

        config.exe_hour = exe_hour
        config.exe_min = exe_min
        config.exe_date = exe_date

        db.session.commit()
        db.session.close()
        



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
        db.session.close()
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
        db.session.close()
        return redirect("/del_email")


        



