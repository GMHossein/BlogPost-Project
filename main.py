from flask import Flask , render_template , request , redirect , url_for , flash , abort , jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash , check_password_hash
from flask_login import LoginManager , UserMixin , current_user , login_user , logout_user , login_required
from datetime import datetime
from smtplib import SMTP
from email.message import EmailMessage
import hashlib
from random import choice

app = Flask(__name__)
app.config['SECRET_KEY'] = "SECRET_KEY"

login_manager = LoginManager()
login_manager.init_app(app)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model,UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(250), unique=True, nullable=False)
    password = db.Column(db.String(250), nullable=False)
    name = db.Column(db.String(250), nullable=False)
    premium = db.Column(db.String(250), nullable=False)

    comments = db.relationship("Comment",backref="author",lazy=True)

    blogpost = db.relationship("BlogPost",backref="author",lazy=True)


class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    discription = db.Column(db.String(250),nullable=False)
    image_url = db.Column(db.String(250),nullable=False)
    body = db.Column(db.Text, nullable=False)
    date = db.Column(db.String(250), nullable=False)

    comments = db.relationship("Comment",backref="post",lazy=True , cascade="all,delete-orphan")

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)


class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer,primary_key=True)
    date = db.Column(db.String(250),nullable=False)
    body = db.Column(db.Text,nullable=True)

    user_id = db.Column(db.Integer,db.ForeignKey("users.id"),nullable=False)
    post_id = db.Column(db.Integer,db.ForeignKey("posts.id"),nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

def gravatar_url(email, size=100, default="identicon", rating="g"):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d={default}&r={rating}"


@app.route("/",methods=["GET","POST"])
def home():
    now = datetime.now()
    year = now.year
    posts = BlogPost.query.all()
    posts = posts[0:5]
    recent_posts = posts[-3:]
    recent_posts_subtitle = posts[-5:]
    return render_template('index.html',current_user = current_user,posts = posts,recent_posts = recent_posts,recent_post=recent_posts_subtitle,year=year)


@app.route("/blog",methods=["GET","POST"])
def blog():
    now = datetime.now()
    year = now.year
    posts = BlogPost.query.all()
    recent_posts_subtitle = posts[-5:]
    return render_template("blog.html",posts = posts,recent_post=recent_posts_subtitle,current_user=current_user,year=year)

@app.route("/about")
def about():
    now = datetime.now()
    year = now.year
    return render_template("about.html",year=year)

@app.route("/contact",methods=["GET","POST"])
def contact():
    now = datetime.now()
    year = now.year
    if request.method == "POST":
        message = f"Name : {request.form['name']}\nEmail : {request.form['email']}\nMessage : {request.form['message']}"
        msg = EmailMessage()
        from_addr = "h73233816@gmail.com"
        password = "edaityeuvdwrkhnm"
        to_addrs = "h73233816@gmail.com"
        msg.set_content(message)
        msg['Subject'] = request.form["subject"]
        msg['From'] = from_addr
        msg['To'] = to_addrs

        with SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=from_addr, password=password)
            connection.send_message(msg)

    return render_template("contact.html",year=year)


@app.route("/post/<int:id>",methods=["GET","POST"])
def post(id):
    now = datetime.now()
    year = now.year
    posts = BlogPost.query.all()
    post = BlogPost.query.filter_by(id=id).first()
    recent_posts_subtitle = posts[-5:]
    today = datetime.today()
    if request.method == "POST":
        if current_user.is_authenticated:
            new_comment = Comment(
                body = request.form["message"],
                date = today.strftime("%b %d, %Y"),
                user_id = current_user.id,
                post_id = post.id
                ) 
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("post",id=id))
        else:
            flash("You should login first")
            return redirect(url_for("login"))
    comments = Comment.query.filter_by(post_id=post.id).all()

    return render_template("post-details.html",post=post,recent_post=recent_posts_subtitle,comments=comments,current_user=current_user,year=year,gravatar_url=gravatar_url)

