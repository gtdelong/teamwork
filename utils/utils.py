import networkx as nx
from itertools import combinations 

columns = ['visit_id',
        'avg_clust',
           'sum_clust',
        'cumulative_experience',
           'potential_edges',
        'avg_cumulative_experience',
        'team_edge_size',
        'team_size']

def get_output_for_row(g, dx_g, visit_id, team):
    data = {}
    data['visit_id'] = visit_id
    
    ''' Clustering coefficient of all nodes (in a dictionary) '''
    #need for both
    clustering_coefficient = nx.clustering(g, weight='weight')
    dx_clustering_coefficient = nx.clustering(dx_g, weight='weight')
    
    ''' Average clustering coefficient with divide-by-zero check '''
    #need for both
    clust_sum = sum(clustering_coefficient.values())
    clust_len = len(clustering_coefficient)
    dx_clust_sum = sum(dx_clustering_coefficient.values())
    dx_clust_len = len(dx_clustering_coefficient)
        
    data['avg_clust'] = clust_sum / clust_len if clust_len > 0 else 0
    data['avg_dx_clust'] = dx_clust_sum / dx_clust_len if dx_clust_len > 0 else 0
    
    data['sum_clust'] = clust_sum
    data['sum_dx_clust'] = dx_clust_sum
    
    data['team_size'] = len(team)
    potential_edges = len(list(combinations(team,2)))
    data['potential_edges'] = potential_edges
    data['team_edge_size'] = g.number_of_edges()
    
    experience = g.size(weight='weight') #Experience as sum of weights
    dx_experience = dx_g.size(weight='weight') 
    
    data['cumulative_experience'] = experience - data['team_edge_size']
    data['cumulative_dx_experience'] = dx_experience - data['team_edge_size']
    
    data['avg_cumulative_experience'] = data['cumulative_experience'] / potential_edges if data['team_size'] > 0 else 0
    data['avg_cumulative_dx_experience'] = data['cumulative_dx_experience'] / potential_edges if data['team_size'] > 0 else 0
    
    return data

discharges_datetime_file = '../data/discharges_w_datetime.csv'
notes_datetime_file = '../data/notes_w_datetime.csv'

discharges_test_file = '../data/discharges_test.csv'
notes_test_file = '../data/notes_test.csv'

test_data_dict = {   
    0: {   'age': 75,
           'arrive_date': '2019-01-01 00:00:00',
           'date': '2019-01-01 19:15:00',
           'discharge_date': '2019-01-01',
           'disposition': 1,
           'dr': 'Brad Palmer',
           'id': 0,
           'patient': 'patient1'},
    1: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 10:19:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Albert Romero',
           'id': 1,
           'patient': 'patient2'},
    2: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 17:09:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Margie Meyer',
           'id': 1,
           'patient': 'patient2'},
    3: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 16:48:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Evan Frazier',
           'id': 1,
           'patient': 'patient2'},
    4: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 13:41:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Myrtle George',
           'id': 1,
           'patient': 'patient2'},
    5: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 12:52:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Victoria Washington',
           'id': 1,
           'patient': 'patient2'},
    6: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-25 09:49:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Brad Palmer',
           'id': 1,
           'patient': 'patient2'},
    7: {   'age': 68,
           'arrive_date': '2019-01-24 00:00:00',
           'date': '2019-01-24 20:52:00',
           'discharge_date': '2019-01-24',
           'disposition': 0,
           'dr': 'Neil Mitchell',
           'id': 1,
           'patient': 'patient2'},
    8: {   'age': 71,
           'arrive_date': '2019-02-14 00:00:00',
           'date': '2019-02-14 20:58:00',
           'discharge_date': '2019-02-14',
           'disposition': 0,
           'dr': 'Albert Romero',
           'id': 2,
           'patient': 'patient3'},
    9: {   'age': 71,
           'arrive_date': '2019-02-14 00:00:00',
           'date': '2019-02-14 15:54:00',
           'discharge_date': '2019-02-14',
           'disposition': 0,
           'dr': 'Margie Meyer',
           'id': 2,
           'patient': 'patient3'},
    10: {   'age': 71,
            'arrive_date': '2019-02-14 00:00:00',
            'date': '2019-02-14 20:07:00',
            'discharge_date': '2019-02-14',
            'disposition': 0,
            'dr': 'Evan Frazier',
            'id': 2,
            'patient': 'patient3'},
    11: {   'age': 71,
            'arrive_date': '2019-02-14 00:00:00',
            'date': '2019-02-14 18:49:00',
            'discharge_date': '2019-02-14',
            'disposition': 0,
            'dr': 'Myrtle George',
            'id': 2,
            'patient': 'patient3'},
    12: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-16 01:29:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Albert Romero',
            'id': 6,
            'patient': 'patient4'},
    13: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-15 20:19:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Margie Meyer',
            'id': 6,
            'patient': 'patient4'},
    14: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-16 04:43:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Evan Frazier',
            'id': 6,
            'patient': 'patient4'},
    15: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-18 21:23:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Myrtle George',
            'id': 6,
            'patient': 'patient4'},
    16: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-16 07:00:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Victoria Washington',
            'id': 6,
            'patient': 'patient4'},
    17: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-17 20:27:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Brad Palmer',
            'id': 6,
            'patient': 'patient4'},
    18: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-15 21:25:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Neil Mitchell',
            'id': 6,
            'patient': 'patient4'},
    19: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-16 01:25:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Henry Philofsky',
            'id': 6,
            'patient': 'patient4'},
    20: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-16 03:25:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Grant DeLong',
            'id': 6,
            'patient': 'patient4'},
    21: {   'age': 66,
            'arrive_date': '2019-04-15 19:15:00',
            'date': '2019-04-17 03:25:00',
            'discharge_date': '2019-04-15',
            'disposition': 0,
            'dr': 'Grant DeLong',
            'id': 6,
            'patient': 'patient4'},
    22: {   'age': 69,
            'arrive_date': '2019-08-15 00:00:00',
            'date': '2019-08-15 17:07:00',
            'discharge_date': '2019-08-15',
            'disposition': 1,
            'dr': 'Neil Mitchell',
            'id': 7,
            'patient': 'patient5'}
}