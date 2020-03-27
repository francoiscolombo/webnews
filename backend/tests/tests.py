# launch on command line with:
# python -m unittest -v tests.tests (default unit testing with python 3)
# or python -m pytest -v tests/tests.py (uses pytest for better reporting)
# please note that for now only the model is tested, but we should also test the routes.
import unittest
from app import create_app, db
from app.models.auth import Auth
from app.models.weather import Weather
from app.models.webnews import WebNews, WebNewsKeyword, WebNewsCategory
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


class CategoryModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_model_auth(self):
        # create
        a = Auth()
        a.application = 'test'
        db.session.add(a)
        db.session.commit()
        self.assertTrue(a.id > 0, 'id must be defined, but it is not.')
        # find
        a = Auth.query.filter_by(application='test').first()
        self.assertIsNotNone(a, 'we did not find the test application')
        # get token
        token = a.get_token()
        self.assertIsNot(token, '', 'token is not provided')
        # get another object
        b = Auth.query.get(a.id)
        self.assertIsNotNone(b, 'we did not retrieve the test application by its id')
        # verify objects equals
        self.assertEqual(str(a), str(b), 'error: a is not b')
        # check token of a
        self.assertIsNotNone(a.verify_token(token), 'invalid token provided (a)')
        self.assertIsNotNone(b.verify_token(token), 'invalid token provided (b)')
        self.assertEqual(a.verify_token(token).application, 'test', 'a check token did not send the proper application')
        # check bad token
        self.assertIsNone(a.verify_token('i am a bad token'), 'check invalid token failed')
        # must not find undefined application
        c = Auth.query.filter_by(application='totolastiko').first()
        self.assertIsNone(c, 'search for undefined application did not fails as expected')
        d = Auth.query.get(123456)
        self.assertIsNone(d, 'get with value 123456 retrieve something but it should not')
        # delete
        e = Auth.query.get(a.id)
        self.assertEqual(e.application, 'test', 'cannot retrieve application test')
        db.session.delete(e)
        db.session.commit()
        f = Auth.query.get(a.id)
        self.assertIsNone(f, 'test application was not deleted')

    def test_model_weather(self):
        # create
        w = Weather()
        w.ip = '1.1.1.1'
        w.country = 'country'
        w.flag = 'flag'
        w.town = 'town'
        w.tendency = 'sunny'
        w.wind_speed = '0'
        w.temperature_min = '20'
        w.temperature_max = '25'
        w.temperature = '23'
        w.humidity = '50%'
        w.clouds = 'none'
        db.session.add(w)
        db.session.commit()
        self.assertTrue(w.id > 0, 'id must be defined, but it is not.')
        # search by IP
        ww = Weather.query.filter_by(ip='1.1.1.1').first()
        self.assertIsNotNone(ww, 'we did not find the test weather')
        # compare results
        self.assertEqual(w.ip, ww.ip, 'ip is not identical but it should be')
        self.assertEqual(w.country, ww.country, 'country is not identical but it should be')
        self.assertEqual(w.flag, ww.flag, 'flag is not identical but it should be')
        self.assertEqual(w.town, ww.town, 'town is not identical but it should be')
        self.assertEqual(w.tendency, ww.tendency, 'tendency is not identical but it should be')
        self.assertEqual(w.wind_speed, ww.wind_speed, 'wind speed is not identical but it should be')
        self.assertEqual(w.temperature_min, ww.temperature_min, 'temperature min is not identical but it should be')
        self.assertEqual(w.temperature_max, ww.temperature_max, 'temperature max is not identical but it should be')
        self.assertEqual(w.temperature, ww.temperature, 'temperature is not identical but it should be')
        self.assertEqual(w.humidity, ww.humidity, 'humidity is not identical but it should be')
        self.assertEqual(w.clouds, ww.clouds, 'clouds is not identical but it should be')
        # search unknown IP
        w2 = Weather.query.filter_by(ip='2.2.2.2').first()
        self.assertIsNone(w2, 'we did find a weather row for an unknown IP')
        # delete
        wd = Weather.query.get(w.id)
        self.assertEqual(wd.ip, '1.1.1.1', 'cannot retrieve test weather')
        db.session.delete(wd)
        db.session.commit()
        f = Weather.query.get(w.id)
        self.assertIsNone(f, 'test weather was not deleted')

    def test_model_webnews(self):
        # create category
        c = WebNewsCategory()
        c.name = 'test'
        db.session.add(c)
        db.session.commit()
        self.assertTrue(c.id > 0, 'id must be defined, but it is not.')
        # create 2 keywords
        k1 = WebNewsKeyword()
        k1.tag = 'keyword1'
        db.session.add(k1)
        k2 = WebNewsKeyword()
        k2.tag = 'keyword2'
        db.session.add(k2)
        db.session.commit()
        self.assertTrue(k1.id > 0, 'id must be defined, but it is not.')
        self.assertTrue(k2.id > 0, 'id must be defined, but it is not.')
        # create a news, associate it with the category and the first keyword
        n = WebNews()
        n.title = 'my news title'
        n.photo = 'my photo'
        n.author = 'me'
        n.source = 'the source'
        n.is_headline = 'yes'
        n.is_top_story = 'yes'
        n.content = 'my content is great'
        n.category_id = c.id
        n.keywords.append(k1)
        db.session.add(n)
        db.session.commit()
        self.assertTrue(n.id > 0, 'id must be defined, but it is not.')
        self.assertTrue(n in c.news, 'news not associated with the category')
        self.assertTrue(n in k1.related, 'keyword 1 not associated with the news')
        self.assertFalse(n in k2.related, 'keyword 2 should not be associated with the news')
        self.assertTrue(k1 in n.keywords, 'news not associated with the keyword1')
        # associate the news with the second keyword
        k2.related.append(n)
        db.session.commit()
        self.assertTrue(n in k2.related, 'keyword 2 should now be associated with the news')
        self.assertTrue(k2 in n.keywords, 'news should contains 2 keywords')
        # search unknown news
        n2 = WebNews.query.filter_by(title='whatever').first()
        self.assertIsNone(n2, 'we did find a news but we should not, it is whatever')
        # find news by author
        n2 = WebNews.query.filter_by(author='me').first()
        self.assertIsNotNone(n2, 'we did not retrieve the news by author name')
        # news should be identical
        self.assertEqual(n.title, n2.title, 'title should be the same but it is not')
        self.assertEqual(n.photo, n2.photo, 'photo should be the same but it is not')
        self.assertEqual(n.author, n2.author, 'author should be the same but it is not')
        self.assertEqual(n.source, n2.source, 'source should be the same but it is not')
        self.assertEqual(n.is_headline, n2.is_headline, 'is_headline should be the same but it is not')
        self.assertEqual(n.is_top_story, n2.is_top_story, 'is_top_story should be the same but it is not')
        self.assertEqual(n.content, n2.content, 'content should be the same but it is not')
        self.assertEqual(n.category_id, n2.category_id, 'category_id should be the same but it is not')
        # delete
        n3 = WebNews.query.get(n.id)
        self.assertEqual(n3.author, 'me', 'cannot retrieve test news')
        db.session.delete(n3)
        db.session.commit()
        f = WebNews.query.get(n.id)
        self.assertIsNone(f, 'test news was not deleted')
        self.assertFalse(n in c.news, 'news still associated with the category')
        self.assertFalse(n in k1.related, 'keyword 1 still associated with the news')
        self.assertFalse(n in k2.related, 'keyword 2 still associated with the news')


if __name__ == '__main__':
    unittest.main(verbosity=2)
