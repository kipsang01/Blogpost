from . import db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin
from . import login_manager
from datetime import datetime


class Quote():
    def __init__(self, author,quote, link):
        self.author = author
        self.quote = quote
        self.link = link
        
        
#user loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(UserMixin,db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(255),index = True)
    password_hash = db.Column(db.String(255))
    email = db.Column(db.String(255),unique = True,index = True)
    bio = db.Column(db.String(255))
    profile_pic_path = db.Column(db.String())
    blogs = db.relationship('Blog', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    

    @property
    def password(self):
        raise AttributeError('You cannnot read the password attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)


    def save_user(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f'User {self.username}'
    
    

class Blog(db.Model):
    __tablename__ = 'blogs'
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(255), nullable = False)
    category = db.Column(db.String(255), nullable = False)
    content = db.Column(db.Text,nullable = False)
    date_posted  = db.Column(db.DateTime,default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
    comments = db.relationship('Comment', backref='blog', lazy='joined' , cascade="all, delete")
    
    
    
    def save_blog(self):
        db.session.add(self)
        db.session.commit()
        

    def __repr__(self):
        return f'Blog {self.title}{self.user_id}'
    
    
class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer,primary_key = True)
    content = db.Column( db.String(255))
    date_posted  = db.Column(db.DateTime,nullable = False,default=datetime.utcnow())
    blog_id = db.Column(db.Integer, db.ForeignKey('blogs.id'),nullable = False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'),nullable = False)
    
    
    def __repr__(self):
        return f'Comment {self.category}{self.content}'
    