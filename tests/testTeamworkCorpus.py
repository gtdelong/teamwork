import unittest

# These two lines allow us to import the package from teamwork
# src_dir = os.path.join(os.getcwd(), "teamwork")
# sys.path.append(src_dir)
# from teamwork import TeamworkCorpus
# sys.path.append(os.path.join(os.getcwd(), ".."))
from .context import teamwork as tw
from .context import utils as u
import pandas as pd
from test_constants import data


class TestTeamworkCorpus(unittest.TestCase):
    #     setUp method is overridden from the parent class TestCase
    #     def setUp(self):

    def test_team_size(self):
        # Arrange
        test_df = pd.DataFrame.from_dict(data, orient="index")
        teamwork_columns = {
            tw.VISIT_ID: "id",
            tw.ADMISSION_DATE: "arrive_date",
            tw.NOTE_AUTHOR: "dr",
            tw.NOTE_DATE: "date",
        }
        
        # Act
        corpus = tw.TeamworkCorpus(notes_table, **teamwork_columns)
        actual_team_size = corpus.

        # Assert
        expected_edges = 3
        self.assertEqual(expected_edges, actual_edges)


# Executing the tests in the above test case class
if __name__ == "__main__":
    unittest.main()
