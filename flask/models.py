import re

import bcrypt as bcrypt
import pydantic
from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import func

password_regex = re.compile(
    "^(?=.*[a-z_])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&_])[A-Za-z\d@$!#%*?&_]{8,200}$"
)

engine = create_engine('postgresql://admin:1234@127.0.0.1:5432/flask_netology')
Base = declarative_base()
Session = sessionmaker(bind=engine)


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    user_name = Column(String(100), nullable=False, unique=True)

    email = Column(String)
    registration_time = Column(DateTime, server_default=func.now())
    password = Column(String, nullable=False)

    @classmethod
    def register(cls, session: Session, user_name: str, password: str):
        new_user = User(
            user_name=user_name,
            password=bcrypt.generate_password_hash(password.encode()).decode(),
        )
        session.add(new_user)
        try:
            session.commit()
            return new_user
        except IntegrityError:
            session.rollback()

    def check_password(self, password: str):
        return bcrypt.check_password_hash(self.password.encode(), password.encode())

    def to_dict(self):
        return {
            'user_name': self.user_name,
            'registration_time': int(self.registration_time.timestamp()),
            'id': self.id,
        }


class Ad(Base):
    __tablename__ = 'ad'

    id = Column(Integer, primary_key=True)
    title = Column(String(100), index=True)
    body = Column(String(500), index=True)
    stamp_time = Column(DateTime, server_default=func.now())
    owner_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'body': self.body,
            'stamp_time': self.stamp_time,
            'owner_id': self.owner_id
        }

Base.metadata.create_all(engine)


class CreateUserModel(pydantic.BaseModel):
    user_name: str
    password: str

    @pydantic.validator("password")
    def strong_password(cls, value: str):
        if not re.search(password_regex, value):
            raise ValueError("password to easy")

        return value
