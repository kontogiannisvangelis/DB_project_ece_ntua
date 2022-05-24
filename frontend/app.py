from flask import Flask, render_template, request, redirect
from flask_mysqldb import MySQL

import yaml

app = Flask(__name__)


db = yaml.safe_load(open('db.yaml'))
#configure db
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']

mysql = MySQL(app)




@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/page_1.html', methods=['GET', 'POST'])
def page_1():
    if request.method == 'POST':
        input_data = request.form
        start_date = input_data['start_date']
        if start_date == '': 
            start_date = None
        end_date = input_data['end_date']
        if end_date == '': 
            end_date = None
        duration = input_data['duration']
        if duration == '':
            duration = None
        ex_f_name = input_data['ex_f_name']
        if ex_f_name == '':
            ex_f_name = None
        ex_l_name = input_data['ex_l_name']
        if ex_l_name == '':
            ex_l_name = None
        cur = mysql.connection.cursor()
        cur.execute("insert into test(start_date, end_date, duration, ex_f_name, ex_l_name) values(%s, %s, %s, %s, %s)", (start_date, end_date, duration, ex_f_name, ex_l_name)) 
        mysql.connection.commit()
        cur.close()
    return render_template('page_1.html')

@app.route('/page_2_1.html')
def page_2_1():
    return render_template('page_2_1.html')

@app.route('/page_2_2.html')
def page_2_2():
    return render_template('page_2_2.html')

@app.route('/page_2.html')
def page_2():
    return render_template('page_2.html')

@app.route('/page_3.html')
def page_3():
    return render_template('page_3.html')

@app.route('/page_4.html')
def page_4():
    return render_template('page_4.html')

@app.route('/page_5.html')
def page_5():
    return render_template('page_5.html')

@app.route('/page_6.html')
def page_6():
    return render_template('page_6.html')

@app.route('/page_7.html')
def page_7():
    return render_template('page_7.html')

@app.route('/page_8.html')
def page_8():
    return render_template('page_8.html')

@app.route('/page_9.html')
def page_9():
    return render_template('page_9.html')



if __name__ == '__main__':
    app.run(debug=True)