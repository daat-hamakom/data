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
$ createuser -d daat && createdb daat -O daat
$ ./manage.py migrate
```
