from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Friends, Post, Reaction, Comment
from sqlalchemy import func

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@views.route('/home', methods=['GET', 'POST'])
@login_required
def home():
    like_count = db.session.query(Post.id, func.count(Reaction.reaction)).filter(
        Reaction.reaction == '1').join(Reaction).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    comment_count = db.session.query(Post.id, func.count(Comment.postid)).join(
        Comment).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    like_exists = db.session.query(Post, Reaction.user_id).filter(
        Reaction.reaction == '1', Reaction.user_id == current_user.id).join(Reaction).all()
    my_friends_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image).filter(
        Friends.status == '1', (Friends.sentto == current_user.id) | (Friends.user_sender == current_user.id), (Friends.sentto == User.id) | (Friends.user_sender == User.id), User.id != current_user.id)[:5]
    friend_request_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image, Friends.request_sent_date).filter(
        Friends.status == '0', Friends.sentto == current_user.id, User.id == Friends.user_sender)[:5]
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    my_all_frnd_post = db.session.query(User, Post).filter(
        Friends.status == '1', (Friends.sentto == current_user.id) | (Friends.user_sender == current_user.id), (Friends.sentto == User.id) | (Friends.user_sender == User.id), User.id != current_user.id, User.id == Post.user_id).order_by(Post.date_posted.desc()).all()
    return render_template('facebook_homepage.html', myname=current_user, total_count_friend_request=total_count_friend_request, friend_request_detail=friend_request_detail, my_friends_detail=my_friends_detail, my_all_frnd_post=my_all_frnd_post, like_exists=like_exists, like_count=like_count, comment_count=comment_count)


@views.route("/myprofile")
@login_required
def myprofile():
    like_count = db.session.query(Post.id, func.count(Reaction.reaction)).filter(
        Reaction.reaction == '1').join(Reaction).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    comment_count = db.session.query(Post.id, func.count(Comment.postid)).join(
        Comment).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    like_exists = db.session.query(Post, Reaction.user_id).filter(
        Reaction.reaction == '1', Reaction.user_id == current_user.id).join(Reaction).all()
    my_post = db.session.query(User, Post).filter(
        Post.user_id == current_user.id, User.id == current_user.id).order_by(Post.date_posted.desc()).all()
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    return render_template('facebook_myprofile.html', myname=current_user, total_count_friend_request=total_count_friend_request, my_post=my_post, like_exists=like_exists, like_count=like_count, comment_count=comment_count)


@views.route("/myabout")
@login_required
def myabout():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    return render_template('facebook_myprofile_about.html', myname=current_user, total_count_friend_request=total_count_friend_request)


@views.route("/username/<int:user_id>")
@login_required
def username(user_id):
    like_count = db.session.query(Post.id, func.count(Reaction.reaction)).filter(
        Reaction.reaction == '1').join(Reaction).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    comment_count = db.session.query(Post.id, func.count(Comment.postid)).join(
        Comment).group_by(Post.id).order_by(func.count(Post.id).desc()).all()
    like_exists = db.session.query(Post, Reaction.user_id).filter(
        Reaction.reaction == '1', Reaction.user_id == current_user.id).join(Reaction).all()
    user_post = db.session.query(User, Post).filter(
        Post.user_id == user_id, User.id == user_id).order_by(Post.date_posted.desc()).all()
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    if user_id == current_user.id:
        return redirect(url_for('views.myprofile'))
    user = User.query.filter(User.id == user_id).first()
    if user:
        detail = Friends.query.filter(Friends.status == '1', (Friends.sentto == current_user.id) | (
            Friends.user_sender == current_user.id), (Friends.sentto == user_id) | (Friends.user_sender == user_id)).scalar()
        return render_template('facebook_user_profile.html', user=user, total_count_friend_request=total_count_friend_request, myname=current_user, user_post=user_post, like_exists=like_exists, like_count=like_count, comment_count=comment_count, detail=detail)
    flash('userid not found', 'error')
    return render_template('facebook_homepage.html', total_count_friend_request=total_count_friend_request, myname=current_user)


@views.route("/user_about/<int:user_id>")
@login_required
def user_about(user_id):
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    if user_id == current_user.id:
        return redirect(url_for('views.myprofile'))
    user = User.query.filter(User.id == user_id).first()
    return render_template('facebook_user_about.html', user=user, total_count_friend_request=total_count_friend_request, myname=current_user)


@views.route("/search_user", methods=['GET', 'POST'])
def search_user():
    if request.method == 'POST':
        form = request.form
        search_value = form['search_user_detail']
        search = "%{}%".format(search_value)
        results = User.query.filter(User.firstname.like(search) | User.lastname.like(
            search)).order_by(User.register_date.desc()).all()
        if form['search_user_detail'] == "":
            flash('please enter data for search', 'error')
            return redirect(url_for('views.home'))
        else:
            return render_template("facebook_search_bar.html", results=results, myname=current_user, search_word=form['search_user_detail'])
    flash('Matching data not found', 'error')
    return redirect(url_for('views.home'))
