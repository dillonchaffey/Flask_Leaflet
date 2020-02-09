from sqlalchemy import Column
from sqlalchemy.types import Integer, Text, String


class User(db.Model):
    id = Column(Integer,
                primary_key=True)
    username = Column(String(80),
                      unique=True, nullable=False)
    email = Column(String(120),
                   unique=True,
                   nullable=False)
    joined = Column(Datetime,
                    unique=False,
                    nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username