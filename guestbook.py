#coding:utf8
import shelve
from datetime import datetime
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
    greeting_list = load_data()
    return render_template('index.html',greeting_list=greeting_list)

@application.route('/post',methods={'POST'})
def post():
    """ 用于提交评论的URL
    """
    # 获取已提交的数据
    name = request.form.get('name') # 名字
    comment = request.form.get('comment') # 留言
    create_at = datetime.now() # 投稿时间（当前时间）
    # 保存数据
    save_data(name, comment, create_at)
    # 保存后重定向到首页
    return redirect('/')

@application.template_filter('n12br')
def n12br_filter(s):
    """将带有换行符号换成br标签
    """
    return escape(s).replace('\n',Markup('<br>'))

@application.template_filter('datetime_fmt')
def datetime_fmt_filter(dt):
    """使用datetime对象更容易的分辨模块过滤器
    """
    return dt.strftime('%Y/%m/%d %H:%M:%S')


if __name__ == '__main__':
    application.run('0.0.0.0',8000,debug=True)
