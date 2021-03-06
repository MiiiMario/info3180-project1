"""
Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/
This file creates your application.
"""

from app import app, db, login_manager,allowed_files
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from forms import ProForm
from models import UserProfile
import os, datetime,random
from werkzeug.utils import secure_filename
from sqlalchemy import exc


###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')

@app.route("/profile", methods=["GET", "POST"])
def profile():
    form = ProForm()
    
    if request.method == "POST":
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            gender = form.gender.data
            email = form.email.data
            location = form.location.data
            biography = form.biography.data
            created = str(datetime.datetime.now()).split()[0]
                
            image = form.image.data
            image_name = secure_filename(image.filename)
            image.save(os.path.join(app.config['UPLOAD_FOLDER'],image_name))
                
            uid = random.randint(1,9999)   
            user = UserProfile(firstname, lastname, gender, email, location, biography, created, uid, image_name)
                
            db.session.add(user)
            db.session.commit()
                
                
                
            flash("Profile Has Been Added Successfully", "success")
            return redirect(url_for("profiles"))
    return render_template("create_profile.html", form = ProForm)
    
@app.route('/profiles', defaults={'userid': None})
@app.route('/profiles')
def profiles(uid):
    if not uid:
        prolist = db.session.query(UserProfile).all()
        if not prolist:
            flash('No users found.', 'danger')
            return redirect(url_for('add_profile'))
        return render_template('profiles.html',prolist = prolist)
    else:
        user = UserProfile.query.filter_by(uid=uid).first()
        if user is not None:
            return render_template('profile.html', user = user)   
        else:
            flash('User was not found','danger')
            return redirect(url_for('home'))


# user_loader callback. This callback is used to reload the user object from
# the user ID stored in the session
@login_manager.user_loader
def load_user(id):
    return UserProfile.query.get(int(id))

###
# The functions below should be applicable to all Flask apps.
###


@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port="8080")
