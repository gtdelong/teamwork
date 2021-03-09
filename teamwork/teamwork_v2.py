from datetime import datetime, date, timedelta
import pandas as pd
import networkx as nx
from itertools import combinations  
import numpy as np

class TeamworkStudyRunner:
    """Runs a teamwork study """
    def __init__(self, notes, window_in_days, step_in_days):
#         notes.sort_values('date', inplace=True)
#         self.notes = notes
        self.DELTA = np.timedelta64(window_in_days, 'D')
        self.STEP = np.timedelta64(step_in_days, 'D')
        self._transform_data()
        self.discharge_id_to_index_team_dict = dict()
        self.edge_to_date_dict = dict()
        self.date_to_discharge_dict = dict()
        self.date_discharge_to_careteam_dict = dict()
        self._populate_dicts()
        self.caredate_list = []
        self._populate_caredate_list()
        
#     def _populate_dicts(self):
#         for 
    
#     def _populate_caredate_list(self):
#         for date in self.careteam_date_range:
#             discharge_ids = self.date_to_discharge_dict.get(hash_date(date),None)
#             if discharge_ids == None: continue
# #             print(type(date))
#             caredate = CareDate(self.DELTA,
#                                 date, 
#                                 discharge_ids, 
#                                 self.edge_to_date_dict,
#                                 self.date_to_discharge_dict,
#                                 self.date_discharge_to_careteam_dict)
#             self.caredate_list.append(caredate)
        
#     def _populate_dicts(self):
#         for date in self.date_range:
# #             print(type(date))
#             plus_step = date + self.STEP
#             notes_for_date = self.notes.query('date >= @date & date <= @plus_step')
#             num_rows = len(notes_for_date.index)
#             if num_rows == 0: continue
#             discharge_ids_for_date = notes_for_date.discharge_id.unique()
#             self.date_to_discharge_dict.setdefault(hash_date(date),[]).extend(discharge_ids_for_date)
#             for discharge_id in discharge_ids_for_date:
#                     care_team = notes_for_date.query('discharge_id == @discharge_id').dr.unique()
#                     care_team_edges = [edge for edge in list(combinations(care_team, 2))]
#                     hashed = hash_date_discharge(date,discharge_id)
#                     self.date_discharge_to_careteam_dict[hash_date_discharge(date,discharge_id)] = (care_team,care_team_edges)
#                     for edge in care_team_edges: 
#                         hashed_edge = hash_edge(edge)
#                         self.edge_to_date_dict.setdefault(hashed_edge,[]).append(date)
                        
    def __iter__(self):
        for care_date in self.caredate_list:
            yield care_date
            
# class CareDate:
#     def __init__(self, delta, date, discharge_ids, edge_to_date_dict,date_to_discharge_dict,date_discharge_to_careteam_dict):
#         self.DELTA = delta
#         self.date = date
#         self.discharge_ids = discharge_ids
#         self.edge_to_date_dict = edge_to_date_dict
#         self.date_to_discharge_dict = date_to_discharge_dict
#         self.date_discharge_to_careteam_dict = date_discharge_to_careteam_dict
#         self.careteam_list = []
#         self._populate_careteam_list()
        
#     def _populate_careteam_list(self):
#         for discharge_id in self.discharge_ids:
#                 care_team, care_team_edges = self.date_discharge_to_careteam_dict[hash_date_discharge(self.date,discharge_id)]
#                 graph = nx.Graph()
#                 for edge in care_team_edges:
#                     hashed_edge = hash_edge(edge)
#                     weight = len([d for d in self.edge_to_date_dict[hashed_edge] if d < self.date and d >= self.date-self.DELTA])
#                     if weight > 0: graph.add_edge(*edge, weight=weight)                
#                 self.careteam_list.append(CareTeam(discharge_id,care_team,care_team_edges,graph))
                
#     def __iter__(self):
#         for care_team in self.careteam_list:
#             yield care_team
          
class CareTeam:
    def __init__(self,discharge_id,care_team,care_team_edges,graph):
        self.discharge_id = discharge_id
        self.care_team = care_team
        self.care_team_edges = care_team_edges
        self.G = graph

def hash_edge(edge):
    edge = sorted(edge)
    return f"{edge[0]}{edge[1]}"

def hash_date_discharge(date, discharge_id):
    hashed = f"{hash_date(date)}{discharge_id}"
    return hashed

def hash_date(date):
    return str(date)[:10]
#     return np.datetime_as_string(d, unit='D')

'''
1. list of notes (notes table)
- match in admission datetime indexing on visit id from discharge table
2. in notes table, create additional column that is difference between time of note writing and time of admit
3. in notes table, create 3rd column, if the diff is less then 48 hrs then 1, else 0
a)- at this point, we could subset from notes table where column == 1 into a new table called (index table), do self join on visit id, which would give edges for all of index teams (define care team for each patient)
- subset where column == 0 into new table (values table), do self join on visit id and date of note writing, which gives all potential edges for edge values of index teams
- for each visit id on index table, pull edges into list called (iterator list), subset from values table where visit id is in iterator list, group by dyad with sum as aggregating function, which will create new object called (iterator care team object), that object can now go into the class(es) already defined
'''