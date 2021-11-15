from flask import render_template,request,redirect,url_for,abort,flash
from flask_login import login_required,current_user
from . import main
from .. import db,photos
from sqlalchemy import  func, desc
from ..models import User,Blog,Comment 
from ..request import get_quotes
from .forms import PostForm,CommentForm,AddBioForm, subscriptionForm



@main.route('/')
@main.route('/home')
def home():
    form = subscriptionForm()
    Quote = get_quotes()
    blogs = Blog.query.order_by(desc('date_posted')).all()
    return render_template('home.html', blogs=blogs,  Quote=Quote,form = form)

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


#profile
@main.route('/profile<username>')
def profile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html',user=user)

#blog page
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

#delete blog
@main.route('/comment/<blog_id>', methods=['POST','GET'])
def delete_blog(blog_id):
    blog_del = Blog.query.filter_by(id = blog_id).first()
    db.session.delete(blog_del)
    db.session.commit()
    flash('Blog deleted!', 'danger')
    return redirect(url_for('.home'))


#delete comment
@main.route('/comment/<comment_id>', methods=['POST','GET'])
def delete_comment(comment_id):
    comment_del = Comment.query.filter_by(id = comment_id).first()
    blog_id = comment_del.blog_id
    db.session.delete(comment_del)
    db.session.commit()
    flash('Comment deleted!', 'danger')
    return redirect(url_for('.blog',blog_id = blog_id))

#edit blog
@main.route('/blog/<blog_id>/update',methods=['GET', 'POST'])
@login_required
def update_blog(blog_id):
    blog=Blog.query.filter_by(id=blog_id).first()
    form=PostForm()
    if blog.author.id !=current_user.id:
        abort(403)
   
    if form.validate_on_submit():
        blog.title=form.title.data
        blog.category=form.category.data
        blog.content=form.editor.data
        db.session.commit()
        flash('Blog updated!','success')
        return redirect(url_for('.blog',blog_id = blog.id))
    elif request.method=='GET':
        form.title.data=blog.title
        form.category.data=blog.category
        form.editor.data = blog.content
        
    return render_template('add-blog.html', form = form)

#adding bio
@main.route('/user/<uname>/update/bio',methods= ['GET','POST'])
@login_required
def add_bio(uname):
    form = AddBioForm()
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',username=user.username))
    return render_template('bio-profile.html',form=form)


#Adding profile pic
@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def update_pic(uname):
    user = User.query.filter_by(username = uname).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'images/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',username=uname))

#return blogs by category
@main.route('/blogs/<category>')
def blog_category(category):
    form = subscriptionForm()
    Quote = get_quotes()
    blogs = Blog.query.filter_by(category=category).all()
    return render_template('category.html',blogs=blogs,form=form,category=category, Quote =Quote)