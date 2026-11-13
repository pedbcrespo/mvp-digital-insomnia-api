from config.db_config import db
class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(255), unique=True, nullable=False)


    def __init__(self, username: str):
        self.username = username


    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
        }