from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL 연결 설정
app.config['MYSQL_HOST'] = 'your_mysql_host'
app.config['MYSQL_USER'] = 'your_mysql_user'
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
app.config['MYSQL_DB'] = 'your_mysql_db'
mysql = MySQL(app)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # 폼에서 전송된 데이터 가져오기
        userid = request.form['userid']
        password = request.form['password']
        nickname = request.form['nickname']
        email = request.form['email']

        # MySQL에 데이터 추가
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users (username, password, nickname, email) VALUES (%s, %s, %s, %s)",
                    (userid, password, nickname, email))
        mysql.connection.commit()
        cur.close()

        return '회원가입 성공'

    return render_template('register.html')

if __name__ == '__main__':
    app.run(debug=True)