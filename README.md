# codesquad-dashboard
### codesquad-dev.herokuapp.com

## Integration branch tests status:

[![CircleCI](https://circleci.com/gh/jwde/codesquad-dashboard/tree/integration.svg?style=svg&circle-token=ef3c1ffb1aaef7fb29685f4ff1410e52183c7327)](https://circleci.com/gh/jwde/codesquad-dashboard/tree/integration)

## Master branch tests status:

[![CircleCI](https://circleci.com/gh/jwde/codesquad-dashboard.svg?style=svg&circle-token=ef3c1ffb1aaef7fb29685f4ff1410e52183c7327)](https://circleci.com/gh/jwde/codesquad-dashboard)


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
    
6. Install postgres -- The remote server will be running version 9.5.4, but you'll be unlikely to have problems as long as you're running a version >= 9.3.14.

7. Install the python package requirements to your virtualenv

    `    cd codesquad-dashboard`

    `    pip install -r requirements.txt`

8. Start postgres service

    This is platform dependent. On Ubuntu, the command is:

    `    sudo /etc/init.d/postgresql start`
    On OSX it's:
    
    `    pg_ctl -D /usr/local/var/postgres -l /usr/local/var/postgres/server.log start`

9. Make codesquad database

    Note: when prompted to set a password for the postgres user, give a password you don't mind becoming public, it will be stored in plaintext.

    In linux (tested only on Ubuntu so far), the postgres installation should have created a new system user: postgres. In a new shell run:

    `    sudo su - postgres`

    `    createuser -P`

    `    createdb codesquad`

    `    psql`

    Then, in the postgres console, run:

    `    GRANT ALL PRIVILEGES ON DATABASE codesquad TO postgres;`

    On osx (tested on Mavericks), there will not be a system user postgres. Instead, run:

    `    createuser -P postgres`

    `    createdb codesquad`

    `    psql -d codesquad`

    Then, in the postgres console, run:

    `    GRANT ALL PRIVILEGES ON DATABASE codesquad TO postgres`

    `    ALTER DATABASE codesquad OWNER TO postgres`

10. Set up environment variables

    On linux, open ~/.profile, on osx, open ~/.bash\_profile (this file might not exist yet), and add the following line:

    `    export DATABASE_URL="postgres://postgres:password@localhost:5432/codesquad"`

11. Runnning the server

    `   python manage.py runserver`


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
5. Once you have an approval to the pull request, merge to integration and remove the feature branch.
6. If integration passes all tests (check for results in the integration channel on slack), merge to master, otherwise fix the problems first.
