import click
from Mycli.models import JournalEntry, User, Tag, Session

@click.group()
def cli():
    """CLI application for managing journal entries, users, and tags."""
    pass

@cli.command()
@click.option('--title', prompt='Title', help='Title of the journal entry')
@click.option('--content', prompt='Content', help='Content of the journal entry')
@click.option('--user', type=str, prompt='Username', help='Username of the author')
@click.option('--tags', type=str, help='Tags for the entry (comma-separated)')
def create_entry(title, content, user, tags):
    """Create a new journal entry."""
    with Session() as session:
        user_obj = session.query(User).filter_by(username=user).first()

        if not user_obj:
            click.echo(f"User '{user}' does not exist.")
            return

        new_entry = JournalEntry(title=title, content=content, user=user_obj)
        
        if tags:
            tag_names = [tag.strip() for tag in tags.split(',')]
            for tag_name in tag_names:
                tag = session.query(Tag).filter_by(name=tag_name).first()
                if tag is None:
                    tag = Tag(name=tag_name)
                new_entry.tags.append(tag)
        
        session.add(new_entry)
        session.commit()
        click.echo('Journal entry created successfully.')

@cli.command()
@click.option('--user-id', type=int, prompt='User ID', help='ID of the user')
def search_entries_by_user(user_id):
    """Search for journal entries by a specific user."""
    with Session() as session:
        user = session.query(User).get(user_id)

        if not user:
            click.echo(f"User with ID {user_id} does not exist.")
            return

        entries = user.entries
        if not entries:
            click.echo(f'No journal entries found for user {user.username}.')
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
