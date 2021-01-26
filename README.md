# teamwork

teamwork is a Python library designed to aid in the study of medical care team collaboration. 

Specifically, the library takes EHR data as input and does the following: 
1) identifies the members of medical care teams per patient visit
2) builds a network graph for each care team based on their common patients in the previous 90 days

The resulting care team network graphs can be used to compute the cumulative collaborative experience of care teams and other metrics.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install teamwork.

```bash
pip install -i https://test.pypi.org/simple/ teamwork==0.1.0
```

## Usage

```python
import teamwork
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
get_care_dates = teamwork.TeamworkStudyRunner(notes_df, WINDOW, STEP)

# gather care teams into a list
care_team_list = [care_team for care_date in get_care_dates for care_team in care_date]

# do something with the care team network graph
for care_team in care_team_list:
    do_something(care_team.G)
```

A sample study can be found [here](notebooks/teamwork_study.ipynb)

## Contributors

| Contributor|Role |
|-|-|
| [Henry Philofsky](https://github.com/hp2335) | Concept, Development |
| [Grant DeLong](https://github.com/gtdelong) | Development |

## License
[MIT](LICENSE.txt)
