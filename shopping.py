from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import os


#애플리케이션 객체 생성
app = Flask(__name__) 


#MySQL 연결설정
mysql = MySQL(app) 
app.config['MYSQL_HOST'] = '158.247.230.44'  # MySQL 서버 주소
app.config['MYSQL_USER'] = 'dev'  # MySQL 사용자 이름
app.config['MYSQL_PASSWORD'] = 'overload'  # MySQL 비밀번호
app.config['MYSQL_DB'] = 'userinfo'  # 사용할 데이터베이스 이름


#메인 페이지
@app.route('/')
def index():
    return render_template("index.html")


#회원가입 페이지
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        nickname = request.form['nickname']
        email = request.form['email']

        try:
            #mysql과 상호작용하는 커서 객체 생성
            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM user WHERE id = %s OR email = %s", (userid, email))
            existing_user = cur.fetchone()

            if existing_user:
                error_message = '이미 존재하는 아이디 또는 이메일입니다.'
                return render_template('register.html', error_message=error_message)
            
            #SQL 쿼리 실행
            cur.execute("INSERT INTO user (id, name, pw, email) VALUES (%s, %s, %s, %s)",
                    (userid, nickname, password, email))
            mysql.connection.commit()

            cur.close()
        
        except Exception as e:
            return f'에러 발생: {str(e)}'

    return render_template('register.html')


app.secret_key = os.urandom(24)


# 로그인 페이지
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']

        try:
            #사용자 정보를 가져옴 
            cur = mysql.connection.cursor()
            cur.execute("SELECT * FROM user WHERE id = %s", (userid, ))
            user = cur.fetchone()
            
            #사용자가 존재하고 비밀번호가 일치하면 로그인 성공
            if user and user[2] == password:
                session['userid'] = user[0]
                session['nickname'] = user[1]
                success_message = "로그인 성공!"
                return render_template('product_list.html', success_message=success_message)  

            # 로그인 실패
            error_message = '아이디 또는 비밀번호가 올바르지 않습니다.'
            return render_template('login.html', error_message=error_message)

        except Exception as e:
            return f'에러 발생: {str(e)}'

    return render_template('login.html')


#로그아웃 페이지
@app.route('/logout')
def logout():
    session.pop('userid', None)
    session.pop('nickname', None)
    return render_template('index.html')


#제품 리스트 페이지
@app.route('/product_list')
def product_list():
    return render_template("product_list.html")


#문의 제출 페이지
@app.route('/submit_inquiry', methods=['GET', 'POST'])
def submit_inquiry():
    if request.method == 'POST':
        username = request.form.get('inquiry_head')
        inquiry_text = request.form.get('inquiry_body')

        try:
            # 사용자 이름과 내용을 추가시킴 
            cur = mysql.connection.cursor()

            cur.execute("SELECT * FROM inquiry")
            inquiries = cur.fetchall()
            

            cur.execute("INSERT INTO inquiry (id, inquiry_head, inquiry_body) VALUES (%s, %s, %s)", (len(inquiries), username, inquiry_text))
            mysql.connection.commit()

            cur.close()

            success_message = "문의가 제출되었습니다!"
            return render_template('submit_inquiry.html', success_message=success_message)

        except Exception as e:
            return f'에러 발생: {str(e)}'

    return render_template('submit_inquiry.html')


#문의 확인 페이지
@app.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    try:
        # inquriy 테이블의 내용을 가져옴
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM inquiry")
        inquiries = cur.fetchall()

        cur.close()

        return render_template('inquiry.html', inquiries=inquiries)

    except Exception as e:
        return f'에러 발생: {str(e)}'

#문의 확인 페이지
@app.route('/view_inquiry', methods=['GET', 'POST'])
def view_inquiry():
    inquiry_id = request.form.get('inquiry_id')

    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM inquiry WHERE id=%s", (inquiry_id,))
    inquiry = cur.fetchone()

    cur.close()

    return render_template('view_inquiry.html', inquiry=inquiry)
    
    
if __name__ == '__main__':
    app.run(debug="true")