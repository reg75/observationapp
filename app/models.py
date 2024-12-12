from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, UniqueConstraint, ForeignKey
from datetime import datetime, timezone

db = SQLAlchemy()

class User(db.Model):
   # EN: Creates Users table
   # BR: Cria tabela 'Users' (Usuários)
   __tablename__ = "Users"
   User_ID = db.Column(
      db.Integer,
      primary_key=True
   )
   User_Forename = db.Column(
      db.String(64),
      nullable=False
   )
   User_Surname = db.Column(
      db.String(64),
      nullable=False
   )
   User_Email = db.Column(
      db.String(128),
      nullable=False,
      unique=True
   )

class Observation(db.Model):
   # EN: Creates Observations table
   # BR: Cria tabela 'Observations' (Observações de aula)
   __tablename__ = "Observations"
   Observation_ID = db.Column(
      db.Integer,
      primary_key=True
   )
   Observation_Date = db.Column(
      db.DateTime
   )
   Observation_Teacher = db.Column(
      db.Integer,
      ForeignKey("Users.User_ID"),
      nullable=False
   )
   Teacher = db.relationship("User", backref="observations") 
   Observation_Class = db.Column(
      db.String(8),
      nullable=False
   )
   Observation_Focus = db.Column(
      db.String(32),
      nullable=False
   )
   Observation_Strengths = db.Column(
      db.String(1000),
   )
   Observation_Weaknesses = db.Column(
      db.String(1000),
   )
   Observation_Comments = db.Column(
      db.String(1000),
   )

# Creates initial list of users / teachers
# Cria lista inicial de usuários / professores
def create_initial_data():
    if db.session.query(User).count() == 0:
        user1 = User(
            User_Forename="Chloe",
            User_Surname="Chen",
            User_Email = "chloe@myschool.co.uk"
        )
        user2 = User(
            User_Forename="Colleen",
            User_Surname="Murphy",
            User_Email = "colleen@myschool.co.uk"
        )
        
        user3 = User(
            User_Forename="Peter",
            User_Surname="Robinson",
            User_Email = "peter@myschool.co.uk"
        )
        user4 = User(
            User_Forename="Laura",
            User_Surname="Williams",
            User_Email = "laura@myschool.co.uk"
        )

        db.session.add_all([user1, user2, user3, user4])
        db.session.commit()