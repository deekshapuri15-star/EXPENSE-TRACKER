from time import strftime

from flask import Flask,render_template,request,redirect,url_for,session
from datetime import datetime
import sqlite3
app = Flask(__name__)
conn = sqlite3.connect('tracker.db')
cur = conn.cursor()
cur.execute("""
                CREATE TABLE IF NOT EXISTS expense(
                 EXPENSENAME VARCHAR(50) NOT NULL,
                 AMOUNT INT NOT NULL,
                 CATEGORY VARCHAR(50)  NOT NULL)
                 """  )
conn.commit()
conn.close()

app.secret_key  = 'abc123'
@app.route('/' , methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
      username = request.form.get('username')
      password = request.form.get('password')
      if username == "dp" and password == "123":
          session['username'] = username
          return redirect(url_for('login123'))
      else:
          return "invalid credentials"
    return render_template('home123.html')
@app.route('/login123', methods=['GET', 'POST'])
def login123():
    conn = sqlite3.connect('tracker.db')
    cur = conn.cursor()

    if request.method == 'POST':
       expense = request.form.get('expense')
       amount = request.form.get('amount')
       category = request.form.get('category')
       date = datetime.now().strftime("%Y-%m-%d")
       cur.execute(f"""
       INSERT INTO expense VALUES( '{expense}', '{amount}' , '{category}') """)
    conn.commit()
    cur.execute("SELECT * FROM expense")
    expenses = cur.fetchall()

    cur.execute(" ""SELECT  category,sum(amount) FROM expense GROUP BY CATEGORY" "")
    category_total  = cur.fetchall()
    cur.execute("SELECT SUM(amount) FROM expense")
    total = cur.fetchone()[0]
    total = total if total else 0


    conn.close()
    return render_template('login123.html',expenses=expenses,category_total=category_total,total = total)

if __name__ == '__main__':
    app.run(debug=True)