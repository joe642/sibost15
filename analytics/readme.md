Directory structure:

```
code/                      -- this is a place from where we can import our reusable python code e.g. into notebooks
|- datasets.py             -- contains a simplified API to load data
|- your_module.py          -- put more useful stuff here

data/                      -- key principle -- data is immutable. don't change data manually to keep things 100% reproducible. also it's not committed to git. don't change things here after adding them.
|- raw/                    -- source datasets, as-is (also, if really unavoidable, any hand-crafted datasets, but then with docs please)
|- interim/                -- machine-processed files -- generated in a 100% deterministic way from the content of the `raw` dir. can be overwritten at will.
|- final/                  -- any output that we can use elsewhere, including hand-crafed reports, visualizations etc. -- based on raw and interim. treat with care.

notebooks/
|- _ns/                    -- your dir with your _n_ame and _s_urname
|- _jd/                    -- John Doe's dir
|- Exploration.ipynb       -- shared notebook with a clear name (let's include timestamps if needed: 2020-09-28_15-45_file_name.ext)
|- stable/                 -- stuff that works. always possible to submit as a solution. writes to this folder are to be done only at team meetings.
   |- 2020-09-28_21-02_e2e_exploration_and_api -- an example self-contained snapshot of something that really works (if supplied with correct data/raw (relies on the fact that `raw` is add-only))
```
