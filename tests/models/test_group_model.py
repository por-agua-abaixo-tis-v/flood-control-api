import unittest
from mock import patch

from flood.models import group as group_model


class TestStringMethods(unittest.TestCase):

    @patch("flood.models._session")
    def test_group_create(self, _session):
        group = group_model.create(
            {
                "name": "Bernardo Vasconcelos",
                "latitude": -19.8762564,
                "longitude": -43.9311202,
                "range": 2,
                "active": True
            }
        )
        self.assertEqual(_session().add.call_count, 1)
        self.assertEqual(_session().flush.call_count, 1)

        self.assertEqual(
            group.to_dict(),
            {
                'active': True,
                'created_at': None,
                'id': None,
                'latitude': -19.8762564,
                'longitude': -43.9311202,
                'name': 'Bernardo Vasconcelos',
                'range': 2,
                'severity': 'low'
            }
        )

    @patch("flood.models.group.to_dict")
    @patch("flood.models._session")
    def test_group_list(self, _session, to_dict):
        groups = group_model.list(True)
        self.assertEqual(_session().query().filter.call_count, 1)


        _session().query().all.return_value = None
        groups = group_model.list(None)
        self.assertEqual(_session().query().all.call_count, 1)
        self.assertEqual(groups, [])

        _session().query().all.return_value = ['row']
        to_dict.return_value = {
            'active': True,
            'id': None,
            'latitude': -19.8762564,
            'longitude': -43.9311202,
            'name': 'Bernardo Vasconcelos',
            'range': 2,
            'severity': 'low',
            'created_at': '2020-06-07T01:13:33'
        }
        groups = group_model.list(None)
        self.assertEqual(len(groups), 1)
        self.assertEqual(
            groups[0].to_dict(),
            {
                'active': True,
                'created_at': '2020-06-07T01:13:33',
                'id': None,
                'latitude': -19.8762564,
                'longitude': -43.9311202,
                'name': 'Bernardo Vasconcelos',
                'range': 2,
                'severity': 'low'
            }
        )

    @patch("flood.models.group.to_dict")
    @patch("flood.models._session")
    def test_group_get(self, _session, to_dict):
        _session().query().get.return_value = None
        self.assertEqual(group_model.get('id'), None)

        _session().query().get.return_value = {}
        to_dict.return_value = {
            'active': True,
            'id': None,
            'latitude': -19.8762564,
            'longitude': -43.9311202,
            'name': 'Bernardo Vasconcelos',
            'range': 2,
            'severity': 'low',
            'created_at': '2020-06-07T01:13:33'
        }

        group = group_model.get('id')
        self.assertEqual(
            group.to_dict(),
            {
                'active': True,
                'created_at': '2020-06-07T01:13:33',
                'id': None,
                'latitude': -19.8762564,
                'longitude': -43.9311202,
                'name': 'Bernardo Vasconcelos',
                'range': 2,
                'severity': 'low'
            }
        )

    @patch("flood.models.group.to_dict")
    @patch("flood.models._session")
    def test_group_delete(self, _session, to_dict):
        _session().query().get.return_value = {}
        to_dict.return_value = {
            'active': True,
            'id': None,
            'latitude': -19.8762564,
            'longitude': -43.9311202,
            'name': 'Bernardo Vasconcelos',
            'range': 2,
            'severity': 'low',
            'created_at': '2020-06-07T01:13:33'
        }

        group = group_model.delete('id')
        self.assertEqual(
            group.to_dict(),
            {
                'active': True,
                'created_at': '2020-06-07T01:13:33',
                'id': None,
                'latitude': -19.8762564,
                'longitude': -43.9311202,
                'name': 'Bernardo Vasconcelos',
                'range': 2,
                'severity': 'low'
            }
        )

        self.assertEqual(_session().query().get.call_count, 1)
        self.assertEqual(_session().delete.call_count, 1)


    @patch("flood.models.group.to_dict")
    @patch("flood.models._session")
    def test_group_delete(self, _session, to_dict):
        _session().query().get.return_value = group_model.Group(
            name='jonas',
            id='jonas',
            latitude=1,
            longitude=1,
            range=1,
            active='jonas',
            severity='jonas'
        )

        to_dict.return_value = {
            'active': True,
            'id': None,
            'latitude': -19.8762564,
            'longitude': -43.9311202,
            'name': 'Bernardo Vasconcelos',
            'range': 2,
            'severity': 'low',
            'created_at': '2020-06-07T01:13:33'
        }
        group_model.update(
            'id',
            {
                'active': True,
                'id': None,
                'latitude': -19.8762564,
                'longitude': -43.9311202,
                'name': 'Bernardo Vasconcelos',
                'range': 2,
                'severity': 'low',
                'created_at': '2020-06-07T01:13:33'
            }
        )

        to_dict.assert_called_once()


        _session().query().get.return_value = None
        self.assertEqual(group_model.update('id', {}), None)

