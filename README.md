# codesquad-dashboard
### codesquad-dev.herokuapp.com

## Environment setup:

1. Install python 2.7 and pip if not already installed.

2. Install virtualenv:

`    pip install virtualenv`

3. Make a directory for codesquad

`    mkdir codesquad`

`    cd codesquad`

4. In the codesquad directory, make a virtualenv and clone this repository

`    virtualenv venv`

`    git clone https://github.com/jwde/codesquad-dashboard.git`


5. Activate the virtualenv (do this every time you work on it)

`    source venv/bin/activate`

6. Install the python package requirements to your virtualenv

`    cd codesquad-dashboard`

`    pip install requirements.txt`


## Workflow

### Working on a new feature:

1. Make a clean feature branch based on the current master

`    git checkout master`

`    git pull origin master`

`    git checkout -b (feature name)`

2. Implement feature and tests (try running tests with `python manage.py test`)
3. Push feature branch

`    git add (files added)`

`    git commit -m "description of work"`

`    git push --set-upstream origin (feature name)`

4. Open a pull request to merge it with the integration branch
5. Once you have two approvals to the pull request, merge to integration and remove the feature branch.
6. If integration passes all tests (check for results in the integration channel on slack), merge to master, otherwise fix the problems first.
