import click
from app import db
from app.models.auth import Auth
from app.models.webnews import WebNews
from tabulate import tabulate


def register(app):

    @app.cli.group()
    def auth():
        """authorization commands."""
        pass

    @auth.command()
    @click.argument('application')
    def add(application):
        """Register a new application allowed to work with the API"""
        a = Auth.query.filter_by(application=application).first()
        if not a:
            a = Auth()
            a.application = application
            db.session.add(a)
            db.session.commit()
        print('>>> Application {} registered. Please use the following token to connect: {}'.format(
            a.application, a.get_token()
        ))

    @auth.command()
    @click.argument('application')
    def renew(application):
        """Renew the token for a registered application"""
        a = Auth.query.filter_by(application=application).first()
        if not a:
            raise RuntimeError('Application <' + application + '> does not exists yet, you have to add it first.')
        print('>>> Application {} is allowed. Please use the following token to connect: {}'.format(
            a.application, a.get_token()
        ))

    @auth.command()
    def show():
        """List all the registered applications"""
        print("List of allowed applications:\n----------------------------")
        for a in Auth.query.all():
            print('>>> Application {}'.format(a.application))

    @app.cli.group()
    def news():
        """news commands."""
        pass

    @news.command()
    def display():
        """List all the news"""
        records = []
        for n in WebNews.query.all():
            record = [n.title[:60], n.author[:20], n.photo[:30], n.source[:30], n.is_headline, n.is_top_story,
                      n.date_publish, n.content[:60], n.category_id]
            records.append(record)
        print(
            tabulate(
                records,
                headers=["title", "author", "photo", "source", "headline?", "top story?", "date", "content", "cat.id"],
                tablefmt="pretty"
            )
        )
