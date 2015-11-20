# Da'at Hamakom

Interactive mapping platform for research data visualization

## Dev

### Prerequisites

 - Python 3.4+
 - PostgreSQL

### Bootstrap

```bash
$ mkvirtualenv daat -p `which python3`
$ pip install -r requirements.txt
$ createdb daat
$ ./manage.py migrate
```

Make sure you create the `daat` database with a user that has superuser privilege (this is default for OS X installations through homebrew). This is required so that the migrations can add the hstore extension.
