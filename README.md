# EyesOnWhitney
Scans recreation.gov for open permits on Mt Whitney. With great power comes great responsibility.


To clone the repo:
```
git clone https://github.com/josemorenoo/EyesOnWhitney.git
```

To install dependencies:
```
python3 -m venv myvenv #creates path to new virtual environment called `myvenv`
source myvenv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

For now, run 
```
python3 permitChecker.py
```
This triggers a schedule that runs every five minutes. If no permits are found, a sanity check print statement is made, otherwise you will get an email