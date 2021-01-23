import networkx as nx

def get_careteam_data(care_team):
    coefficients = nx.clustering(care_team.G)# Clustering coefficient of all nodes (in a dictionary)
    # Average clustering coefficient with divide-by-zero check
    avg_clust = sum(coefficients.values()) / len(coefficients) if len(coefficients) > 0 else 0  
    experience = care_team.G.size(weight='weight') #Experience as sum of weights
    team_edge_size = care_team.G.number_of_edges()
    cumulative_experience = experience - team_edge_size
    avg_cumulative_experience = cumulative_experience / len(care_team.care_team)#Average Cumulative Experience

    return {
        'discharge_id': care_team.discharge_id,
        'avg_clust': avg_clust,
        'cumulative_experience': cumulative_experience,
        'avg_cumulative_experience': avg_cumulative_experience,
        "team_edge_size": team_edge_size,
        "team_size": care_team.G.number_of_nodes()
    }
