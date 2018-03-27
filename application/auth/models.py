from application import db

class Account(db.Model):
    __tablename__ = 'Account'
    id = db.Column('id', db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    username = db.Column('username', db.Unicode, nullable=False)
    password = db.Column('password', db.Unicode, nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def get_id(self):
        return self.id

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def is_authenticated(self):
        return True
