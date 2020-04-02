import click
import os
import requests
import inspect
from requests.exceptions import HTTPError
from dotenv import load_dotenv
from celery import Celery
from celery.schedules import crontab

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))
script_name = inspect.getfile(inspect.currentframe()).split('.')[0]


class Config(object):
    NEWS_API_KEY = os.environ.get('NEWS_API_KEY')
    JOBS_APP_TOKEN = os.environ.get('JOBS_APP_TOKEN')
    JOBS_APP_NAME = os.environ.get('') or 'webnews.jobs'
    WEBNEWS_API_BASE_URL = os.environ.get('WEBNEWS_API_BASE_URL') or 'http://127.0.0.1:5000/api/v1.0'
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
    CELERY_BACKEND_URL = os.environ.get('CELERY_BACKEND_URL')
    CATEGORIES = os.environ.get('CATEGORIES') or 'Technology,Business,Health,Entertainment,Lifestyle,Politics,World'


scheduler = Celery(
    script_name,
    broker=Config.CELERY_BROKER_URL,
    backend=Config.CELERY_BACKEND_URL,
)
scheduler.conf.beat_schedule = {
    'synchronize-every-30-minutes': {
        'task': 'scheduler.news_synchronize',
        'schedule': crontab(minute='*/30')
    },
}
scheduler.conf.timezone = 'Europe/Zurich'


class API(object):

    @staticmethod
    def call_api(model, method, payload=None):
        headers = {
            'application': Config.JOBS_APP_NAME,
            'token': Config.JOBS_APP_TOKEN,
            'Content-Type': 'application/json'
        }
        url = '{}/{}'.format(Config.WEBNEWS_API_BASE_URL, model)
        try:
            if payload is not None:
                response = requests.request(method=method, url=url, headers=headers, json=payload)
            else:
                response = requests.request(method=method, url=url, headers=headers)
            response.raise_for_status()
            return response
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return None

    @staticmethod
    def show_statistics():
        headers = {
            'Content-Type': 'application/json'
        }
        url = '{}/{}'.format(Config.WEBNEWS_API_BASE_URL, 'stats')
        print('>>> Statistics:')
        try:
            response = requests.request(method='GET', url=url, headers=headers)
            response.raise_for_status()
            print('-> {} categories\n-> {} news\n-> {} keywords'.format(
                response.json()['count']['categories'],
                response.json()['count']['news'],
                response.json()['count']['tags']
            ))
        except HTTPError as http_err:
            print(f'### ERROR: HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'### ERROR: Other error occurred: {err}')

    @staticmethod
    def update_news_from_provider(categories):
        """
            We are using the API News API for retrieving the news. In developer mode we can
            query only every 15mn, so this is the why of this scheduler.
            we are going to query all the categories, and the 'top headlines' for the US.
            of course, this is just a first step, and it will have to be improved later.
        """
        collected_news = []
        headers = {
            'X-Api-Key': Config.NEWS_API_KEY,
            'Content-Type': 'application/json'
        }
        # starts with the headlines for US
        try:
            response = requests.request(
                method='GET',
                url='https://newsapi.org/v2/top-headlines?country=us',
                headers=headers
            )
            response.raise_for_status()
            # do we have an error?
            if response.json()['status'] == 'error':
                # later we will have to do something better than that
                print('an error "{}" happened during the query. the message is: {}'.format(
                    response.json()['code'],
                    response.json()['message']
                ))
            else:
                # no errors, so build the result list
                for article in response.json()['articles']:
                    if article['description']:
                        n = {
                            'category': 'headlines',
                            'title': article['title'],
                            'source': article['url'],
                            'photo': article['urlToImage'],
                            'author': article['author'],
                            'date_publish': article['publishedAt'],
                            'content': article['description'],
                            'is_headline': 'yes',
                            'is_top_story': 'yes',
                        }
                        collected_news.append(n)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')

        # and now we are doing the same for all the categories to consult
        try:
            all_categories = categories.split(',')
            for c in all_categories:
                category = c.strip()
                response = requests.request(
                    method='GET',
                    url='https://newsapi.org/v2/everything?q={}'.format(category),
                    headers=headers
                )
                response.raise_for_status()
                # do we have an error?
                if response.json()['status'] == 'error':
                    # later we will have to do something better than that. really.
                    print('an error "{}" happened during the processing of {}. the message is: {}'.format(
                        response.json()['code'],
                        category,
                        response.json()['message']
                    ))
                else:
                    # no errors, so build the result list
                    for article in response.json()['articles']:
                        if article['description']:
                            n = {
                                'category': category.title(),
                                'title': article['title'],
                                'source': article['url'],
                                'photo': article['urlToImage'],
                                'author': article['author'],
                                'date_publish': article['publishedAt'],
                                'content': article['description'],
                                'is_headline': 'no',
                                'is_top_story': 'no'
                            }
                            collected_news.append(n)
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')
        except Exception as err:
            print(f'Other error occurred: {err}')
        return collected_news


@scheduler.task()
def news_synchronize():
    for h in API.update_news_from_provider(categories=Config.CATEGORIES):
        API.call_api(model='webnews', method='POST', payload=h)


@click.group()
@click.pass_context
def news(ctx):
    """news jobs commands."""
    ctx.ensure_object(dict)
    ctx.obj['TASK_ID'] = -1


@news.command()
@click.pass_context
def synchronize(ctx):
    """Launch the synchronization of the news database"""
    task = news_synchronize.delay()
    ctx.obj['TASK_ID'] = task.id
    print('>>> Synchronize task scheduled. use status to check when it is completed.')


@news.command()
@click.pass_context
def start_worker(ctx):
    """Start a celery worker"""
    print('>>> Start the celery worker. Use CTRL+C to stop it.')
    # we have to add --pool=solo otherwise it can not run on Windows
    os.system("celery -A {} worker --pool=solo --loglevel=info".format(script_name))


@news.command()
@click.pass_context
def start_beat(ctx):
    """Start the celery scheduler"""
    print('>>> Start the celery scheduler. Use CTRL+C to stop it.')
    os.system("celery -A {} beat".format(script_name))


@news.command()
@click.pass_context
def start_flower(ctx):
    """Start flower monitoring web interface"""
    print('>>> Start the flower on port 5555. Use CTRL+C to stop it.')
    os.system("celery -A {} flower --port=5555".format(script_name))


@news.command()
@click.pass_context
def status(ctx):
    """Check the status of the celery workers"""
    API.show_statistics()
    print('>>> Status of the platform:')
    os.system("celery -A {} status".format(script_name))
    print('>>> Active workers status:')
    os.system("celery -A {} inspect active".format(script_name))


if __name__ == '__main__':
    news(obj={})
