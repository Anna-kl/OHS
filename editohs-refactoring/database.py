login = "postgres"
password = "2537300"
host = "localhost"
port = "5432"
db_name = "postgres"


database_url = "postgresql://{0}:{1}@{2}:{3}/{4}".format(login, password, host, port, db_name)
print(database_url)

