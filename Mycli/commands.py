import click
from models import JournalEntry, User, Tag, entry_tags
from models import Session

@click.group()
def cli():
    """CLI application for managing journal entries, users, and tags."""

@cli.command()
@click.option('--title', prompt='Title', help='Title of the journal entry')
@click.option('--content', prompt='Content', help='Content of the journal entry')
@click.option('--user', type=str, prompt='Username', help='Username of the author')
@click.option('--tags', type=str, help='Tags for the entry (comma-separated)')
def create_entry(title, content, user, tags):
    """Create a new journal entry."""
    with Session() as session:
        # Validate user input (point 2)
        if not title or not content or not user:
            click.echo('Title, content, and username are required.')
            return

        user_obj = session.query(User).filter_by(username=user).first()

        if not user_obj:
            click.echo(f"User '{user}' does not exist.")
            return

        # Create a new journal entry and associate it with the user
        new_entry = JournalEntry(title=title, content=content, user=user_obj)
        
        # Parse tags and associate them with the entry
        if tags:
            tag_names = [tag.strip() for tag in tags.split(',')]
            for tag_name in tag_names:
                # Check if the tag already exists
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tag(name=tag_name)
                new_entry.tags.append(tag)
        
        session.add(new_entry)
        session.commit()
        click.echo('Journal entry created successfully.')

@cli.command()
@click.option('--date', type=str, help='Search by date (YYYY-MM-DD)')
@click.option('--keyword', type=str, help='Search by keyword in titles or content')
def search_entries(date, keyword):
    """Search for journal entries by date or keyword."""
    with Session() as session:
        query = session.query(JournalEntry)

        if date:
            query = query.filter(JournalEntry.created_at.like(f'{date}%'))

        if keyword:
            query = query.filter((JournalEntry.title.like(f'%{keyword}%')) | (JournalEntry.content.like(f'%{keyword}%')))

        entries = query.all()
        if not entries:
            click.echo('No matching entries found.')
        else:
            for entry in entries:
                click.echo(f'Title: {entry.title}')
                click.echo(f'Content: {entry.content}')
                click.echo(f'Created At: {entry.created_at}')
                if entry.tags:
                    click.echo(f'Tags: {", ".join(tag.name for tag in entry.tags)}')
                click.echo('\n')

if __name__ == '__main__':
    cli()
