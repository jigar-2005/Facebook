from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Friends
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from . import db
from . import db, ALLOWED_EXTENSIONS_IMAGE, UPLOAD_FOLDER_PROFILE_IMAGE, UPLOAD_FOLDER_COVER_IMAGE
from werkzeug.utils import secure_filename
import os


setting = Blueprint('setting', __name__)


@setting.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    if request.method == 'POST':
        if check_password_hash(current_user.password, request.form.get('old_password')):
            if request.form.get('new_password') == request.form.get('confirm_new_password'):
                hashed_password = generate_password_hash(
                    request.form.get('new_password'), method='sha256')
                current_user.password = hashed_password
                db.session.commit()
                flash('password changed successfully', 'success')
                return render_template('facebook_password.html', myname=current_user)
            else:
                flash('new password does not match with confirm password', 'danger')
        else:
            flash('password wrong', 'danger')
    return render_template('facebook_password.html', myname=current_user, total_count_friend_request=total_count_friend_request)


@setting.route("/editprofile", methods=["GET", "POST"])
@setting.route("/setting", methods=["GET", "POST"])
def setting_page():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    return render_template('facebook_edit_profile.html', myname=current_user, total_count_friend_request=total_count_friend_request)


@setting.route("/update_profile", methods=["GET", "POST"])
@login_required
def editprofile():
    total_count_friend_request = Friends.query.filter(
        Friends.sentto == current_user.id, Friends.status == "0").count()
    if request.method == 'POST':
        if request.form.get('profile_image') != "":
            profile_image_data = request.files['profile_image']
            if profile_image_data and '.' in profile_image_data.filename and \
                    profile_image_data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE:
                current_user_profile_image = secure_filename(
                    profile_image_data.filename)
                profile_image_data.save(os.path.join(
                    UPLOAD_FOLDER_PROFILE_IMAGE, current_user_profile_image))
                current_user.profile_image = current_user_profile_image
                db.session.commit()
            else:
                current_user.profile_image = current_user.profile_image
                db.session.commit()
        if request.form.get('cover_image') != "":
            cover_image_data = request.files['cover_image']
            if cover_image_data and '.' in cover_image_data.filename and \
                    cover_image_data.filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS_IMAGE:
                current_user_cover_image = secure_filename(
                    cover_image_data.filename)
                cover_image_data.save(os.path.join(
                    UPLOAD_FOLDER_COVER_IMAGE, current_user_cover_image))
                current_user.cover_image = current_user_cover_image
                db.session.commit()
        else:
            current_user.cover_image = current_user.cover_image
            db.session.commit()
    current_user.firstname = request.form.get('firstname')
    current_user.lastname = request.form.get('lastname')
    current_user.email = request.form.get('email')
    current_user.date_of_birth = request.form.get('date_of_birth')
    db.session.commit()
    flash('Your account has been updated!', 'success')
    return render_template('facebook_edit_profile.html', myname=current_user, total_count_friend_request=total_count_friend_request)
