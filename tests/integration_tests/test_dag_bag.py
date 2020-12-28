from unittest import TestCase

from airflow.models import DagBag

class TestDagBag(TestCase):
    def setUp(self):
        self.dagbag = DagBag()

    def test_import_dags(self):
        self.assertFalse(
            len(self.dagbag.import_errors),
            'Failed to import DAGs. Details: {}'.format(
                self.dagbag.import_errors
            )
        )
