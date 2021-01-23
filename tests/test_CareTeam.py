import unittest
import os
import sys
# These two lines allow us to import the package from src
src_dir = os.path.join(os.getcwd(), 'src')
sys.path.append(src_dir)
from experience import CareTeam
import pandas as pd

class TestCareTeam(unittest.TestCase):
#     setUp method is overridden from the parent class TestCase
#     def setUp(self):
        
    def test_edges(self):
        # Arrange
        discharge_id = 1
        date = '2019-1-24'
        test_team = ['Albert Romero','Margie Meyer','Evan Frazier']
        test_notes = [[discharge_id, name, date] for name in test_team]
        columns = ['discharge_id', 'dr', 'date']
        test_df = pd.DataFrame(test_notes, columns=columns)
        
        # Act
        care_team = CareTeam(test_df, discharge_id, test_team)
        actual_edges = care_team.G.number_of_edges()
        
        # Assert
        expected_edges = 3
        self.assertEqual(expected_edges,actual_edges)
        
# Executing the tests in the above test case class
if __name__ == "__main__":
  unittest.main()