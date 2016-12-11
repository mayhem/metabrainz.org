from metabrainz.testing import FlaskTestCase
from flask import url_for


class IndexViewsTestCase(FlaskTestCase):

    def test_homepage(self):
        response = self.client.get(url_for('index.home'))
        self.assert200(response)

    def test_contact(self):
        response = self.client.get(url_for('index.contact'))
        self.assert200(response)

    def test_about(self):
        response = self.client.get(url_for('index.about'))
        self.assert200(response)

    def test_projects(self):
        response = self.client.get(url_for('index.projects'))
        self.assert200(response)

    def test_team(self):
        response = self.client.get(url_for('index.team'))
        self.assert200(response)

    def test_sponsors(self):
        response = self.client.get(url_for('index.sponsors'))
        self.assert200(response)

    def test_bad_customers(self):
        response = self.client.get(url_for('index.bad_customers'))
        self.assert200(response)

    def test_privacy_policy(self):
        response = self.client.get(url_for('index.privacy_policy'))
        self.assert200(response)

    def test_about_customers(self):
        response = self.client.get(url_for('index.about_customers_redirect'))
        self.assertRedirects(response, url_for('users.supporters_list'))
