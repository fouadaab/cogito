# Cogito
Automate Billing to Clients. <br>
<br>
<br>
**Init**: <br>
Clone the repository and install list of required packages: <br>
```
git clone git_repo_address .
pip install -r /path/to/requirements.txt
```

**Keyring and Email**: <br>
Documentation to [keyring pip product](https://pypi.org/project/keyring/) <br>
Set up keyring in local environment and retrieve in code using get_credential() method. <br>
Specify which service and username, used to log into email api. <br>
Attributes will need to be adjusted in the ini config file "conf.ini" (domain, email address, sender). <br>
<br>
**Firebase (Google DB)**: <br>
Set up a Firebase DataBase in Google account. <br>
Name of the project (project-id) and key file should also be adjusted in the config file to match. <br>
The key file (json) to connect to Firebase should be placed inside the "./firebase" folder. <br>
<br>
**Data**: <br>
Create a "./data" folder at the main script's location. <br>
It should include a minimum of two files: <br>
1. Excel of accounting data from Cogito App's extract <br>
2. PDF of all client's invoices to be split <br>

The name of those files should match "EXCEL_FILE" and "PDF_FILE" attributes in the config file. <br>

