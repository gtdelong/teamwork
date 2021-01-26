# teamwork

teamwork is a Python library for identifying the members of medical care teams using EHR metadata and then calculating the cumulative collaborative experience of providers working together for each care team based on their common patients in a previous time window.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install teamwork.

```bash
pip install teamwork
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



## License
[MIT](https://choosealicense.com/licenses/mit/)
