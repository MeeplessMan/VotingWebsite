# VotingWebsite - Atesh Branch
![DUT logo image](/Images/dut-logo.png)

## Description
This is a web application developed for the purpose of replacing the current SRC Voting System in place for Durban University of Technology(DUT). This system incompases the student voting proccess and the administrative system to manage the yearly voting for SRC's at DUT. The web applicatopm encompasses a efficient and easy to use voting system which should be usable by all of DUT's students. The adminstrative section shall be used to manage all current elections, past election and future elections occuring in the application.

## Database
The current database in place is a SQLite RDBMS which is the default database template for the SQLAlchemy package. The current models in the database are:

- user
- vote
- ballot
- election
- candidate

ERD MODEL:

- ![ERD Model](images/erd.png)

- User:
    - id
    - email
    -

## Dependacies
All the dependacies are listed in requirements.txt. To install all dependancies into your flaskenv folder you woruld run the command `pip install -r requirements.txt`:

```
alembic==1.15.1
blinker==1.9.0
certifi==2025.1.31
click==8.1.8
colorama==0.4.6
distlib==0.3.9
filelock==3.18.0
Flask==3.1.0
Flask-DotEnv==0.1.2
Flask-Login==0.6.3
Flask-Mail==0.10.0
Flask-Migrate==4.1.0
Flask-SQLAlchemy==3.1.1
Flask-WTF==1.2.2
greenlet==3.1.1
itsdangerous==2.2.0
Jinja2==3.1.6
Mako==1.3.9
MarkupSafe==3.0.2
packaging==24.2
platformdirs==4.3.7
python-dotenv==1.0.1
setuptools==77.0.3
SQLAlchemy==2.0.39
typing_extensions==4.12.2
virtualenv==20.29.3
Werkzeug==3.1.3
WTForms==3.2.1
```



## Contributors
- MeeplessMan - Atesh Reddy
- Prevani - Prevani Moodley
- 4444ToniHector - Ndingeko Unathi Gumede
- ndeluOmncane - Amahle Bhulose
- nkanyiso02 - Nkanyiso Xaba
- ShabalalaThabo - Thabo Shabalala
- ViolanReddy - Violan Reddy
- Kea02-dot - Keabetswe Kadiege
- tshepo-exe - Tshepo Masiteng
- Magubane20|| - Siboniso Magubane