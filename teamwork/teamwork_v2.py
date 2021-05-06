import pandas as pd
import networkx as nx
# from itertools import combinations  
import numpy as np

class TeamworkCorpus():
    def __init__(self, notes_df, teamwork_window=90, team_window=2, **columns):
        self.columns = { **default_columns, **columns }
        self.notes_df = notes_df[self.columns.values()]
        self.TEAMWORK_DELTA = np.timedelta64(teamwork_window, 'D')
        self.TEAM_DELTA = np.timedelta64(team_window, 'D')
        
        _prepare_note_data(self.notes_df, self.columns, self.TEAM_DELTA)
        self.FIRST_DATE = self.notes_df[self.columns[ADMISSION_DATE]].iloc[0]
        self.edge_df = _get_edge_data(self.notes_df, self.columns, teamwork_window, self.FIRST_DATE)
        self.team_df = _get_team_data(self.notes_df, self.columns, teamwork_window, self.FIRST_DATE)
        self.__build_dicts()
        
    def __build_dicts(self):
        self.visit_id_to_edges_dict = dict()  
        self.edge_to_date_dict = dict()
        self.visit_id_to_team_dict = dict()
        self.edge_df.apply(_add_edge_to_dict, axis='columns', args=(self.edge_to_date_dict,))
        self.team_df.apply(_add_team_to_dicts, axis='columns', args=(self.visit_id_to_edges_dict, self.visit_id_to_team_dict))
        self.team_experience_dict = {k: self.__get_team_experience(k, v) for (k,v) in self.visit_id_to_edges_dict.items()}
        
    def __get_edge_list_item(self, edge_item):
        edge = edge_item[0]
        if edge not in self.edge_to_date_dict: return None
        (dr_x,dr_y) = edge_item[1]
        arrive_date = edge_item[2]
        weight = len([note_day for note_day in self.edge_to_date_dict[edge] 
                      if note_day < arrive_date and note_day >= arrive_date - TEAMWORK_DELTA])
        if(weight < 1): return None
        return {'source':dr_x,'target':dr_y,'weight':weight}

    def __get_team_experience(self, visit_id, edge_items):
        edge_list = [i := self.__get_edge_list_item(edge_item) for edge_item in edge_items if i is not None]
        edge_list_df = pd.DataFrame(edge_list, columns = ['source', 'target', 'weight'])
        g = nx.from_pandas_edgelist(edge_list_df, source='source', target='target',edge_attr='weight')
        team = self.visit_id_to_team_dict[visit_id]
        return {'team': team, 'graph': g}
        
def _prepare_note_data(notes_df, columns, team_delta):
    visit_id, admit_date, note_date, note_author = [*columns.values()]  
    notes_df[NORM_ADMISSION_DATE] = notes_df[admit_date].astype('datetime64[D]')
    notes_df[NORM_NOTE_DATE] = notes_df[note_date].astype('datetime64[D]')
    notes_df.drop_duplicates([NORM_NOTE_DATE, note_author, visit_id], keep="first", inplace=True)
    notes_df.sort_values(admit_date, inplace=True)   
    # add indicator column for whether the note author is in the index team
    notes_df[IS_IN_TEAM] = notes_df[note_date] - notes_df[admit_date] <= team_delta
    
def _get_edge_data(notes_df, columns, teamwork_delta, first_date):
    visit_id, *_, note_author = [*columns.values()]
    # do self join on discharge id and normalized note date to get table of edges
    edges_df = notes_df.merge(notes_df[[note_author,visit_id,IS_IN_TEAM,NORM_NOTE_DATE]], how='inner', on=[visit_id,NORM_NOTE_DATE])
    # remove edges with the same name twice or with authors in reverse order
    _add_team_columns(edges_df, columns, teamwork_delta, first_date)
    return edges_df
    
def _get_team_data(notes_df, columns, teamwork_delta, first_date):
    visit_id, *_, note_author = [*columns.values()]
    # do self join on discharge id get table of team edges
    team_df = notes_table.merge(notes_table[[note_author, visit_id, IS_IN_TEAM, NORM_NOTE_DATE]], how='inner', on=VISIT_ID)
    # remove edges with the same name twice or with authors in reverse order
    _add_team_columns(team_df, columns, teamwork_delta, first_date)
    # keep only edge in team and after initial teamwork window
    team_df = team_df[team_df[IS_IN_TEAM] & team_df[IS_AFTER_DELTA]]
    return team_df
    
def _add_team_columns(df, columns, teamwork_delta, first_date):
    print(f'teamwork_delta: {teamwork_delta}')
    print(f'teamwork_delta: {first_date}')
    _, admit_date, _, note_author = [*columns.values()]
    author_x = f'{note_author}_x'
    author_y = f'{note_author}_y'
    
    # remove edges with the same name twice or with authors in reverse order
    df = df[df[author_x] < df[author_y]]
    df[EDGE] = df[author_x] + df[author_y]

    # might be able to remove this line, need to discuss
    df[IS_IN_TEAM] = df[IS_IN_TEAM_X] & df[IS_IN_TEAM_Y]
    # add column indicating whether there are 90 days prior to arrive date. if not, don't count as index team
    df[IS_AFTER_DELTA] = df[admit_date] > (first_date + teamwork_delta)
    
def _add_team_to_dicts(edge_record, visit_id_to_edges_dict, visit_id_to_team_dict, columns):
    visit_id, *_, note_author = [*columns.values()]
    author_x = f'{note_author}_x'
    author_y = f'{note_author}_y'
    edge_tup = (edge_record[author_x], edge_record[author_y])
    # store edge, individual note author names, and arrive date in list item
    edge_list_item = (edge_record[EDGE], edge_tup, edge_record[NORM_ADMISSION_DATE])
    visit_id_to_edges_dict.setdefault(edge_record[visit_id],[]).append(edge_list_item)
    visit_id_to_team_dict.setdefault(edge_record[visit_id],set()).update(edge_tup)

def _add_edge_to_dict(edge_record, edge_to_date_dict):
    edge_to_date_dict.setdefault(edge_record[EDGE],[]).append(edge_record[NORM_NOTE_DATE])
        
def from_csv(filename, teamwork_delta=90, team_delta=2,**columns):
    columns = { **default_columns, **columns }
    notes_df = pd.read_csv(filename, parse_dates=[ADMISSION_DATE,NOTE_DATE], usecols=columns.values())
    return TeamworkCorpus(notes_df, teamwork_delta, team_delta, columns)

'''Static Column Names'''
VISIT_ID = 'visit_id'
ADMISSION_DATE = 'admission_date'
NOTE_DATE = 'note_date'
NOTE_AUTHOR = 'note_author'
NORM_ADMISSION_DATE = 'norm_admission_date'
NORM_NOTE_DATE = 'norm_note_date'
IS_IN_TEAM = 'is_in_team'
IS_IN_TEAM_X = f'{IS_IN_TEAM}_x'
IS_IN_TEAM_Y = f'{IS_IN_TEAM}_y'
EDGE = 'edge'
IS_AFTER_DELTA = 'is_after_delta'

default_columns = {
    VISIT_ID:'id',
    ADMISSION_DATE:'arrive_date',
    NOTE_DATE:'date',
    NOTE_AUTHOR:'dr'
}