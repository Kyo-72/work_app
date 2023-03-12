import os
import enum
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_programs import main

from sqlalchemy.types import Float,Boolean
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import DateTime,Date,Enum
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import exists


#DB

app = Flask(__name__)
#dbのURLを設定
db_uri = os.environ.get('DATABASE_URL') or "postgres://postgres:postgres@localhost/work_app"
db_uri = db_uri.replace("://", "ql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
db = SQLAlchemy(app) 


class Event_type(str,enum.Enum):
    open = "open"
    deliverd = "deliverd"
    proccessed = "proccessed"

#メールアドレス管理用DB
class Config(db.Model): 
    __tablename__ = "configs" 
    id = db.Column(db.Integer, primary_key=True) # 識別子（特に使わない）
    exe_date = db.Column(db.Integer(), nullable=False) # メール送信日 0:当日，1:前日，2:2二日前
    exe_hour = db.Column(db.Integer(), nullable=False) # メール送信時間（時間）
    exe_min = db.Column(db.Integer(), nullable=False) # メール送信時間（分）

class Branch(db.Model):
    __tablename__ = "branches"
    id = db.Column(db.Integer, primary_key=True) # id
    name = db.Column(db.String, nullable=False) #支店の名前
    teachers = relationship("Teacher")

class Teacher(db.Model):
    __tablename__ = "teachers"
    id = db.Column(db.Integer, primary_key=True) 
    last_name = db.Column(db.String(), nullable=False) # 姓
    first_name = db.Column(db.String(), nullable=False) # 名前
    email_address = db.Column(db.String(), nullable=False) # メールアドレス
    grade = db.Column(db.Integer, nullable=False) #学年（学生以外は0）
    branch_id = Column("branch_id", Integer(), ForeignKey('branches.id',onupdate='CASCADE'))
    mail_histories = relationship("Activity_history")


class Mail_history(db.Model):
    __tablename__ = "mail_histories"
    x_id = db.Column(db.String, primary_key=True) # 送信されたメールごとの識別子
    work_date = db.Column(db.Date,nullable=True)
    created_at = Column(DateTime, nullable=True, server_default=current_timestamp())
    activity_histories = relationship("Activity_history")
    
    
class Activity_history(db.Model):
     __tablename__ = "activity_histories"
     id = db.Column(db.Integer, primary_key=True) # id
     teachers_id = Column("teachers_id",Integer(),ForeignKey('teachers.id',onupdate='CASCADE'))
     x_id = Column("x_id",db.String,ForeignKey('mail_histories.x_id',onupdate='CASCADE'))
     time_record = Column(DateTime, nullable=False)
     #0 proccessed 1 deliverd, 2 open
     event_type = Column(Enum(Event_type),nullable=False)
    
    
#設定情報をdbから持ってくる
with app.app_context():
    config = db.session.query(Config).filter_by(id=1).first()

print(config)
exe_date = config.exe_date
exe_hour = config.exe_hour
exe_min = config.exe_min



#main.pyをたたく
def task():
    teachers = []
    #dbからメールアドレスを取る
    with app.app_context():
     teachers = Teacher.query.all()
    email_dicts = {}
    for teacher in teachers:
        name = teacher.last_name + " " + teacher.first_name
        email_dicts[name] = teacher.email_address
    print(email_dicts)

    x_id = main.execute_email_jobs(exe_date,email_dicts)
    print("次はここを見るねん")
    print(x_id)


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

    
@app.route('/',methods=["GET","POST"])
def index():
    #index.html
    global sched
    global exe_date
    global exe_hour
    global exe_min

    #GEtなら現在の設定日時を表示する
    if request.method == "GET":
        config = db.session.query(Config).filter_by(id=1).first()
        exe_date = config.exe_date
        exe_hour = config.exe_hour
        exe_min = config.exe_min

        return render_template("index.html",exe_date=exe_date,exe_hour=exe_hour,exe_min=exe_min )
        
    #POSTなら、設定時刻を更新してスケジューラをシャットダウン，タスクを追加後，起動
    else:

        config = db.session.query(Config).filter_by(id=1).first()
        
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
        
#講師情報を追加する
@app.route("/add_teachers_info",methods=["GET","POST"])
def add_teachers_info():
   
    if request.method == "GET":
        #DBのすべてのクエリを取得
        teachers = Teacher.query.all()
        branches = Branch.query.all()
        return render_template("add_teachers_info.html",teachers=teachers,branches=branches)
    elif request.method == "POST":

         #インスタンス作成
        teacher = Teacher()

        #フォームから講師情報を取得
        teacher.last_name = str( request.form.get("last_name") )
        teacher.first_name = str( request.form.get("first_name") )
        teacher.grade = int( request.form.get("grade") )
        print(teacher.grade)
        teacher.branch_id =  int( request.form.get("branch_selection") )
        teacher.email_address = str( request.form.get("email") )

        db.session.add(teacher)
        db.session.commit()
        db.session.close()
        return redirect("/add_teachers_info")

        
#TODO 講師情報を変更する

#メールアドレスを削除する
@app.route("/del_teachers_info",methods=["GET","POST"])
def del_teachers_info():
    if request.method == "GET":
        #DBのすべてのクエリを取得
        teachers = Teacher.query.all()
        return render_template("del_teachers_info.html",teachers=teachers)
    else:
        #選択されたクエリをDBから削除する
        id = request.form["del_sel"] 
        db.session.query(Teacher).filter_by(id=id).delete()
        db.session.commit()
        db.session.close()
        return redirect("/del_teachers_info")

#SendGrid　webhookからポストを受け取り、activity_historiesを更新
@app.route('/webhook', methods=['POST'])
def webhook():
    # data_list = request.get_json()
    data_list = [{'email': 'seino0702@gmail.com', 'event': 'open', 'ip': '66.249.84.53', 'sg_content_type': 'html', 'sg_event_id': '7SySn_H4QJa5e6gGSVfw1w', 'sg_machine_open': False, 'sg_message_id': 'kWUYivbIRzSjc8PMp3xTNg.filterdrecv-68f8d557c9-cxx9p-1-640894F4-127.9', 'timestamp': 1678336248, 'useragent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)'}]
    print(data_list)
    return '', 200, {}


#TODO メール既読画面
@app.route('/mail_history')
def mail_history():
    pass


data_list = [{'email': 'seino0702@gmail.com', 'event': 'open', 'ip': '66.249.84.53', 'sg_content_type': 'html', 'sg_event_id': '7SySn_H4QJa5e6gGSVfw1w', 'sg_machine_open': False, 'sg_message_id': 'kWUYivbIRzSjc8PMp3xTNg.filterdrecv-68f8d557c9-cxx9p-1-640894F4-127.9', 'timestamp': 1678336248, 'useragent': 'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)'}]
data_dict = data_list[0]

email_from_sg = data_dict['email']
event = data_dict['event']
timestamp =  data_dict['timestamp']  
sg_message_id = data_dict['sg_message_id']

#mail_historiesからwork_date,teachersからteachers.idを所得
mail_history = Mail_history()
teacher = Teacher()

with app.app_context():
    #TODO mail_historyがない時の処理を考える
    mail_history =  db.session.query(Mail_history).filter_by(x_id=sg_message_id).first() 

print(mail_history)

with app.app_context():
    teacher = db.session.query(Teacher).filter_by(email_address=email_from_sg).first() 

work_date = mail_history.work_date
activity_history = Activity_history()
#acitivity_historiesに登録されているか確認
activity_existance = True
with app.app_context():
    activity_existance = db.session.query(Activity_history.query.filter(Activity_history.x_id == sg_message_id,Activity_history.teachers_id == teacher.id).exists()).scalar()


if(activity_existance):
    with app.app_context():
        activity_history =  db.session.query(Activity_history).filter(Activity_history.x_id == sg_message_id, Activity_history.teachers_id == teacher.id)
        #eventタイプによって処理を分ける
        
    
else:
    same_day_existance = False
    #同日のactivity_historyがないか確認
    with app.app_context():
        same_day_existance = db.session.query(Mail_history.query.filter(Mail_history.work_date == work_date).exists()).scalar()
    # if(same_day_existance):
        # #eventの種類を調べる
        # exsit_x_id = ""
        # with app.app_context():
        #     exsit_x_id = db.session.query(Mail_history).filter(Mail_history.work_date == work_date)
        # with app.app_context():
        #     activity_history =  db.session.query(Activity_history).filter(Activity_history.x_id == exsit_x_id, Activity_history.teachers_id == teacher.id).first()
        #     print("ここやで")
        #     print(activity_history)
        # event = activity_history.event_type
    # else:

    #mail_historiesに登録する
    
    activity_history = Activity_history()
    activity_history.teachers_id = teacher.id
    activity_history.time_record =  datetime.fromtimestamp(timestamp)
    activity_history.event_type = event
    activity_history.x_id = sg_message_id
    print(sg_message_id)
    with app.app_context():
        db.session.add(activity_history)
        db.session.commit()
        db.session.close()





        

    



