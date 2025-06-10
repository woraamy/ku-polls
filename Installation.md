# Instructions for Installing and Running the App

## 1. Clone the repository from GitHub
Cloning the repository from GitHub by running this command on your command prompt
```commandline
git clone https://github.com/woraamy/ku-polls.git
```
## 2. Create a virtual environment
* You can create a virtual environment for running the Application by running this command line on terminal
```commandline
python -m venv .venv
```
this command line will create a subdirectory that contains virtual environment named '.venv'
* Start the virtual environment by running this command
```commandline
source .venv/bin/activate
```
* Install the `requirements.txt` file which contains names of required packages by running the command
```commandline
pip install -r requirements.txt
```
* You can deactivate the virtual environment by running 
```commandline
deactivate
```
## 3. Run migrations
* To create a new database for the Application, run the following command
```commandline
python manage.py migrate
```

## 4. Install data from data fixtures
* To load initial data of the Application, run the following command
```commandline
python manage.py loaddata data/polls.json data/users.json
```

## 5. Run tests
* To run tests for the application, run the following command
```commandline
python manag.py runtest polls
```
