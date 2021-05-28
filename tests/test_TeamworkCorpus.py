import unittest
from .context import teamwork, utils
from teamwork import teamwork as tw
from utils import utils as u
import pandas as pd
from .constants import data, test_visit_id


class TestTeamworkCorpus(unittest.TestCase):
    #     setUp method is overridden from the parent class TestCase
    #     def setUp(self):

    def test_team_size(self):
        # Arrange
        test_df = pd.DataFrame.from_dict(data, orient="index").astype(
            {"date": "datetime64", "arrive_date": "datetime64"}
        )

        # Act
        corpus = tw.TeamworkCorpus(test_df)
        actual_teamsize = len(corpus.visit_id_to_team_dict[test_visit_id])

        # Assert
        expected_teamsize = 7
        self.assertEqual(expected_teamsize, actual_teamsize)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
