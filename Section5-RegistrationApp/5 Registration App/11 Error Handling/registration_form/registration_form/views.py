from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for

from .extensions import db
from .models import Language, Topic, Member

main = Blueprint('main', __name__)

@main.route('/', methods=['GET', 'POST'], defaults={'member_id' : None})
@main.route('/<int:member_id>', methods=['GET', 'POST'])
def index(member_id):

    member = None
    if member_id:
        member = Member.query.get_or_404(member_id)

    errors = {}

    if request.method == 'POST':
        # Gather Form Input
        email = request.form['email']
        password = request.form['password']
        location = request.form['location']
        first_learn_date = request.form['first_learn_date']
        fav_language = request.form['fav_language']
        about = request.form['about']
        learn_new_interest = request.form['learn_new_interest']
        interest_in_topics = request.form.getlist('interest_in_topics') # getlist() is used to get all values of a multi-select field

        if not email:
            errors['email'] = 'You must have an email address.'
        if not password and not member_id:
            errors['password'] = 'You must have a password.'
        if not location:
            errors['location'] = 'You must have a location.'
        if not first_learn_date:
            errors['first_learn_date'] = 'You must have a first learn date.'
        if not about:
            errors['about'] = 'You must say something about yourself.'
        if not interest_in_topics:
            errors['interest_in_topics'] = 'You must select at least one topic.'

        if not errors:
            if member:
                member.email = email

                if password:
                    member.password = password

                member.location = location
                member.first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d')
                member.fav_language = fav_language
                member.about = about
                member.learn_new_interest = (True if learn_new_interest == 'yes' else False)

                member.interest_in_topics[:] = []

            else:
                member = Member(
                    email = email,
                    password = password,
                    location = location,
                    first_learn_date = datetime.strptime(first_learn_date, '%Y-%m-%d'),# The datetime.strptime() function is used to convert the string input from the form into a datetime object that can be stored in the database.
                    fav_language = fav_language,
                    about = about,
                    learn_new_interest = (True if learn_new_interest == 'yes' else False)
                )

                db.session.add(member)

            for topic_id in interest_in_topics:
                topic = Topic.query.get(int(topic_id))
                member.interest_in_topics.append(topic)

            db.session.commit()

            return redirect(url_for('main.index', member_id=member.id))

    languages = Language.query.all()
    topics = Topic.query.all()

    # If there are errors, we want to re-render the form with the previously entered data and the error messages.
    context = {
        'member_id' : member_id,
        'languages' : languages,
        'topics' : topics,
        'member' : member,
        'errors' : errors
    }

    return render_template('form.html', **context)# This code defines a Flask Blueprint for the main routes of the application. It includes a route for the index page, which can handle both GET and POST requests. The route can also accept an optional member_id parameter, which is used to retrieve a specific member from the database.