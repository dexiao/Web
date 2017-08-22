#coding:utf8
import shelve

from flask import Flask,request,render_template,redirect,escape,Markup

application = Flask(__name__)
DATA_FILE = 'guestbook.dat'
def save_data(name, comment, create_at):
    database = shelve.open(DATA_FILE)
    if 'greeting_list' not in database:
        greeting_list = []
    else:
        greeting_list = database['greeting_list']
    greeting_list.insert(0, {
'name': name,
'comment': comment,
'create_at': create_at,
})
    database['greeting_list'] = greeting_list
    database.close()

def load_data():
    """返回已经提交的数据
    """
    database = shelve.open(DATA_FILE)
    # 返回greeting_list。如果没有数据则返回空表
    greeting_list = database.get('greeting_list', [])
    database.close()
    return greeting_list

@application.route('/')
def index():
    """首页
    使用模板显示页面
    """
    return render_template('index.html')

if __name__ == '__main__':
    application.run('0.0.0.0',8000,debug=True)
