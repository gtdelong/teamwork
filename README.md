# Teamwork

Teamwork is a Python library designed to aid in the study of medical care team collaboration. 

Specifically, the library takes electronic health record encounter-level data (both discharges and notes) as inputs and does the following: 
1) Identifies the members of medical care teams for unique patient visits based on medical note meta-data
2) Builds a network graph for each care team based on their common patients in the previous 90 days. The nodes of the graph are note authors, and the edge weights are the number of days where the authors have both written a note on common patient

The resulting care team network graphs can be used to compute the cumulative collaborative experience of care teams and other metrics.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install teamwork.

```bash
pip install teamwork
```

## Usage

```python
from teamwork.teamwork import TeamworkStudyRunner
import pandas as pd

# read medical notes (3 columns) into pandas DataFrame
notes_df = pd.read_csv("notes_file.csv", parse_dates=[2])
# enforce column names
notes_df.columns = ['discharge_id', 'dr', 'date']
# set a 90 day window to find collaboration among care teams
WINDOW = 90
# identify care teams within 2 day increments 
STEP = 2

# the study runner is a generator
get_care_dates = TeamworkStudyRunner(notes_df, WINDOW, STEP)

# gather care teams into a list
care_team_list = [care_team for care_date in get_care_dates for care_team in care_date]

# now you can do something with the care team network graph
for care_team in care_team_list:
    analyze_graph(care_team.G)
```

A sample study can be found [here](https://github.com/gtdelong/teamwork/blob/main/notebooks/teamwork_study.ipynb)

## Contributors

| Contributor|Role |
|-|-|
| [Henry Philofsky](https://github.com/hp2335) | Concept, SME |
| [Grant DeLong](https://github.com/gtdelong) | Developer, Architect |

## License
[MIT](https://github.com/gtdelong/teamwork/blob/main/LICENSE.txt)
