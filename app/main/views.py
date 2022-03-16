from ..requests import get_quotes
from app.main.forms import UpdateProfile, PostForm, CommentForm, UploadForm
from flask import render_template,abort,redirect,flash,url_for,Blueprint,request
from . import main
from .. import db, create_app
import secrets
import os
from flask_login import login_user,logout_user,login_required,current_user
from ..models import Post, User, Comment
from ..auth.forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory  
  




@main.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(main.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')



@main.route('/')
def home():
    quotes=get_quotes()
    print(quotes)
    posts=Post.query.all()
    
    return render_template("home.html",posts=posts,quotes=quotes, uname = current_user)

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user = User(email = form.email.data, username = form.username.data,password = form.password.data)
        db.session.add(user)
        db.session.commit()
        
        
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('..login'))
        
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Register'
    return render_template("register.html",form=form,title=title)

@main.route('/login',methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    '''
    View root page function that returns the index page and its data
    '''
    if form.validate_on_submit():
         
        user = User.query.filter_by(email = form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.home'))

        flash('Invalid username or Password')

    return render_template('login.html', title='Login', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.home"))

@main.route('/user/<username>')
def profile(username):
    user = User.query.filter_by(username = username).first()
    if user is None:
        abort(404)

    return render_template("profile/profile.html", user = user)

@main.route('/user/<uname>/update/pic',methods= ['POST'])
@login_required
def save_picture(username):
    form = UploadForm
    random_hex=secrets.token_hex(8)
    _,f_ext = os.path.splitext(form.data)
    picture_fn =random_hex + f_ext
    picture_path=os.path.join(main.root_path,'static/photos',picture_fn)
    form.save(picture_path)
    return redirect(url_for('main.profile',uname=username,  picture_fn='profile_picture'))
    
    

@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname ).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('main.profile', username = uname))

    return render_template('update.html',form =form)

@main.route('/comment/new', methods = ['GET','POST'])
@login_required
def new_comment(post_id):
    post = Comment.query.filter_by(post_id=post_id).first()
    if post is None:
        abort(404)
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(comment=form.content.data, post_id=post_id)
        new_comment.save_comment()
        db.session.add(new_comment)
        db.session.commit()
       
        flash('You comment has been created!', 'success')
        return redirect(url_for('main.post',post_id=post_id))
    else:
        content=Comment.query.order_by(Comment.content).all()
    return render_template('new-comment.html', add='New Comment',post=post,comment=content,form=form)


@main.route('/post/new',methods=['GET','POST'])
@login_required
def new_post():
    form =PostForm()
    if form.validate_on_submit():
        post =Post(title=form.title.data,content=form.content.data,author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your blog has been created",'success')
        return redirect(url_for('main.home'))
    return render_template('create_post.html',form=form,legend='New Post')

@main.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

   
@main.route('/post/<int:post_id>/update',methods=['GET','POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author !=current_user:
        os.abort(403)
    form=PostForm()
    if form.validate_on_submit():
        post.title=form.title.data
        post.content=form.content.data
        db.session.commit()
        flash("Your post has been updated",'success')
        return redirect(url_for('.post',post_id=post_id))
    elif request.method=='GET':
        form.title.data=post.title
        form.content.data=post.content
    
    return render_template('create_post.html', title='Update Post',legend='Update Post', post=post,form=form)

@main.route('/post/<int:post_id>/delete',methods=['POST','GET'])
@login_required
def delete_post(post_id): 
    post = Post.query.get_or_404(post_id)
    if post.author !=current_user:
        os.abort(403)
    db.session.delete(post)
    db.session.commit()
    
    
    flash("Your post has been deleted",'success')
    return redirect(url_for('main.home'))
 
