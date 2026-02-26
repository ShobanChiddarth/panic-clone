# PANIC CLONE

When you want to clone all repositories of multiple people immediately.

### REQUIREMENTS
1. Python 3.12.3
2. `pip install -r requirements.txt` (python-dotenv is optional)
3. git

### Setup
1. Go to https://github.com/settings/personal-access-tokens/new
2. Select required "Repository Access"
3. "Contents" permission is required with read access
4. Generate token, confirm it, copy it
5. Duplicate the file `sample.env` into `.env`
6. Edit the file `.env` and replace "<YOUR-TOKEN>" with what you just copied

### Usage

1. Run [github-api-testing.py](./github-api-testing.py) if you want to test your API credentials
2. Run [github-main.py](./github-main.py) to start the process
3. Enter list of usernames you wan't to mass clone from
4. Enter the target directory you wan't to save cloned repos (dir names starting with "clone_output" are gitignored in this repo)
5. Enter git clone depth (`None` if you want full history or `1` for faster cloning)
6. Wait until it is Done.

