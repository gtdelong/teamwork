from datetime import datetime, date, timedelta
import pandas as pd
import networkx as nx
from itertools import combinations  
import numpy as np

class TeamworkStudyRunner:
    def __init__(self, notes, window_in_days, step_in_days):
        notes.sort_values('date', inplace=True)
        self.notes = notes
        self.DELTA = np.timedelta64(window_in_days, 'D')
        self.STEP = np.timedelta64(step_in_days, 'D')
        first_date = notes['date'].iloc[0] 
        last_date = notes['date'].iloc[-1]
        self.date_range = np.arange(first_date, last_date - self.DELTA, self.STEP)
        
    def __iter__(self):
        for start_date in self.date_range:
            end_date = start_date + self.DELTA 
            date_of_care = end_date + self.STEP 
            notes_in_window = self.notes.query('date >= @start_date & date <= @end_date')
            notes_for_care_date = self.notes.query('date > @end_date & date <= @date_of_care')
            num_rows = len(notes_for_care_date.index)
            if num_rows == 0: continue
            yield CareDate(notes_in_window, notes_for_care_date)
            
class CareDate:
    def __init__(self, notes_in_window, notes_for_care_date):
        self.notes_in_window = notes_in_window
        self.notes_for_care_date = notes_for_care_date
        self.care_team_dict = {}
        self.__populate_care_team_dict()
    
    def __populate_care_team_dict(self):
        discharge_ids_for_date = self.notes_for_care_date.discharge_id.unique()
        for discharge_id in discharge_ids_for_date:
            drs_for_discharge_id = self.notes_for_care_date.query('discharge_id == @discharge_id').dr.unique()
            self.care_team_dict[discharge_id] = drs_for_discharge_id
        
    def __iter__(self):
        for discharge_id, care_team in self.care_team_dict.items():
            yield CareTeam(self.notes_in_window, discharge_id, care_team)
            
class CareTeam:
    def __init__(self, notes_in_window, discharge_id, care_team):
        self.notes_in_window = notes_in_window  
        self.discharge_id = discharge_id
        self.care_team = care_team
        self.care_team_edges = [sorted(edge) for edge in list(combinations(care_team, 2))]
        self.G = nx.Graph()
        self.unique_dates = notes_in_window.date.unique()
        self.__create_graph()
    
    def __create_graph(self):
        for note_date in self.unique_dates:
            notes_for_date = self.notes_in_window.query('date == @note_date')
            discharge_ids_for_date = notes_for_date.discharge_id.unique()
            for discharge_id in discharge_ids_for_date:
                drs_for_discharge_id = notes_for_date.query('discharge_id == @discharge_id').dr.unique()
                care_team_edges_for_discharge_id = [edge for edge in list(combinations(drs_for_discharge_id, 2)) 
                                                    if sorted(edge) in self.care_team_edges]
                for edge in care_team_edges_for_discharge_id: 
                    self.__add_edge_to_G(edge)
        
    def __add_edge_to_G(self, edge):
        data = self.G.get_edge_data(*edge, default=None)
        weight = 1 if data is None else data['weight'] + 1
        self.G.add_edge(*edge, weight=weight)