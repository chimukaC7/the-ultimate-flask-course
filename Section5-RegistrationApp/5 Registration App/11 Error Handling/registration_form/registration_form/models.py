from werkzeug.security import generate_password_hash

from .extensions import db

# Association table for many-to-many relationship between Member and Topic
member_topic_table = db.Table('member_topic',
        db.Column('member_id', db.Integer, db.ForeignKey('member.id'), primary_key=True),
        db.Column('topic_id', db.Integer, db.ForeignKey('topic.id'), primary_key=True)
    )


class Member(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(50))
    password_hash = db.Column(db.String(50))
    location = db.Column(db.String(30))
    first_learn_date = db.Column(db.DateTime)
    fav_language = db.Column(db.ForeignKey('language.id'))
    about = db.Column(db.Text)
    learn_new_interest = db.Column(db.Boolean)

    #use the relationship function to create a relationship between the Member and Language tables, this will allow us to access the language associated with a member using member.language and access the members associated with a language using language.member
    interest_in_topics = db.relationship(
        'Topic',
        secondary=member_topic_table,# use the secondary parameter to specify the association table that represents the many-to-many relationship between Member and Topic, this will allow us to access the topics associated with a member using member.interest_in_topics and access the members associated with a topic using topic.member
        lazy=True, # use the lazy parameter to specify how the related objects should be loaded, in this case we set it to True which means that the related objects will be loaded lazily, meaning that they will only be loaded when they are accessed for the first time, this can help improve performance by avoiding unnecessary database queries
        backref=db.backref('topic', lazy=True)# use the backref function to create a back reference from the Topic table to the Member table, this will allow us to access the members associated with a topic using topic.member
    )

    @property
    def password(self):
        raise AttributeError('Cannot view password')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)


class Language(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(10))


class Topic(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
