A small script to ping multiple IP v4 addresses concurrently.
After installation you can refer to `run.py --help` for more info.

# Installation using virtualenv

Install virtualenv:

`pip install virtualenv`

Create a virtualenv:

`virtualenv <VIRTUALENV DIRECTORY OF YOUR CHOOSING>`

E.g.:
`virtualenv ~\.venvs\pingthem`

Activate new virtualenv:

`<VIRTUALENV DIRECTORY OF YOUR CHOOSING>\Scripts\activate.ps1`

E.g.:
`~\.venvs\pingthem\Scripts\activate.ps1`

Install the dependencies:

`pip install -r requirements.txt`

# Running

To check available parameters:

`python run.py --help`

Example invocation:

`python .\run.py 192.168.0.0/28`

With extra params - timeout 1 second and 100 concurrent pings:

`python .\run.py 192.168.0.0/28 -t 1 -c 100`