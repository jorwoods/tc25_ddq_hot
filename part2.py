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
    
def update_connection(server: TSC.Server, workbook: TSC.WorkbookItem, new_connection: TSC.ConnectionItem) -> None:
    """
    Update the connection of a workbook.

    :param server: Tableau server instance
    :param workbook: WorkbookItem to update
    :param new_connection: New connection item to set
    """
    # Get the current workbook details
    server.workbooks.populate_connections(workbook)

    # Create a copy of the workbook connections by iterating over the Pager.
    connections = [c for c in workbook.connections if c.server_address == new_connection.server_address]
    
    # Update the connection details to keep the same connection ID
    for conn in connections:
        conn.server_address = new_connection.server_address
        conn.username = new_connection.username
        conn.password = new_connection.password
        server.workbooks.update_connection(workbook, conn)

    return connections

with server.auth.sign_in(auth):
    # Get the workbook by name
    workbook = get_workbooks(server, "TC25 DDQ HOT")
    assert workbook is not None, "Workbook not found"
    
    fixed_connection = TSC.ConnectionItem()
    fixed_connection.server_address = "aws-0-us-west-1.pooler.supabase.com"
    fixed_connection.username = "postgres.xqeozpibcbggvezbxjps"
    fixed_connection.password = ""
    fixed_connection.server_port = "5432"
    fixed_connection.connection_type = "postgres"
    update_connection(server, workbook, fixed_connection)
    print(f"Updated connection for workbook '{workbook.name}' with new server address '{fixed_connection.server_address}'.")

