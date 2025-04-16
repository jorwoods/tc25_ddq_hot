import tableauserverclient as TSC
import os
from dotenv import load_dotenv

load_dotenv()


server = TSC.Server(os.environ["TABLEAU_SERVER"], use_server_version=True)
auth = TSC.PersonalAccessTokenAuth(os.environ["TOKEN_NAME"], os.environ["TOKEN_SECRET"], site_id=os.environ["TABLEAU_SITE"])

def get_workbooks(server: TSC.Server, name: str) -> TSC.WorkbookItem | None:
    """
    Get a workbook by its name.

    :param server: Tableau server instance
    :param name: Name of the workbook to search for
    :return: WorkbookItem if found, None otherwise
    """
    workbooks = server.workbooks.filter(name=name)
    if len(workbooks) == 0:
        print(f"Workbook '{name}' not found.")
        return None
    elif len(workbooks) > 1:
        print(f"Multiple workbooks found with name '{name}'. Please specify a unique name.")
        return None
    else:
        print(f"Workbook '{name}' found.")
        return workbooks[0]

with server.auth.sign_in(auth):
    # Get the workbook by name
    workbook = get_workbooks(server, "TC25 DDQ HOT")
    assert workbook is not None, "Workbook not found"
