from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///users.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = "123456789"
postdb = False
db = SQLAlchemy(app)

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(80), unique=True, nullable=False)
  password = db.Column(db.String(120), unique=False, nullable=False)

  def __repr__(self):
    return '<User %r>' % self.username

@app.route("/")
def index():
    db.create_all()
    print(session)
    return render_template("index.html")

@app.route("/log")
def log():
    return render_template("form.html")

@app.route('/login', methods=["POST", "GET"])
def login():
  if request.method == "POST":
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()
    print(user)
    if user and (password == user.password):
      session["username"] = username
      return redirect('/')
    else:
      return render_template("login.html",
                             message="password or/and username is wrong")
  else:
    return render_template("login.html")
  
@app.route('/register', methods=["GET", "POST"])
def register():
  if request.method == "GET":
    return render_template("register.html")
  else:
    username = request.form.get("username")
    password = request.form.get("password")
    password2 = request.form.get("confirm-password")

    if password != password2:
      return render_template("register.html",
                             message="passwords are not the same")

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    session["username"] = username
    return redirect('/')

@app.route('/logout', methods=["GET"])
def logout():
  if "username" in session:
    session.pop("username")
    return redirect('/')

if __name__ == '__main__':  
   app.run(debug = True)