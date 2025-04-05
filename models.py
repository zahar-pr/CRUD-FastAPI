from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from database import Base

class Provider(Base):
    __tablename__ = "providers"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    email = Column(String(255), nullable=True)

    games = relationship("Game", back_populates="provider")

class Game(Base):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    is_published = Column(Boolean, default=True, nullable=False)
    provider_id = Column(Integer, ForeignKey("providers.id"), nullable=False)

    provider = relationship("Provider", back_populates="games")
