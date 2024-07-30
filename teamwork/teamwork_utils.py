import os
import sys
import time
from datetime import datetime
from tqdm import tqdm
import numpy as np
import pandas as pd
import re
import functools
import gender_guesser.detector as gender
import pickle
import networkx as nx
from itertools import combinations

def detect_gender(name: str):
    match = re.search(r"(?<=,\s)\w+", name)
    if match is None:
        match = re.search(r"\w+", name)
    first_name = match.group()
    result = gender_detector.get_gender(first_name)
    return get_gender_label(result)

def get_gender_label(result: str):
    if re.match(r".*female.*", result):
        return "F"
    elif re.match(r".*male.*", result):
        return "M"
    else: return "U"
    
def get_gender_for_row(row):
    sex = row['sex']
    if sex is not None and re.match("[MF]", sex):
        return sex
    else: return detect_gender(row['prov_name'])
    
def get_prov_demo_dict(prov_demo_filename):   
    prov_demo_df = pd.read_csv(prov_demo_filename)
    prov_demo_df = prov_demo_df.dropna(subset=['prov_name', 'author_prov_id'])
    prov_demo_df['sex'] = prov_demo_df['sex'].fillna("U")
    prov_demo_df['clinician_title'] = prov_demo_df['clinician_title'].fillna("UNKNOWN")
    prov_demo_df['guessed_sex'] = prov_demo_df.apply(get_gender_for_row, axis="columns")
    
    prov_demo_df = prov_demo_df.set_index('author_prov_id')
    prov_demo_dict = prov_demo_df.to_dict('index')
    return prov_demo_dict

def get_dept_dict(dept_filename):
    dept_df = pd.read_csv(dept_filename)
    dept_df = dept_df.set_index('enc_csn_id')
    dept_dict = dept_df.to_dict('index')
    return dept_dict

def get_output_for_row(g, dx_g, visit_id, team, dept_dict, prov_demo_dict):
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
    data['experience'] = experience
    dx_experience = dx_g.size(weight='weight') 
    data['dx_experience'] = dx_experience
    
    data['cumulative_experience'] = experience - data['team_edge_size']
#     We are not adjusting to avoid negative number
    data['cumulative_dx_experience'] = dx_experience #- data['team_edge_size']
    
    data['avg_cumulative_experience'] = data['cumulative_experience'] / potential_edges if data['team_size'] > 0 else 0
    data['avg_cumulative_dx_experience'] = data['cumulative_dx_experience'] / potential_edges if data['team_size'] > 0 else 0
    
    genders = [prov_demo_dict[prov]["sex"] for prov in team]
    guessed_genders = [prov_demo_dict[prov]["guessed_sex"] for prov in team]
    
    count_genders = lambda acc, s: acc if s == "U" else acc + 1
    count_females = lambda acc, s: acc if s != "F" else acc + 1

    gen_count = functools.reduce(count_genders, genders, 0)
    guessed_gen_count = functools.reduce(count_genders, guessed_genders, 0)
    fem_count = functools.reduce(count_females, genders, 0)
    guessed_fem_count = functools.reduce(count_females, guessed_genders, 0)
    guessed_gender_ratio = guessed_fem_count / guessed_gen_count if guessed_gen_count > 0 else 0
    gender_ratio = fem_count / gen_count if gen_count > 0 else 0
    
    data['gen_count'] = gen_count
    data['guessed_gen_count'] = guessed_gen_count
    data['fem_count'] = fem_count
    data['guessed_fem_count'] = guessed_fem_count
    data['guessed_gender_ratio'] = guessed_gender_ratio
    data['gender_ratio'] = gender_ratio
    
    data = {**data, **dept_dict[int(visit_id)]}
    
    return data