from src.user_interface.public_menu import PublicMenu
from src.database.connection import get_connection
from src.system.context import Context

if __name__ == "__main__":
    # De database moet nog een nieuwe file voor gemaakt worden, dit is die van analyse 8.
    Context.db_connection = get_connection()
    public_menu = PublicMenu()
    public_menu.run()