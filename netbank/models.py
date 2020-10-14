from netbank import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)    
    password = db.Column(db.String(60), nullable=False)
    account = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username