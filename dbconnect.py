import MySQLdb

def connection():
    conn = MySQLdb.connect(host="Localhost",
                           user = "user",
                           passwd = "password",
                           db = "Database")
    c = conn.cursor()

    return c, conn
		
