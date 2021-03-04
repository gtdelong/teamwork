import networkx as nx

columns = ['discharge_id',
        'avg_clust',
        'cumulative_experience',
        'avg_cumulative_experience',
        'team_edge_size',
        'team_size']

def get_careteam_data(care_team):
    data = {}
    data['discharge_id'] = care_team.discharge_id
    
    ''' Clustering coefficient of all nodes (in a dictionary) '''
    clustering_coefficient = nx.clustering(care_team.G)
    
    ''' Average clustering coefficient with divide-by-zero check '''
    data['avg_clust'] = sum(clustering_coefficient.values()) / len(clustering_coefficient) if len(clustering_coefficient) > 0 else 0 
    
    data['team_size'] = care_team.G.number_of_nodes()
    data['team_edge_size'] = care_team.G.number_of_edges()
    
    experience = care_team.G.size(weight='weight') #Experience as sum of weights
    data['cumulative_experience'] = experience - data['team_edge_size']
    data['avg_cumulative_experience'] = data['cumulative_experience'] / len(care_team.care_team)#Average Cumulative Experience
    
    return data

notes_with_disposition_file = '../data/notes_w_disposition.csv'
discharges_with_disposition_file = '../data/discharges_w_disposition.csv'

notes_test_file = '../data/notes_test.csv'
notes_with_disposition_large_file = '../data/notes_w_disposition_large.csv'