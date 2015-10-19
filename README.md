# Da'at Hamakom

Interactive mapping platform for research data visualization

## Dev

### Prerequisites

 - Python 3.4+
 - PostgreSQL

### Bootstrap

```bash
$ mkvirtualenv sixpm -p `which python3`
$ pip install -r requirements.txt
$ createuser -d sixpm && createdb sixpm -O sixpm
$ ./manage.py migrate
```
