# Teamwork

Teamwork is a Python library designed to aid in the study of medical care team collaboration. 

Specifically, the library takes electronic health record encounter-level data (both discharges and notes) as inputs and does the following: 
1) Identifies the members of medical care teams for unique patient visits based on medical note meta-data
2) Builds a network graph for each care team based on their common patients in the previous 90 days

The resulting care team network graphs can be used to compute the cumulative collaborative experience of care teams and other metrics.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install teamwork.

```bash
pip install teamwork
```

## Usage

```python
import pandas as pd
from teamwork import teamwork as tw

# read medical notes (3 columns) into pandas DataFrame
test_df = pd.read_csv('../data/sample_notes.csv')
# enforce date columns
test_df['date'] = pd.to_datetime(test_df['date'])
test_df['arrive_date'] = pd.to_datetime(test_df['arrive_date'])
# set a 90 day window to find collaboration among care teams
WINDOW = 90
# identify care teams within 2 day increments 
STEP = 2

corpus = tw.TeamworkCorpus(test_df)

# now you can do something with the care team network graph
for visit_id, item in corpus.team_experience_dict.items():
    print(item['graph'])
```

## Contributors

| Contributor|Role |
|-|-|
| [Henry Philofsky](https://github.com/hp2335) | Concept, SME |
| [Grant DeLong](https://github.com/gtdelong) | Developer, Architect |

## License
[MIT](https://github.com/gtdelong/teamwork/blob/main/LICENSE.txt)
