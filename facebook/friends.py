from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, login_required, logout_user, current_user
from .models import User, Friends
from . import db


friends = Blueprint('friends', __name__)


@friends.route("/addfriend<int:user_id>", methods=["GET", "POST"])
@login_required
def addfriend(user_id):
    exists_confirmed_frnd = Friends.query.filter(Friends.status == '1', (Friends.sentto == current_user.id) | (
        Friends.user_sender == current_user.id), (Friends.sentto == user_id) | (Friends.user_sender == user_id)).scalar()
    exists_block_frnd = Friends.query.filter(
        Friends.status == '2', Friends.sentto == current_user.id, Friends.user_sender == user_id).scalar()

    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    user = User.query.filter(User.id == user_id).first()
    addfriend = Friends(user_sender=current_user.id, sentto=user_id)
    exists_if_user_sender_current_user = Friends.query.filter(
        Friends.status == '0', Friends.user_sender == current_user.id, Friends.sentto == user_id).scalar()
    exists_if_user_sender_user_id = Friends.query.filter(
        Friends.status == '0', Friends.user_sender == user_id, Friends.sentto == current_user.id).scalar()
    if exists_if_user_sender_current_user:
        flash('Your Friend request has already send', 'warning')
    elif exists_if_user_sender_user_id:
        flash(user.firstname + " " + user.lastname +
              ' already sent you a friend request', 'warning')
    elif exists_confirmed_frnd:
        flash('you both are friends since previously', 'warning')
    elif exists_block_frnd:
        flash('you blocked the' + " " + user.firstname + " " +
              user.lastname + " Friend request", 'warning')
    else:
        db.session.add(addfriend)
        db.session.commit()
        flash('Your Friend request has send', 'success')
    return redirect(url_for('views.username', user_id=user_id, total_count_friend_request=total_count_friend_request))


@friends.route("/accept_friend_request/<userid>", methods=['GET', 'POST'])
@login_required
def accept_friend_request(userid):
    friend_request_accept = Friends.query.filter(
        Friends.status == '0', Friends.sentto == current_user.id, Friends.user_sender == userid).first()
    friend_request_accept.status = '1'
    db.session.commit()
    flash('Friend added', 'success')
    return redirect(url_for('friends.friend_request_receive'))


@friends.route("/accept_block_friend_request/<userid>", methods=['GET', 'POST'])
@login_required
def accept_block_friend_request(userid):
    friend_request_accept = Friends.query.filter(
        Friends.status == '2', Friends.sentto == current_user.id, Friends.user_sender == userid).first()
    friend_request_accept.status = '1'
    db.session.commit()
    flash('Friend added', 'success')
    return redirect(url_for('friends.block_user'))


@friends.route("/block_friend_request/<userid>", methods=['GET', 'POST'])
@login_required
def block_friend_request(userid):
    friend = Friends.query.filter(Friends.status == '0', Friends.sentto ==
                                  current_user.id, Friends.user_sender == userid).first()
    friend.status = '2'
    db.session.commit()
    flash('User blocked', 'success')
    return redirect(url_for('friends.friend_request_receive'))


@friends.route("/friend_request_receive")
@login_required
def friend_request_receive():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    friend_request_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image, Friends.request_sent_date).filter(
        Friends.status == '0', Friends.sentto == current_user.id, User.id == Friends.user_sender).all()
    return render_template('facebook_friend_request.html', myname=current_user, total_count_friend_request=total_count_friend_request, friend_request_detail=friend_request_detail)


@friends.route("/block_user")
@login_required
def block_user():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    block_friends_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image, Friends.request_sent_date).filter(
        Friends.status == '2', Friends.sentto == current_user.id, User.id == Friends.user_sender).all()
    return render_template('facebook_block_user.html', myname=current_user, total_count_friend_request=total_count_friend_request, block_friends_detail=block_friends_detail)


@friends.route("/myfriends")
@login_required
def myfriends():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    my_friends_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image).filter(
        Friends.status == '1', (Friends.sentto == current_user.id) | (Friends.user_sender == current_user.id), (Friends.sentto == User.id) | (Friends.user_sender == User.id), User.id != current_user.id).all()
    return render_template('facebook_myprofile_friends.html', myname=current_user, total_count_friend_request=total_count_friend_request, my_friends_detail=my_friends_detail)


@friends.route("/user_friend/<int:user_id>")
@login_required
def user_friend(user_id):
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    user_friends_detail = db.session.query(User.id, User.firstname, User.lastname, User.profile_image).filter(
        Friends.status == '1', (Friends.sentto == user_id) | (Friends.user_sender == user_id), (Friends.sentto == User.id) | (Friends.user_sender == User.id), User.id != user_id).all()
    if user_id == current_user.id:
        return redirect(url_for('views.myprofile'))
    user = User.query.filter(User.id == user_id).first()
    return render_template('facebook_user_friends.html', user=user, total_count_friend_request=total_count_friend_request, myname=current_user, user_friends_detail=user_friends_detail)
