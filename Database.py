from datetime import datetime

import pymysql

hostname = "Localhost"
username = "root"
password = "1234"
databasename = "dbProject"
port = 3307
tableName = {'user', 'repository', 'like', 'star', 'issue', 'watch', 'answer', 'notification'}


class DatabaseMiddleWare(object):
    dbRef = None
    offline = None
    curType = pymysql.cursors.DictCursor

    @staticmethod
    def initialize():
        try:
            DatabaseMiddleWare.dbRef = pymysql.connect(host=hostname, port=port, user=username, passwd=password,
                                                       db=databasename)
            for s in tableName:
                if not DatabaseMiddleWare.checkTableExists(s):
                    DatabaseMiddleWare.createTable(s)
        except:
            DatabaseMiddleWare.onException()

    @staticmethod
    def onException():
        DatabaseMiddleWare.offline = True

    @staticmethod
    def execute(query=None):
        if DatabaseMiddleWare.offline == True:
            return None
        if query is not None:
            cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
            cur.execute(query)
            records = cur.fetchall()
            return records

    @staticmethod
    def getRepoNumber():
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute(
            "SELECT count(id) AS count FROM repository")
        record = cur.fetchall()
        return record

    @staticmethod
    def getUsersNumber():
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute(
            "SELECT count(username) AS count FROM user")
        record = cur.fetchall()
        return record

    @staticmethod
    def fetchUser(username):
        usernameStr = str(username)
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute("SELECT * FROM user WHERE username =" + usernameStr)
        record = cur.fetchone()
        return record



    @staticmethod
    def checkTableExists(tablename):
        dbcur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        dbcur.execute("""SELECT COUNT(*) FROM information_schema.tables WHERE table_name = '{0}'""".format(
            tablename.replace('\'', '\'\'')))
        if dbcur.fetchone()[0] == 1:
            dbcur.close()
            return True
        dbcur.close()
        return False

    def createTable(self, tableName):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        switcher = {
            'user': "CREATE TABLE  user ("
                    "id int PRIMARY KEY,"
                    "username VARCHAR (20) UNIQUE NOT NULL,"
                    "email VARCHAR (100) UNIQUE NOT NULL,"
                    "first_name VARCHAR (25) NOT NULL,"
                    "last_name VARCHAR (45) NOT NULL,"
                    "gender INT(1) DEFAULT 1 NOT NULL,"
                    "birthday DATE);",

            'repository': "CREATE TABLE repository ("
                          "id int PRIMARY KEY,"
                          "repo_name VARCHAR (120) UNIQUE NOT NULL,"
                          "description VARCHAR (300),"
                          "is_private INT(1) DEFAULT 0,"
                          "is_forked INT(1) DEFAULT 0,"
                          "source_id INT DEFAULT -1,"
                          "owner_id INT NOT NULL,"
                          "create_date DATE,"
                          "FOREIGN KEY (owner_id) REFERENCES user(id));",

            'star': "CREATE TABLE star (id int PRIMARY KEY,"
                    "rep_id INT NOT NULL,"
                    "user_id INT NOT NULL,"
                    "FOREIGN KEY (user_id) REFERENCES user(id), "
                    "FOREIGN KEY (rep_id) REFERENCES repository(id));",

            'watch': "CREATE TABLE watch (id int PRIMARY KEY,"
                     "rep_id INT NOT NULL,"
                     "user_id INT NOT NULL,"
                     "FOREIGN  KEY  (user_id) REFERENCES  user(id),"
                     "FOREIGN  Key (rep_id) REFERENCES repository(id));",

            'issue': "CREATE TABLE issue ("
                     "id INT PRIMARY KEY,"
                     "title VARCHAR(45) NOT NULL,"
                     "issue_type INT NOT NULL DEFAULT 1,"
                     "description VARCHAR (500) NOT NULL ,"
                     "rep_id INT NOT NULL ,"
                     "user_id INT NOT NULL ,"
                     "is_open INT NOT NULL DEFAULT 1,"
                     "FOREIGN KEY  (user_id) REFERENCES user(id),"
                     "FOREIGN KEY  (rep_id) REFERENCES repository(id));",

            'notification':
                "CREATE TABLE notification ( "
                "id INT PRIMARY KEY , "
                "user_id INT NOT NULL ,"
                "title VARCHAR(45) NOT NULL, "
                "description VARCHAR (200) NOT NULL,"
                "link_id INT NOT NULL ,"
                "link_type INT(1) NOT NULL ,"
                "is_read INT (1) DEFAULT 0 , "
                "created_date DATE NOT NULL,"
                "FOREIGN KEY (user_id) REFERENCES user(id));",

            'answer':
                "CREATE TABLE answer ("
                "id INT PRIMARY  KEY , "
                "user_id INT NOT NULL ,"
                "issue_id INT NOT  NULL ,"
                "title VARCHAR(45) NOT  NULL,"
                "description VARCHAR(200) NOT  NULL,"
                "is_correct INT(1) DEFAULT 0,"
                "created_date DATE NOT NULL,"
                "FOREIGN (user_id) REFERENCES user(id),"
                "FOREIGN (issue_id) REFERENCES issue(id));",

            'like':
                "CREATE TABLE like("
                "issue_id INT NOT NULL,"
                "answer_id INT NOT NULL ,"
                "user_id INT NOT NULL,"
                "PRIMARY KEY (issue_id,answer_id,user_id),"
                "FOREIGN KEY (issue_id) REFERENCES issue(id),"
                "FOREIGN KEY (answer_id) REFERENCES answer(id),"
                "FOREIGN KEY (user_id) REFERENCES user(id));"
        }

        selectedQuery = switcher.get(tableName, None)
        if selectedQuery != None:
            cur.execute(selectedQuery);
        else:
            print(tableName + " is not a valid table");

    @staticmethod
    def getEntityByKey(tableName, **kwargs):
        """
        Fetching a tuple from table with key
        """
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        statement = ""
        for key in kwargs:
            statement += key + "=" + kwargs[key] + " AND ";
        statement = statement[:-5]
        query = "SELECT * FROM " + tableName + " WHERE " + statement
        cur.execute(query)
        return cur.fetchone

    @staticmethod
    def createRepository(repositoryName, user_id, description, is_private):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        date = datetime.datetime.now()
        query = "INSERT INTO TABLE repository (repo_name,description,is_private,owner_id,create_date) VALUES(" + repositoryName + " , " + description + " , " + is_private + " , " + user_id + " , " + date + ")"
        cur.execute(query)

    @staticmethod
    def forkRepository(source_id, user_id, is_private):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        date = datetime.datetime.now()

        query = "INSERT INTO TABLE repository (repo_name,description,is_forked,source_id,is_private,owner_id,create_date) " \
                "SELECT repo_name,description,1,source_id" + is_private + "," + user_id + "," + date + " FROM TABLE WHERE id=" + source_id + " UPDATE source_id CASE source_id=-1 THEN " + source_id
        cur.execute(query)

    @staticmethod
    def register(user):
        pass


