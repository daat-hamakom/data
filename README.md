# Da'at Hamakom Data Models and Backend Admin

Django-based project running the Da'at Hamakom backend data models and admin panel.
Usage of the project code and resources in this repository is under the conditions specified in LICENSE.txt as provided by Yissum, on behalf of the Hebrew University of Jerusalem.

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
