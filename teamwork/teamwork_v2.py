from datetime import datetime, date, timedelta
import pandas as pd
import networkx as nx
from itertools import combinations  
import numpy as np

class TeamworkCorpus():
    def __init__(self, notes_df, teamwork_delta=90, team_delta=2, **columns):
        columns = { **default_columns, **columns }
        self._create_edge_table()
        self._build_dicts(notes_df,)

        
def from_csv(filename, teamwork_delta=90, team_delta=2,**columns):
    columns = { **default_columns, **columns }
    notes_df = pd.read_csv(filename, parse_dates=[ADMISSION_DATE,NOTE_DATE])
    return TeamworkCorpus(notes_df, teamwork_delta, team_delta, columns)

DISCHARGE_ID = 'discharge_id'
ADMISSION_DATE = 'admission_date'
NOTE_DATE = 'note_date'
NOTE_AUTHOR = 'note_author'

default_columns = {
    DISCHARGE_ID:'id',
    ADMISSION_DATE:'arrive_date',
    NOTE_DATE:'date',
    NOTE_AUTHOR:'dr'
}