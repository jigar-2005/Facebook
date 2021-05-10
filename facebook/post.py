from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from . import db
from .models import User, Friends, Post, Reaction, Comment
from . import db, ALLOWED_EXTENSIONS_POST, UPLOAD_FOLDER_POST
from werkzeug.utils import secure_filename
import os


post = Blueprint('post', __name__)


@post.route("/post/<int:post_id>/comment", methods=["GET", "POST"])
@login_required
def comment_post(post_id):
    if request.method == 'POST':
        comment = Comment(comment=request.form.get(
            'comment_data'), postid=post_id, userid=current_user.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been post', 'success')
        return redirect(url_for('post.post_with_comment', post_id=post_id))
    flash('comment did not passed', 'danger')
    return redirect(url_for('views.home'))


@post.route("/like<int:post_id>", methods=["GET", "POST"])
@login_required
def like(post_id):
    addlike = Reaction(postid=post_id, user_id=current_user.id, reaction="1")
    remove_like = Reaction.query.filter(
        Reaction.reaction == '1', Reaction.postid == post_id, Reaction.user_id == current_user.id).scalar()
    if remove_like:
        db.session.delete(remove_like)
        db.session.commit()
        flash('You remove like', 'success')
        return redirect(url_for('views.home'))
    else:
        db.session.add(addlike)
        db.session.commit()
        flash('You liked the post', 'success')
    return redirect(url_for('views.home'))


@post.route("/post_with_comment/<int:post_id>")
@login_required
def post_with_comment(post_id):
    user_comment_detail = db.session.query(User.id, User.firstname, User.lastname, Comment.comment).filter(
        Comment.postid == post_id, Comment.userid == User.id).all()
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    post_detail = db.session.query(
        User, Post).filter(Post.id == post_id).first()
    post_detail_for_profileimage = Post.query.get_or_404(post_id)
    profile_img = '/profile_image/'+post_detail_for_profileimage.author.profile_image
    return render_template('facebook_single_post_with_comment.html', total_count_friend_request=total_count_friend_request, myname=current_user, post_detail=post_detail, user_comment_detail=user_comment_detail, profile_img=profile_img)


@post.route("/post_with_like/<int:post_id>")
@login_required
def post_with_like(post_id):
    user_like_detail = db.session.query(User.id, User.firstname, User.lastname).filter(
        Reaction.reaction == '1', Reaction.postid == post_id, Reaction.user_id == User.id).all()
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    post_detail = db.session.query(
        User, Post).filter(Post.id == post_id).first()
    post_detail_for_profileimage = Post.query.get_or_404(post_id)
    profile_img = '/profile_image/'+post_detail_for_profileimage.author.profile_image
    return render_template('facebook_single_post_with_like.html', total_count_friend_request=total_count_friend_request, myname=current_user, post_detail=post_detail, user_like_detail=user_like_detail, profile_img=profile_img)


@post.route("/addpost", methods=["GET", "POST"])
@login_required
def addpost():
    if request.method == 'POST':
        if request.form.get('postimage') != "":
            postimage_data = request.files['postimage']
            if postimage_data and '.' in postimage_data.filename and \
                    postimage_data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_POST:
                post_image_filename = secure_filename(
                    postimage_data.filename)
                postimage_data.save(os.path.join(
                    UPLOAD_FOLDER_POST, post_image_filename))
                addpost_with_image = Post(post_description=request.form.get(
                    'postdescription'), post_image=post_image_filename, author=current_user)
                db.session.add(addpost_with_image)
                db.session.commit()
                flash('post add successfully', 'success')
                return redirect(url_for('views.home'))
        elif request.form.get('postdescription') == "":
            flash('post description cannot be empty', 'warning')
            return redirect(url_for('views.home'))
        else:
            addpost_without_image = Post(post_description=request.form.get(
                'postdescription'), post_image="none", author=current_user)
            db.session.add(addpost_without_image)
            db.session.commit()
            flash('post add successfully', 'success')
    return redirect(url_for('views.home'))
