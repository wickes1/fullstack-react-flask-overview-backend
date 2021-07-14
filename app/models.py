import os
from sqlalchemy import create_engine, Table, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(os.getenv('DEV_DATABASE_URI'),
                       convert_unicode=True, echo=False)
Base = declarative_base(engine)


class Buildings(Base):
    __table__ = Table("buildings", Base.metadata,
                      autoload=True, autoload_with=engine)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Buildings_gfa(Base):
    __table__ = Table("buildings_gfa", Base.metadata,
                      autoload=True, autoload_with=engine)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Energy_star_rating(Base):
    __table__ = Table("energy_star_rating", Base.metadata,
                      autoload=True, autoload_with=engine)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Metrics(Base):
    __table__ = Table("metrics", Base.metadata,
                      autoload=True, autoload_with=engine)

    def serialize(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# User.__table__.create(db.session.bind)


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    public_id = Column(String(50), unique=True)
    username = Column(String(50))
    password = Column(String(80))
    admin = Column(Boolean)

    def serialize(self):
        return {"public_id": self.public_id, "username": self.username, "password": self.password, "admin": self.admin}


if __name__ == '__main__':
    # test
    from sqlalchemy.orm import scoped_session, sessionmaker
    db_session = scoped_session(sessionmaker(bind=engine))
    print(User.serialize(db_session.query(User).first()))
