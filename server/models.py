from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)


class Hero(db.Model, SerializerMixin):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    super_name = db.Column(db.String)

    # add relationship
    hero_powers=db.relationship('HeroPower', back_populates='heroes')
    # add serialization rules
    serialize_rules=('-hero_powers',)

    def __repr__(self):
        return f'<Hero {self.id}>'


class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)

    # add relationship
    heros_powers=db.relationship('HeroPower', back_populates='powers')
    # add serialization rules
    serialize_rules=('-heros_powers',)
    # add validation
    @validates('description')
    def validate_description(self,key,description):
        if len(description)<20:
            raise ValueError("Description has to be atleast 20 characters long!")
        else:
            return description
        

    def __repr__(self):
        return f'<Power {self.id}>'


class HeroPower(db.Model, SerializerMixin):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String, nullable=False)
    hero_id=db.Column(db.Integer, db.ForeignKey('heroes.id'))
    power_id=db.Column(db.Integer, db.ForeignKey('powers.id'))

    # add relationships
    powers=db.relationship('Power', back_populates='heros_powers')
    heroes=db.relationship('Hero',back_populates='hero_powers')
    
    # add serialization rules
    serialize_rules = ('-hero.hero_powers', '-power.heros_powers')

    # add validation
    strengths=['Strong',"Weak","Average"]
    @validates('strength')
    def validate_strength(self,key,strength):
        if strength not in self.strengths:
            raise ValueError(f"{strength} not a valid entry!")
        else:
            return strength

    def __repr__(self):
        return f'<HeroPower {self.id}>'
