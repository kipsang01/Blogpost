from flask import render_template,request,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from .. import db
from sqlalchemy import  func, desc
from ..models import User,Blog,Comment 
from ..request import get_quotes
from .forms import PostForm,CommentForm



@main.route('/')
@main.route('/home')
def home():
    Quote = get_quotes()
    blogs = Blog.query.order_by(desc('date_posted')).all()
    return render_template('home.html', blogs=blogs,  Quote=Quote)

@main.route('/addblog', methods=['GET', 'POST'])
@login_required
def add_blog():
    form = PostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_blog = Blog( title=form.title.data, category=form.category.data, content=form.editor.data, user_id = current_user.id)
            new_blog.save_blog()
            blogs = Blog.query.order_by(desc('date_posted')).all()
            flash('Blog posted!','success')
            return redirect(url_for('.home',blogs=blogs))
        
    return render_template('add-blog.html' , form=form)


@main.route('/profile')
@login_required
def profile():
    pass

@main.route('/blog/<blog_id>', methods=['GET', 'POST'])
def blog(blog_id):
    form = CommentForm()
    blog = Blog.query.filter_by(id =blog_id).first()
    comments = Comment.query.filter_by(blog_id = blog_id).all()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_comment = Comment( content=form.comment.data, blog_id = blog_id, user_id = current_user.id)
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment posted!','success')
            return redirect(url_for('.blog',blog_id = blog.id))
    return render_template('blog.html', blog=blog,comments=comments,form=form)


@main.route('/comment/<blog_id>', methods=['POST','GET'])
def delete_blog(blog_id):
    blog_del = Blog.query.filter_by(id = blog_id).first()
    db.session.delete(blog_del)
    db.session.commit()
    return redirect(url_for('.home'))



@main.route('/comment/<comment_id>', methods=['POST','GET'])
def delete_comment(comment_id):
    comment_del = Comment.query.filter_by(id = comment_id).first()
    blog_id = comment_del.blog_id
    db.session.delete(comment_del)
    db.session.commit()
    return redirect(url_for('.blog',blog_id = blog_id))




