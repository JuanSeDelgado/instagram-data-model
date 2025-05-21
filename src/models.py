from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey, Enum  
from sqlalchemy.orm import Mapped, mapped_column, relationship 
from typing import List  

db = SQLAlchemy()

user_likes_post = Table(
    "user_likes_post",
    db.Model.metadata, 
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("post_id", ForeignKey("post.id"), primary_key=True),
)


class User(db.Model):
    __tablename__ = "user"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(
        String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)

    posts: Mapped[List["Post"]] = relationship(
        "Post", back_populates='user')  
    liked_posts: Mapped[List["Post"]] = relationship(
        "Post", secondary=user_likes_post, back_populates="liked_by")


class Follower(db.Model):
    __tablename__ = 'follower'
    user_from_id: Mapped[int] = mapped_column(primary_key=True)
    user_to_id: Mapped[int] = mapped_column(primary_key=True)


class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), nullable=False)
    user: Mapped['User'] = relationship("User", back_populates='posts')
    liked_by: Mapped[List["User"]] = relationship(
        "User", secondary=user_likes_post, back_populates='liked_posts')
    comments: Mapped[List["Comment"]] = relationship(
        "Comment", back_populates="post")
    media: Mapped[List["Media"]] = relationship("Media", back_populates="post")


class Comment(db.Model):
    __tablename__ = "comment"
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(250), nullable=False)
    author_id: Mapped[int] = mapped_column(ForeignKey(
        "user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship(
        "Post", back_populates="comments")


class Media(db.Model):
    __tablename__ = 'media'
    id: Mapped[int] = mapped_column(primary_key=True)
    type: Mapped[str] = mapped_column(
        Enum('image', 'video', name='media_types'), nullable=False)
    url: Mapped[str] = mapped_column(String(180), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="media")


def serialize(self):
    return {
        "id": self.id,
        "email": self.email,
        # do not serialize the password, its a security breach
    }


