import os
from flask import Flask
from apscheduler.schedulers.background import BackgroundScheduler
from flask import render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from email_programs import main
from app import db

from sqlalchemy.types import Float,Boolean
from sqlalchemy.types import Integer
from sqlalchemy.types import String
from sqlalchemy.types import DateTime,Date
from sqlalchemy.sql.functions import current_timestamp

from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import declarative_base, relationship


#DB

# app = Flask(__name__)
# #dbのURLを設定
# db_uri = os.environ.get('DATABASE_URL')or "postgres://postgres:postgres@localhost/work_app"
# db_uri = db_uri.replace("://", "ql://", 1) 
# print(db_uri)
# app.config['SQLALCHEMY_DATABASE_URI'] = db_uri 
# db = SQLAlchemy(app) 

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
     #0 proccessed 1 deliverd, 2 open
     event_type = db.Column(db.Integer,nullable=False)

