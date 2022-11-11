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

# Make a setup-env file (to use each time you want to set the environment)
echo "source stac-venv/bin/activate" > setup-env.sh

# Set the environment
source ./setup-env.sh

# If using a github token do the following
gh_user_token="GITHUB_ID:GITHUB_ACCESS_TOKEN"
git clone https://${gh_user_token}@github.com/cedadev/pystac
git clone https://${gh_user_token}@github.com/cedadev/pystac-client
git clone https://${gh_user_token}@github.com/cedadev/esgf-stac-client

# Else if using github SSH keys, do
git clone git+https://github.com/cedadev/pystac
git clone git+https://github.com/cedadev/pystac-client
git clone git+https://github.com/cedadev/esgf-stac-client

# Go in and change to our working branches, and install dependencies
cd pystac/
git checkout asset-search
pip install -e .
cd ../

cd pystac-client/
git checkout asset-search
pip install -e .
cd ../

cd esgf-stac-client/
pip install -e  .

# Install requirements for development, e.g. "pytest"
pip install -r requirements_dev.txt

# Run the tests
python -m pytest -v tests
```

You should see some output showing that tests have run.
