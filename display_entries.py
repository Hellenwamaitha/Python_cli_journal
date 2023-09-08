from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Mycli.models import JournalEntry, User, Tag

# Create an SQLite database engine and establish a session
engine = create_engine('sqlite:///my_journal_app_new.db')
Session = sessionmaker(bind=engine)

def create_user():
    username = input("Enter a username for the new user: ")

    with Session() as session:
        # Check if the username already exists
        existing_user = session.query(User).filter_by(username=username).first()

        if existing_user:
            print("User with that username already exists.")
        else:
            new_user = User(username=username)
            session.add(new_user)
            session.commit()
            print(f"User '{username}' created successfully!")

def display_entries():
    # Create a session
    with Session() as session:
        # Retrieve and display journal entries
        entries = session.query(JournalEntry).all()

        if not entries:
            print("No journal entries found.")
        else:
            print("Journal Entries:")
            for entry in entries:
                print(f"ID: {entry.id}")
                print(f"Title: {entry.title}")
                print(f"Content: {entry.content}")
                print(f"Created At: {entry.created_at}")
                if entry.user:
                    print(f"User: {entry.user.username}")
                if entry.tags:
                    print(f"Tags: {', '.join(tag.name for tag in entry.tags)}")
                print()

def create_entry():
    title = input("Enter the title for your new entry: ")
    content = input("Enter the content for your new entry: ")

    # Collect user information
    author_username = input("Enter your username (to associate this entry with yourself): ")

    with Session() as session:
        user = session.query(User).filter_by(username=author_username).first()

        if user is None:
            print(f"User with username '{author_username}' not found. Please create the user first.")
            return

        # Collect tags (optional)
        tags_input = input("Enter tags for the entry (comma-separated): ")
        tags = [tag.strip() for tag in tags_input.split(",")]

        new_entry = JournalEntry(title=title, content=content, user=user)

        # Add tags to the entry (if provided)
        if tags:
            existing_tags = session.query(Tag).filter(Tag.name.in_(tags)).all()
            new_entry.tags.extend(existing_tags)

        session.add(new_entry)
        session.commit()
        print("New entry created successfully!")

def delete_entry():
    entry_id = input("Enter the ID of the entry you want to delete: ")

    with Session() as session:
        entry = session.query(JournalEntry).filter_by(id=entry_id).first()

        if entry:
            session.delete(entry)
            session.commit()
            print("Entry deleted successfully!")
        else:
            print("Entry not found.")

def search_entries():
    search_term = input("Enter a keyword to search for in journal entries: ")

    with Session() as session:
        entries = session.query(JournalEntry).filter(
            JournalEntry.title.like(f"%{search_term}%") |
            JournalEntry.content.like(f"%{search_term}%")
        ).all()

        if not entries:
            print("No matching journal entries found.")
        else:
            print("Matching Journal Entries:")
            for entry in entries:
                print(f"ID: {entry.id}")
                print(f"Title: {entry.title}")
                print(f"Content: {entry.content}")
                print(f"Created At: {entry.created_at}")
                if entry.user:
                    print(f"User: {entry.user.username}")
                if entry.tags:
                    print(f"Tags: {', '.join(tag.name for tag in entry.tags)}")
                print()

def main():
    print("Welcome to My Journal App!")
    while True:
        print("Options:")
        print("1. Display Journal Entries")
        print("2. Create a New Entry")
        print("3. Delete a Journal Entry")
        print("4. Search for a Journal Entry")
        print("5. Create a New User")  # Option to create users
        print("6. Quit")

        choice = input("Enter your choice: ")

        if choice == "1":
            display_entries()
        elif choice == "2":
            create_entry()
        elif choice == "3":
            delete_entry()
        elif choice == "4":
            search_entries()
        elif choice == "5":
            create_user()  
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()
