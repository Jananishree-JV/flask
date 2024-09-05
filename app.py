from flask import Flask,render_template,request,redirect,session
import sqlite3

app=Flask(__name__)
app.secret_key="7599"

con=sqlite3.connect("user.db" ,check_same_thread=False)
cur=con.cursor()
con.execute("create table if not exists user(emp_id integer primary key autoincrement,name varchar(50),age int,email varchar(50),role varchar(50))")
     
@app.route("/homepage")
def home():
    return render_template("home.html")

@app.route("/create",methods=["POST","GET"])
def create():
        if request.method=="POST": 
            emp_id=request.form["emp_id"]
            name=request.form["name"]
            age=request.form["age"]
            email=request.form["email"]
            role=request.form["role"]
            cur.execute("insert into user(name,age,email,role)values(?,?,?,?)",(name,age,email,role))
            con.commit()
            return "USER DATA CREATED!!"
        return render_template("create.html")
@app.route("/view")
def view():
    cur.execute("select * from user")
    data=cur.fetchall()
    return render_template("view.html",data=data)
@app.route("/update/<id>", methods=["POST","GET"])
def update(id):
    if request.method=="POST":
        name=request.form["name"]
        age=request.form["age"]
        email=request.form["email"]
        role=request.form["role"]
        cur.execute("update user set name=?,age=?,email=?,role=? where emp_id=?",(name,age,email,role,id))
        con.commit()
        return redirect("/view")

    cur.execute("select * from user where emp_id=?",(id,))
    data=cur.fetchone()
    print(data)
    return render_template("update.html",data=data)
@app.route("/delete/<id>")
def delete(id):
    cur.execute("delete from user where emp_id=?",(id,))
    con.commit()
    return redirect("/view")
app.run(debug=True)