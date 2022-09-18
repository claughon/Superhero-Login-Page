from flask import Blueprint, render_template

"""
Note that in the below code,
some arguments are specified when creating the Blueprint object.
The first argument, 'site' is the blueprint's name which is used
by Flask's routing mechanism

The second argumnet, __name__, is the Blueprint's import name,
which Flask uses to locate the Blueprint's resources
"""

site = Blueprint('site', __name__, template_folder = 'site_templates')

@site.route('/')
def home():
    return render_template('index.html')

@site.route('/profile')
def profile():
    return render_template('profile.html')