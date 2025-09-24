from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column,  relationship
from typing import List
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'user'
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    nickname: Mapped[str] = mapped_column(String(20), nullable=True)
    age: Mapped[int] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False)
    #relacion 1-1
    profile: Mapped['Profile'] = relationship(back_populates = "user", uselist=False) 
    #### IMPORTANTE EL LIST EN EL MAPPED!!! SINO SE PASARAN 1 HORA O MAS, COMO EN CLASE, DANDOSE GOLPE EN LA CABEZA
    ### relacion de uno a muchos
    posts: Mapped[List['Post']]= relationship(back_populates = "author", uselist=True) #relacion 1-N
    ### relacion de muchos a muchos a traves de tabla de asociacion
    groups: Mapped[List['UserGroup']] = relationship("UserGroup",back_populates = "groups", uselist=True)
 

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
            "nickname": self.nickname,
            "age": self.age,
            #estamos extrayendo el titulo y el contenido de cada post que el usuario el es autor y si no hay post, devuelve None
            "posts": [{"title": post.title, "content": post.content} for post in self.posts] if self.posts else None,
            #extrasemos de profile solo la info de bio si tenemos un profile, sino, None 
            "profile": {
                "bio": self.profile.bio
            } if self.profile else None,
            #mostramos los grupos a los que pertenece el usuario si tiene alguno, sino []
            "groups": [group.serialize() for group in self.groups or []]
        }
# ------      1 - 1  user-profile
class Profile(db.Model):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(primary_key=True)
    bio: Mapped[str] = mapped_column(String(120), nullable=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #relacion 1-1 con user
    user: Mapped["User"] = relationship(back_populates = "profile", uselist=False) #devuelve UN solo regsitro, por eso uselist=False
    
    def serialize(self):
        return {
            "id": self.id,
            "bio": self.bio,
            #devolvemos nickname del usuario al que le pertenece el profile
            "user": {
                "nickname": self.user.nickname
            }
        }
    
# ------- 1 - N
class Post(db.Model):
    __tablename__ = 'post'
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    content: Mapped[str] = mapped_column(String(250), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    #el autor es uno solo, por eso no usamos lista 
    author: Mapped["User"] = relationship(back_populates='posts', uselist=False) ##AQUI ES UNO, ASI QUE NO NECESITAMOS EL LIST
    
    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "content": self.content,    
            #podemos acceder directamente al nickname del autor por ser uno soloo        
            "author": self.author.nickname
        }

# ----- N - N

class Group(db.Model):
    __tablename__ = 'group'
    id: Mapped[int] = mapped_column(primary_key=True)
    name:Mapped[str] = mapped_column(String(25), nullable=False)
    #relacion N-N
    members: Mapped[List["UserGroup"]] = relationship("UserGroup", back_populates='user', uselist=True)

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            #mostramos los miembros a los que pertenece el usuario si tiene alguno, sino []
            "members": [member.serialize() for member in self.members or []]
        }

#tabla de asociacion
class UserGroup(db.Model):
    __tablename__ = 'user_groups'
    #id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"), primary_key=True)
    group_id = mapped_column(ForeignKey("group.id"), primary_key=True)
    groups: Mapped["User"] = relationship('User', back_populates='groups', uselist=False)
    user: Mapped["Group"] = relationship("Group", back_populates='members', uselist=False)

    def serialize(self):
        return {
            "user_id": self.user_id,
            "group_id": self.group_id
        }
