#!/usr/bin/env uv run --script
# ///script
# requires_python = ">=3.10"
# dependencies = [
#   "tableauserverclient",
#   "python-dotenv",
# ]
# ///

"""
This script sets up the workbook on Tableau Server using the Tableau Server Client (TSC) library.

The following environment variables are required:

TABLEAU_SERVER
TABLEAU_SITE
TOKEN_NAME
TOKEN_SECRET
TABLEAU_PROJECT_NAME

If TABLEAU_PROJECT_NAME is not set, it defaults to "Default".

"""

from contextlib import contextmanager
import os
from pathlib import Path

import tableauserverclient as TSC
from dotenv import load_dotenv

load_dotenv()

@contextmanager
def get_server():
    """
    Connect to the Server using the credentials from environment variables.
    """
    server = TSC.Server(os.environ["TABLEAU_SERVER"], True)
    auth = TSC.PersonalAccessTokenAuth(
        token_name=os.environ["TOKEN_NAME"],
        personal_access_token=os.environ["TOKEN_SECRET"],
        site_id=os.environ["TABLEAU_SITE"],
    )
    with server.auth.sign_in(auth):
        yield server

def publish_workbook(server: TSC.Server, workbook_file_path: str) -> TSC.WorkbookItem:
    project_name = os.getenv("TABLEAU_PROJECT_NAME", "Default").casefold()
    project = next((p for p in TSC.Pager(server.projects) if p.name.casefold() == project_name))

    # Publish the workbook
    workbook = TSC.WorkbookItem(project.id, "TC25 DDQ HOT")
    workbook = server.workbooks.publish(
            workbook,
            str(workbook_file_path),
            TSC.Server.PublishMode.Overwrite,
            # connections=[connection],
            skip_connection_check=True,
        )
    
    return workbook

def add_connection_details(server: TSC.Server, workbook: TSC.WorkbookItem) -> None:
        connection = TSC.ConnectionItem()
        connection.server_address = "aws-0-us-west-1.pooler.supabase.com"
        connection.server_port = "5432"
        connection.username = "postgres.xqeozpibcbggvezbxjps"
        connection.password = "abcd"
        connection.embed_password = True
        
        server.workbooks.populate_connections(workbook)
        connections = [c for c in workbook.connections if c.server_address == connection.server_address]
        for conn in connections:
            conn.server_address = connection.server_address
            conn.server_port = connection.server_port
            conn.username = connection.username
            conn.password = connection.password
            conn.embed_password = True

            server.workbooks.update_connection(workbook, conn)


def main() -> None:
    with get_server() as server:
        server: TSC.Server
        # Get the project ID
        
        workbook_file_path = Path(__file__).parent / "TC25 DDQ HOT.twbx"
        workbook = publish_workbook(server, workbook_file_path)
        print(f"Published workbook: {workbook.name}")
        add_connection_details(server, workbook)


if __name__ == "__main__":
    main()
