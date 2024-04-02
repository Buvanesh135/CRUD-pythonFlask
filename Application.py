from flask import Flask,render_template,redirect,request,url_for,jsonify
from flask_mysqldb import MySQL  # pip install flask-mysqldb
app=Flask(__name__)
app.config['MYSQL_HOST']='localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']='#N3wP4ssw0rd1'
app.config['MYSQL_DB']='flask'
mysql=MySQL(app)
                
@app.route('/index')
def fetch():
    cur= mysql.connection.cursor() #mysql.connection.cursor(): This method is called on the connection object to create a cursor object. A cursor is an object used to interact with the database. It allows you to execute SQL queries, fetch results, and perform other database operations.
    cur.execute("select * from student")
    data=cur.fetchall()  # nexted tuple 
    print(type(data))
    print(data,"datas")
    cur.close()
    return render_template('index.html',students=data)


@app.route('/insert',methods=['POST'])
def insert():
    if request.method== "POST":
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur=mysql.connection.cursor()
        cur.execute("INSERT INTO student ( name, email, phone) VALUES ( %s, %s, %s)", (name, email, phone))
        mysql.connection.commit() #.commit(): This is a method called on the connection object to commit the current transaction to the database. When you execute SQL statements that modify the database (such as INSERT, UPDATE, DELETE), those changes are not immediately applied to the database. Instead, they are kept in a transaction until you explicitly commit them. This ensures that changes are only applied to the database if all the operations in the transaction succeed.
        return redirect(url_for('fetch'))
    


@app.route('/update',methods=["POST","GET"])
def update():
    if request.method =="POST":
        user_id=request.form['id']
        name=request.form['name']
        email=request.form['email']
        phone=request.form['phone']
        cur=mysql.connection.cursor()
        cur.execute(""" UPDATE student SET name=%s, email=%s, phone=%s WHERE id= %s""",(name,email,phone,user_id))
        mysql.connection.commit()
        return redirect(url_for('fetch'))



@app.route("/delete/<string:id_data>",methods=["POST","GET"])
def delete(id_data):
        cur=mysql.connection.cursor()
        cur.execute(""" DELETE from student where id=%s""",(id_data))
        mysql.connection.commit()
        return redirect(url_for('fetch'))



if __name__=='__main__':
    app.run(debug=True,port=4000)