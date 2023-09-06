from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

Base = declarative_base()

# Define the many-to-many relationship table for Entry and Tag
entry_tags = Table('entry_tags', Base.metadata,
    Column('entry_id', Integer, ForeignKey('journal_entries.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id'), primary_key=True)
)

class JournalEntry(Base):
    __tablename__ = 'journal_entries'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey('users.id'))

    # Define a many-to-one relationship with User
    user = relationship('User', back_populates='entries')

    # Define a many-to-many relationship with Tag
    tags = relationship('Tag', secondary=entry_tags, back_populates='entries')

class User(Base):
   __tablename__ = 'users'

   id = Column(Integer, primary_key=True)
   username = Column(String(50), nullable=False, unique=True)

   # Define a one-to-many relationship with JournalEntry
   entries = relationship('JournalEntry', back_populates='user')

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False, unique=True)

    # Define a many-to-many relationship with JournalEntry
    entries = relationship('JournalEntry', secondary=entry_tags, back_populates='tags')


