from flask import Blueprint, render_template, redirect, url_for
from metabrainz.model.user import User

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def home():
    return render_template(
        'index/index.html',
        good_users=User.get_featured(limit=4, with_logos=True),
        bad_users=User.get_featured(in_deadbeat_club=True, limit=4),
    )


@index_bp.route('/about')
def about():
    return render_template('index/about.html')


@index_bp.route('/projects')
def projects():
    return render_template('index/projects.html')
    

@index_bp.route('/team')
def team():
    return render_template('index/team.html')
    

@index_bp.route('/contact')
def contact():
    return render_template('index/contact.html')


@index_bp.route('/sponsors')
def sponsors():
    return render_template('index/sponsors.html')


@index_bp.route('/bad-customers')
def bad_customers():
    return render_template(
        'index/bad-customers.html',
        bad_users=User.get_featured(in_deadbeat_club=True),
    )


@index_bp.route('/privacy')
def privacy_policy():
    return render_template('index/privacy.html')


@index_bp.route('/about/customers.html')
def about_customers_redirect():
    return redirect(url_for('users.supporters_list') , 301)
