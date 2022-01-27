from datetime import datetime
from re import M
from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from flask import session

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mydatabase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['SQLALCHEMY_BINDS']={
#     'userdata':'sqlite:///userdb.db',
# }

db = SQLAlchemy(app)

db.create_all()
class ToDoList(db.Model):
    # __tablename__ = 'todolist'
    index = db.Column(db.Integer, primary_key = True,autoincrement=True)
    title = db.Column(db.String(100), nullable = False)
    description = db.Column(db.String(400), nullable = False)
    datetime_var = db.Column(db.DateTime, default = datetime.utcnow)
class UserData(db.Model):
    # __bind_key__ = 'userdata'
    __tablename__ = 'userdata'
    index = db.Column(db.Integer,primary_key = True,autoincrement=True)
    firstname = db.Column(db.String(10), nullable = False)
    lastname = db.Column(db.String(10), nullable = False)
    email = db.Column(db.String(50), nullable = False)
    mobile = db.Column(db.Integer, nullable = False)
    password = db.Column(db.String(20), nullable = False)
    date_time = db.Column(db.DateTime, default = datetime.utcnow)

session = {}
session['check_login'] = False

@app.route('/', methods = ['GET', 'POST'])
def home_page():
    if not session.get('check_login') == True:
        print(session['check_login'], " - session status")  ## for developers understanding session check
        return redirect('/login')
    else:
        all_to_do = ToDoList.query.all()
        
        return render_template('./index.html',allTodo = all_to_do)

@app.route('/update/<int:index>', methods = ['GET', 'POST'])
def update_data(index):
    if request.method == "POST":
        title_data = request.form['title']
        description_data = request.form['description']
        todo = ToDoList.query.filter_by(index = index).first()
        todo.title = title_data
        todo.description = description_data
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    all_todo = ToDoList.query.filter_by(index = index).first()
    
    return render_template('./update.html',allTodo = all_todo)

@app.route('/delete/<int:index>', methods = ['GET', 'POST'])
def delete_data(index):
    all_todo = ToDoList.query.filter_by(index = index).first()
    db.session.delete(all_todo)
    db.session.commit()
    return redirect('/')


@app.route('/add', methods = ['GET', 'POST'])
def add_data():
    if request.method == "POST":
        title_data = request.form['title']
        description_data = request.form['description']
        if len(description_data)>0 and len(title_data)>0:
            todo = ToDoList(title = title_data, description = description_data)
            db.session.add(todo)
            db.session.commit()
    return redirect('/')

@app.route('/login/', methods = ['GET', 'POST'])
def login_data():
    print("in /login page")
    if request.method == "POST":
        data_email = request.form['email']
        data_password = request.form['password']
        data_login = UserData.query.filter_by(email = data_email,password = data_password).first()
        if data_email == data_login.email and data_password == data_login.password:
            session['check_login'] = True  
            print(session['check_login']," - session status")
            return redirect('/')
        else:
            session['check_login'] = False         ## for developers understanding session check
            return render_template('./login.html')    
    return render_template('./login.html')   

@app.route('/logout', methods = ['GET', 'POST'])
def logout_data():
    if request.method == "POST":
                                                         
        session['check_login'] = False            ## for developers understanding session check
        print(session['check_login']," - session status")
        return redirect('/login')

@app.route('/signup', methods = ['GET', 'POST'])
def signup_data():
    print("in /signup page")
    if request.method == "POST":
        firstname_data = request.form['fname']
        lastname_data = request.form['lname']
        email_data = request.form['email']
        mobile_data = request.form['mobile']
        password_data = request.form['password']
    
        if len(firstname_data)>0 and len(lastname_data)>0 and len(email_data)>0 and len(mobile_data)>0 and len(password_data)>0:
            data = UserData(firstname=firstname_data,lastname=lastname_data,email=email_data,mobile=mobile_data,password=password_data)
            db.session.add(data)
            db.session.commit()
            return render_template('./login.html')
        else:
            pass
    return render_template('/signup.html')    
        

@app.errorhandler(404)
def page_not_found(e):                                  # error handling for invalid url
    return render_template('./error.html'),404

if __name__== '__main__':
    app.run(debug=False)