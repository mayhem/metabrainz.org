from metabrainz.testing import FlaskTestCase
from metabrainz.api.views import DAILY_SUBDIR, WEEKLY_SUBDIR
from metabrainz.model.token import Token
from flask import url_for, current_app
import tempfile
import shutil
import os


class APIViewsTestCase(FlaskTestCase):

    def setUp(self):
        super(APIViewsTestCase, self).setUp()
        current_app.config['REPLICATION_PACKETS_DIR'] = self.path = tempfile.mkdtemp()
        os.mkdir(os.path.join(self.path, DAILY_SUBDIR))
        os.mkdir(os.path.join(self.path, WEEKLY_SUBDIR))
        self.token = Token.generate_token(owner_id=None)

    def tearDown(self):
        super(APIViewsTestCase, self).tearDown()
        shutil.rmtree(self.path)

    def test_info(self):
        self.assert200(self.client.get(url_for('api.info')))

    def test_replication_info(self):
        self.assert400(self.client.get(url_for('api.replication_info')))
        self.assert403(self.client.get(url_for('api.replication_info', token='fake')))

        resp = self.client.get(url_for('api.replication_info', token=self.token))
        self.assert200(resp)
        self.assertEquals(resp.json, {
            'last_packet': None,
            'last_packet_daily': None,
            'last_packet_weekly': None,
        })

        open(os.path.join(self.path, 'replication-1.tar.bz2'), 'a').close()
        open(os.path.join(self.path, DAILY_SUBDIR, 'replication-daily-1.tar.bz2'), 'a').close()
        open(os.path.join(self.path, WEEKLY_SUBDIR, 'replication-weekly-1.tar.bz2'), 'a').close()
        resp = self.client.get(url_for('api.replication_info', token=self.token))
        self.assert200(resp)
        self.assertEquals(resp.json, {
            'last_packet': 'replication-1.tar.bz2',
            'last_packet_daily': 'replication-daily-1.tar.bz2',
            'last_packet_weekly': 'replication-weekly-1.tar.bz2',
        })

    def test_replication_hourly(self):
        self.assert400(self.client.get(url_for('api.replication_hourly', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_hourly', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_hourly', packet_number=1, token=self.token)))

        open(os.path.join(self.path, 'replication-1.tar.bz2'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_hourly', packet_number=1, token=self.token)))

    def test_replication_hourly_signature(self):
        self.assert400(self.client.get(url_for('api.replication_hourly_signature', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_hourly_signature', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_hourly_signature', packet_number=1, token=self.token)))

        open(os.path.join(self.path, 'replication-1.tar.bz2.asc'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_hourly_signature', packet_number=1, token=self.token)))

    def test_replication_daily(self):
        self.assert400(self.client.get(url_for('api.replication_daily', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_daily', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_daily', packet_number=1, token=self.token)))

        open(os.path.join(self.path, DAILY_SUBDIR, 'replication-daily-1.tar.bz2'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_daily', packet_number=1, token=self.token)))

    def test_replication_daily_signature(self):
        self.assert400(self.client.get(url_for('api.replication_daily_signature', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_daily_signature', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_daily_signature', packet_number=1, token=self.token)))

        open(os.path.join(self.path, DAILY_SUBDIR, 'replication-daily-1.tar.bz2.asc'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_daily_signature', packet_number=1, token=self.token)))

    def test_replication_weekly(self):
        self.assert400(self.client.get(url_for('api.replication_weekly', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_weekly', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_weekly', packet_number=1, token=self.token)))

        open(os.path.join(self.path, WEEKLY_SUBDIR, 'replication-weekly-1.tar.bz2'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_weekly', packet_number=1, token=self.token)))

    def test_replication_weekly_signature(self):
        self.assert400(self.client.get(url_for('api.replication_weekly_signature', packet_number=1)))
        self.assert403(self.client.get(url_for('api.replication_weekly_signature', packet_number=1, token='fake')))
        self.assert404(self.client.get(url_for('api.replication_weekly_signature', packet_number=1, token=self.token)))

        open(os.path.join(self.path, WEEKLY_SUBDIR, 'replication-weekly-1.tar.bz2.asc'), 'a').close()
        self.assert200(self.client.get(url_for('api.replication_weekly_signature', packet_number=1, token=self.token)))
