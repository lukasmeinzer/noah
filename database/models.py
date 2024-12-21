from sqlalchemy import Column, Integer, BigInteger, String, Text, Date, Boolean, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    first_name = Column(String(50))  # Specify length
    last_name = Column(String(50), nullable=True)  # Specify length
    zip_code = Column(String(10), nullable=True)  # Specify length
    markets = Column(Text, nullable=True)  # Store as JSON string
    products = Column(Text, nullable=True)  # Store as JSON string

    offers = relationship("OfferModel", back_populates="user")

class OfferModel(Base):
    __tablename__ = 'offers'
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id'))
    supermarkt = Column(String(100))  # Specify length
    gesuchtes_produkt = Column(String(100))  # Specify length
    beschreibung = Column(Text)
    preis = Column(String(20))  # Specify length
    alter_preis = Column(String(20), nullable=True)  # Specify length
    referenz_preis = Column(String(20), nullable=True)  # Specify length
    requiresLoyaltyMembership = Column(Boolean)
    gültig_von = Column(String(10))
    gültig_bis = Column(String(10))
    gefundenes_produkt = Column(String(100))  # Specify length
    image = Column(String(512))  # Specify length

    user = relationship("UserModel", back_populates="offers")

class Feedback(Base):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True, autoincrement=True)
    timestamp = Column(String(50))  # Specify length
    feedback = Column(Text)

DATABASE_URL = "mysql://root:root@87.106.165.63/noah"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)