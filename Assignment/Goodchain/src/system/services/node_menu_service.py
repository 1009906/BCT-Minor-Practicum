from datetime import datetime
from sqlite3 import IntegrityError
from src.system.context import Context

def update_last_login_date():
    con = Context.db_connection
    c = con.cursor()
    datetime_now = datetime.now()

    try:
        c.execute(
            "UPDATE users "
            "SET    LastLogin = ? "
            "WHERE Name = ?"
            , (datetime_now, Context.user_name))

        if c.rowcount == 1:
            con.commit()
            Context.last_login_date = datetime_now
            return True, "User updated."
        else:
            return False, "Error: Could not update user."

    except IntegrityError as e:
        return False, str(e)