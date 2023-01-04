from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'free_board'

sql = "SELECT * from board"
mysql = MySQL(app)



@app.route("/") 		
def main():
    cur = mysql.connection.cursor()
    cur.execute(sql)
    data_list = cur.fetchall()
    cur.close() 			
    return render_template("index.html", data_list=data_list)

@app.route('/write', methods = ["POST",'GET'])
def write():
    
    if request.method == 'POST' :
        title = request.form['title']
        text = request.form['text']
        writer = request.form['writer']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO board (title, text, writer) VALUES (%s, %s, %s)", (title, text, writer))
        mysql.connection.commit()
        return redirect(url_for('main'))
    return render_template('write.html')

    

@app.route('/delete/<string:id>', methods = ['GET'])
def delete(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM board WHERE id=%s",(id,))
    mysql.connection.commit()
    return redirect(url_for('main'))

@app.route('/update/<string:id>',methods=['POST','GET'])
def update(id):

    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']
        writer = request.form['writer']
        cur = mysql.connection.cursor()
        cur.execute("""
               UPDATE board
               SET title=%s, text=%s, writer=%s
               where id=%s
            """, (title, text, writer, id))
        mysql.connection.commit()
        return redirect(url_for('main'))
    return render_template('update.html', id=id)



if __name__ == "__main__":
    app.run()