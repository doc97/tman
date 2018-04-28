from application import db


class Tag(db.Model):
    __tablename__ = 'Tag'
    id = db.Column('id', db.Integer, primary_key=True)
    account_id = db.Column('account_id', db.Integer, db.ForeignKey('Account.id'), nullable=False)

    name = db.Column('name', db.Unicode, nullable=False)

    def __init__(self, account_id, name):
        self.account_id = account_id
        self.name = name
