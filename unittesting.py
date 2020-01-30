import unittest
from service import service
from utils import make_key
from random import randrange
service.testing = True

### OPEN URLS FILE AND CREATE SHORTCODES FOR TESTING ###

with open("urls.txt", "r") as urls:
    urls = urls.readlines()[:10]
    
urls = [x.rstrip() for x in urls]
shortcodes = [make_key(6) for x in range(len(urls))]

class TestApi(unittest.TestCase):
    
    def test_01_test(self):
        with service.test_client() as client:
            response = client.get('/')
            self.assertEqual(response.status_code, 200)
 
    def test_02_shorten(self):
        """Shorten urls from url file"""
        with service.test_client() as client:
            for x in range(len(urls)):
                sent = {'url': urls[x], "shortcode":shortcodes[x]}
                posting = client.post('/shorten',
                    json=sent)
                self.assertEqual(posting.status_code, 201)

    def test_03_shorten(self):
        """Shorten with no url"""
        with service.test_client() as client:
            sent = {'url': "", "shortcode":"123456"}
            posting = client.post('/shorten',
                    json=sent)
            self.assertEqual(posting.status_code, 400)

    def test_04_shorten(self):
        """Shorten with invalid key"""
        with service.test_client() as client:
            sent = {'url': "test.it", "shortcode":make_key(9)}
            posting = client.post('/shorten',
                json=sent)
            self.assertEqual(posting.status_code, 412)

    def test_05_shorten(self):
        """Shorten with invalid key"""
        with service.test_client() as client:
            sent = {'url': "test.it", "shortcode":"123p.4"}
            posting = client.post('/shorten',
                json=sent)
            self.assertEqual(posting.status_code, 412)

                
    def test_06_showShortcode(self):
        """Show the stats of all the stored shortcodes"""
        with service.test_client() as client:
            for x in range(len(urls)):
                response = client.get('/%s' % shortcodes[x])
                self.assertEqual(response.status_code, 302)


    def test_07_shortcodeStats(self):
        """ Show stats of unregistered shortcode """
        with service.test_client() as client:
            shortcode = '/aaaaaa'
            response = client.get(shortcode+"/stats")
            self.assertEqual(response.status_code, 404)
