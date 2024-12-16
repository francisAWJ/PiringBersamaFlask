from datetime import datetime, timezone
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db, login

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    first_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))
    last_name: so.Mapped[Optional[str]] = so.mapped_column(sa.String(30))

    donations: so.WriteOnlyMapped['Donation'] = so.relationship(back_populates='author')

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Donation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    address: so.Mapped[str] = so.mapped_column(sa.String(256))
    phone_number: so.Mapped[str] = so.mapped_column(sa.String(14))

    food_type: so.Mapped[str] = so.mapped_column(sa.String(100))
    portions: so.Mapped[int] = so.mapped_column()
    food_desc: so.Mapped[str] = so.mapped_column(sa.String(256))
    donation_date: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))

    user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
    author: so.Mapped[User] = so.relationship(back_populates='donations')

    def __repr__(self):
        return '<Donation from {}>'.format(self.author)
    
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))
    