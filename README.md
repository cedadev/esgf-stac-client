# ESGF STAC Client library

## Usage

TBC

## Development and testing

Here is a quick guide to getting started so that you can run the unit tests:

```
ssh sci3.jasmin.ac.uk # If you are running on a `sci` server, otherwise run where you like

mkdir stac
cd stac/

module load jaspy # If running on a `sci` server, if not, just make sure you have a python3 installed

python -m venv stac-venv
source stac-venv/bin/activate

gh_user_token="GITHUB_ID:GITHUB_ACCESS_TOKEN"

# Clone local versions of the repositories that we might modify
git clone https://${gh_user_token}@github.com/cedadev/pystac-client

# Go in and change to our working branch, and install dependencies
cd pystac-client/
git checkout asset-search

pip install -e .

cd ../

git clone https://${gh_user_token}@github.com/cedadev/esgf-stac-client
cd esgf-stac-client/

pip install -e  .

# Install requirements for development, e.g. "pytest"
pip install -r requirements_dev.txt

# Run the tests
python -m pytest -v tests
```

You should see some output showing that tests have run.
