from flask import render_template,redirect,url_for,abort,request,flash
from app.main import main
from app.models import User,Blog,Comment,Subscriber
from .. import db
from app.requests import get_quotes
from flask_login import login_required,current_user
from ..email import mail_message
from .forms import UpdateProfile,CommentForm, CreateBlog
import secrets
from ..auth.forms import RegistrationForm, LoginForm
import os
from PIL import Image


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + f_ext
    picture_path = os.path.join('app/static/photos', picture_filename)
    
    output_size = (200, 200)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_filename

@main.route('/')
def index():
    user = User.query.filter_by().first()
    page = request.args.get('page',1, type = int )
    blogs = Blog.query.order_by(Blog.posted.desc()).all()
    quotes = get_quotes()
    print(quotes)
    return render_template('index.html', user=user,blogs=blogs, quotes = quotes)

@main.route("/about")
def learn():
    about_us = 'MyBlogPost is an app that allows you to register, post your personal blogs, read blogs form other people and like or comment on them'
    return render_template('about.html', about_us = about_us)

@main.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!','success')
        return redirect(url_for('index'))
        
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Register'
    return render_template('register.html' ,title=title,form = form)


@main.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    '''
    View root page function that returns the index page and its data
    '''
    title = 'Home - Login'
    return render_template('login.html' ,title=title,form = form )



@main.route('/user/<uname>/update',methods = ['GET','POST'])
@login_required
def update_profile(uname):
    user = User.query.filter_by(username = uname).first()
    if user is None:
        abort(404)

    form = UpdateProfile()

    if form.validate_on_submit():
        user.bio = form.bio.data

        db.session.add(user)
        db.session.commit()

        return redirect(url_for('.profile',uname=user.username))

    return render_template('profile/update.html',form =form)


@main.route("/post/<int:post_id>/comment", methods=['GET', 'POST'])
@login_required
def new_comment(post_id):
    post = Blog.query.get_or_404(post_id)
    
    form = CommentForm()
    if form.validate_on_submit():
        new_comment = Comment(comment=form.comment.data, author=current_user, post_id = post_id )
        new_comment.save_comment()
        db.session.add(new_comment)
        db.session.commit()
       
        flash('You comment has been created!', 'success')
        return redirect(url_for('main.posts', post_id=post.id))
    else:
        comments=Comment.query.order_by(Comment.comment).all()
    return render_template('new-comment.html', add='New Comment',post=post,comments=comments,form=form)

@main.route('/blog/<blog_id>/delete', methods = ['POST'])
@login_required
def delete_post(blog_id):
    blog = Blog.query.get(blog_id)
    if blog.user != current_user:
        abort(403)
    blog.delete()
    flash("You have deleted your Blog succesfully!")
    return redirect(url_for('main.index'))

@main.route('/subscribe',methods = ['POST','GET'])
def subscribe():
    email = request.form.get('subscriber')
    new_subscriber = Subscriber(email = email)
    new_subscriber.save_subscriber()
    mail_message("Subscribed to D-Blog","email/welcome_subscriber",new_subscriber.email,new_subscriber=new_subscriber)
    flash('Sucessfuly subscribed')
    return redirect(url_for('main.index'))

@main.route('/new_post', methods=['POST','GET'])
@login_required
def new_blog():
    subscribers = Subscriber.query.all()
    form = CreateBlog()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id =  current_user._get_current_object().id
        blog = Blog(title=title,content=content,user_id=user_id)
        blog.save()
        for subscriber in subscribers:
            mail_message("New Blog Post","email/new_blog",subscriber.email,blog=blog)
        return redirect(url_for('main.index'))
        flash('You Posted a new Blog')
    return render_template('newblog.html', form = form)
@main.route('/blog/<id>')
def blog(id):
    comments = Comment.query.filter_by(blog_id=id).all()
    blog = Blog.query.get(id)
    return render_template('blog.html',blog=blog,comments=comments)


@main.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Blog.query.filter_by(author=user).order_by(Blog.posted_date.desc()).paginate(page=page, per_page=10)
    return render_template('userpost.html', posts=posts, user=user)

@main.route('/like/<int:post_id>/<action>')
@login_required
def like_action(post_id, action):
    post = Blog.query.filter_by(id=post_id).first_or_404()
    if action == 'like':
        current_user.like_post(post)
        db.session.commit()
    if action == 'unlike':
        current_user.unlike_post(post)
        db.session.commit()
    return redirect(request.referrer)
    

@main.route('/profile',methods = ['POST','GET'])
@login_required
def profile():
    form = UpdateProfile()
    if form.validate_on_submit():
        if form.profile_picture.data:
            picture_file = save_picture(form.profile_picture.data)
            current_user.profile_pic_path = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        db.session.commit()
        flash('Succesfully updated your profile')
        return redirect(url_for('main.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
    profile_pic_path = url_for('static',filename = 'photos/'+ current_user.profile_pic_path) 
    return render_template('profile/profile.html', profile_pic_path=profile_pic_path, form = form)