@app.route("/login",methods=["GET","POST"])
def login():
    now = datetime.now()
    year = now.year
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]
        user = User.query.filter_by(email=email).first()
        if not user:
            flash("This email does not exist.")
            return redirect(url_for("register"))
        if user and check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            flash("Your password is incorrect.")
            return redirect(url_for("login"))

    return render_template("login.html",year=year)


@app.route("/register" , methods=["GET","POST"])
def register():
    now = datetime.now()
    year = now.year
    if request.method == "POST":
        email = request.form["email"]
        name = request.form["name"]
        is_user_in = User.query.filter_by(email=email).first()
        if is_user_in :
            flash("You are already registered.")
            return redirect(url_for("login")) 
        else:
            password = generate_password_hash(request.form["password"],method="pbkdf2:sha256",salt_length=8)
            premium = "False"
            new_user = User(email=email,name=name,password=password,premium=premium)
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user)
            return redirect(url_for("home"))
    return render_template("register.html",year=year)


@app.route("/logout")
def logout():
    if not current_user.is_authenticated:
        abort(403)
    logout_user()
    return redirect(url_for("home"))

@login_required
@app.route("/make-post",methods=["GET","POST"])
def make_post():
    if current_user.is_authenticated:
        if current_user.id != 1:
            abort(403)
    else:
        abort(403)
    now = datetime.now()
    year = now.year
    today = datetime.today()
    if request.method == "POST":
        title = request.form["title"]
        subtitle = request.form["subtitle"]
        discription = request.form["discription"]
        image_url = request.form["image-url"]
        body = request.form["editor"]
        date = today.strftime("%b %d, %Y")

        new_post = BlogPost(
            title=title,
            subtitle=subtitle,
            discription=discription,
            image_url=image_url,
            body=body,
            date=date,
            user_id=current_user.id)

        db.session.add(new_post)
        db.session.commit()
        
        return redirect(url_for("blog"))
    return render_template("edit-post.html",year=year)


@login_required
@app.route("/edit-post/<int:id>",methods=["POST","GET"])
def edit_post(id):
    if current_user.is_authenticated:
        if current_user.id != 1:
            abort(403)
    else:
        abort(403)
    now = datetime.now()
    year = now.year
    post = BlogPost.query.get(id)
    if request.method == "POST":
        post.title = request.form["title"]
        post.subtitle = request.form["subtitle"]
        post.discription = request.form["discription"]
        post.image_url = request.form["image-url"]
        post.body = request.form["editor"]
        db.session.commit()
        return redirect(url_for("blog"))
    return render_template("edit-post.html",is_edit=True,post=post,year=year)


@login_required
@app.route("/delet_post/<int:id>")
def delet_post(id):
    if current_user.is_authenticated:
        if current_user.id != 1:
            abort(403)
    else:
        abort(403)
    delet_post = BlogPost.query.filter_by(id=id).first()
    db.session.delete(delet_post)
    db.session.commit()
    return redirect(url_for("home"))

def to_dict(self):
    return {column.name: getattr(self, column.name) for column in self.__table__.columns}

@app.route("/api")
def api():
    return render_template("api.html") 

@app.route("/api/all")
def api_all():
    all_posts = BlogPost.query.all()
    return jsonify(posts = [to_dict(post) for post in all_posts])

@app.route("/api/search",methods = ["GET","POST"])
def search():
    query_title = request.args.get("title")
    all_posts = BlogPost.query.all()
    post = BlogPost.query.filter_by(title = query_title).first()
    if post:
        return jsonify(post = to_dict(post))
    else :
        return jsonify(error = {"Not Found":"There's no post with this title."})

@app.route("/api/remove",methods=["GET","POST"])
def remove():
    query_id = int(request.args.get("id"))
    query_key = request.args.get("key")
    if query_key == "TOP_API_KEY_FOR_BLOG":
        delet_post = BlogPost.query.filter_by(id=query_id).first()
        if delet_post:
            db.session.delete(delet_post)
            db.session.commit()
            return jsonify(message={"success":"you delet the post."})
        return jsonify(message={"error":"there is something wrong."})
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)