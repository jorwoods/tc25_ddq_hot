# tc25_ddq_hot
Tableau Conference 2025 Hands On Training - DataDevQuest


[Tableau DataDev slack](https://tabsoft.co/JoinTableauDev)

For this training session, we are going to use python and the Tableau Server
Client (TSC) library.

[Tableau Server Client Documentation](https://tableau.github.io/server-client-python/docs/)

## Install python and dependencies

For this lab, I will be using [uv to manage python and its dependencies](https://astral.sh) for me. If you are familiar with Python, feel free to do it however you know how.

If you're on Windows, you can install it like this:
```pwsh
irm "https://astral.sh/uv/0.6.6/install.ps1" | iex
```

On Mac/Linux, like this:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**Make sure to close the terminal and reopen it to ensure that uv is available in your PATH.**

Now, install Python, initialize your project, and add our dependencies.
```bash
uv python install 3.12
uv init
uv add python-dotenv
uv add tableauserverclient
```
If you have issues on your machine, it may be due to the certificates installed on your machine. You can whitelist them as follows, and rerun the install commands.

```pwsh
# Windows
$env:UV_NATIVE_TLS=1
uv python install 3.12
uv init
uv add python-dotenv
uv add tableauserverclient
```

```bash
# Mac or Linux
UV_NATIVE_TLS=1
uv add python-dotenv
uv add tableauserverclient
```

## Authentication

Connecting to Tableau Server with the REST API has a few options. Username and 
password is what you might expect to use, but certain Server configurations can
make that difficult. If the Server is configured for Single Sign On (SSO) or 
Multi Factor Authentication (MFA) then username and password will not work. I 
suggest creating a Personal Access Token (PAT) for signing in. 

### Create a Personal Access Token

First, go to your account settings.

![Navigate to account settings](assets/account_settings.jpg)

Then, create a new Personal Access Token. The server requires you enter a name
to be able to create the token. Be sure to copy your secret key out before 
closing the dialog. You will not be able to see it again.


![Enter a name for the personal access token](assets/name_your_pat.jpg)


![Copy your secret from the dialog box](assets/copy_your_secret.jpg)

### Using the Personal Access Token

Now that you have your token name and secret, you will need to use them to
login to the server. I have found using ".env" files to be a good way to keep
secrets out of the code. Here is an example ".env" file that you can use to
store your PAT.

```plaintext
# .env

# Tableau Server
TABLEAU_SERVER=https://10az.online.tableau.com
TABLEAU_PAT_NAME=your-pat-name
TABLEAU_PAT_SECRET=your-pat-secret
```

These secrets can be loaded into your code using the `dotenv` package. Here is
how to install the dotenv package for python.

Now, we can read in the secrets and use them to login to the server.

### JWT Scopes
If you decide to use JWT authentication, you will need the following scopes for this lab:

```plaintext
tableau:content:read
tableau:jobs:read
tableau:workbooks:update
tableau:views:download
```

## Find Your Site ID

To work with the REST API, you need the site ID as it appears in the URL.

!IMAGE[find_site_id.jpg](instructions287866/find_site_id.jpg)

## Publish demo workbook

Use the publish.py script to publish the workbook to your test site.
If you want to publish to a project besides the default, set the
environment variable `TABLEAU_PROJECT_NAME` in your .env file.


## Challenge 1

Find a specific workbook on your site, as determined by its name.
Search for the workbook name "TC25 DDQ HOT".

You may find the following helpful:

- [Filtering and Sorting in the Tableau REST API](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm)
- [TSC Filter and Sort](https://tableau.github.io/server-client-python/docs/filter-sort)
- [TSC Docs: Workbooks](https://tableau.github.io/server-client-python/docs/api-ref#workbooks)
- [TSC: Move workbook projects](https://github.com/tableau/server-client-python/blob/master/samples/move_workbook_projects.py)

## Challenge 2

Update the database credentials. The password is out of date. Update
it to the correct value: `"upxm5sverHnLlgwj"`.

- [Update connection sample](https://github.com/tableau/server-client-python/blob/master/samples/update_connection.py)
- [Query Workbook Connections](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#query_workbook_connections)
- [Update workbook connection](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_connection)


## Challenge 3

Trigger a data refresh on that workbook. Set it up
to wait until the refresh has completed.

- [TSC Docs: Workbooks](https://tableau.github.io/server-client-python/docs/api-ref#workbooks)
- [Update workbook Now](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#update_workbook_now)

## Challenge 4

Get a PDF of the updated workbook. Set the `maxAge` to be 1
minute.

- [Download Workbook PDF](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_ref_workbooks_and_views.htm#download_workbook_pdf)
- [TSC Export](https://github.com/tableau/server-client-python/blob/master/samples/export.py)
- [View filter queries](https://help.tableau.com/current/api/rest_api/en-us/REST/rest_api_concepts_filtering_and_sorting.htm#Filter-query-views)
- [TSC Filter and Sort](https://tableau.github.io/server-client-python/docs/filter-sort)

