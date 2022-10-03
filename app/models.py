from . import db


class Role(db.Model):
    __tablename__ = "roles"
    # SqlAlchemy always needs an id
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users = db.relationship(
        "User", backref="role", lazy="dynamic"
    )  # To repr one-to-many

    def __repr__(self) -> str:
        return "<Role %r>" % self.name


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    # To repr the many-to-one relation
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    def __repr__(self):
        return "<User %r>" % self.username
