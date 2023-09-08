
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Mycli.models import JournalEntry, User, Tag, Base

# Create an SQLite database engine and establish a session
engine = create_engine('sqlite:///my_journal_app_new.db')
Session = sessionmaker(bind=engine)

# Create the tables if they don't exist
Base.metadata.create_all(engine)

# Create a session
with Session() as session:
    # Create a user
    user = User(username='Alice')
    session.add(user)

    # Create tags
    tag1 = Tag(name='Personal')
    tag2 = Tag(name='Work')
    session.add_all([tag1, tag2])

    # Create journal entries
    entry1 = JournalEntry(
        title='My First Entry',
        content='This is the content of my first journal entry.',
        created_at=datetime.now(),
        user=user,
        tags=[tag1]
    )
    entry2 = JournalEntry(
        title='Another Entry',
        content='This is another journal entry.',
        created_at=datetime.now(),
        user=user,
        tags=[tag2]
    )

    # Add journal entries to the session
    session.add_all([entry1, entry2])

    # Commit the changes to the database
    session.commit()

print('Data seeded successfully.')

