from datetime import datetime

import pymysql

hostname = "localhost"
username = "root"
password = "1234"
databasename = "TESTDB"
port = 330
tableName = ['user', 'repository', 'star', 'issue', 'watch', 'answer', 'likeRep' , 'notification']


class DatabaseMiddleWare(object):
    dbRef = None
    offline = None
    curType = pymysql.cursors.DictCursor

    @staticmethod
    def createTable(tname):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        switcher = {
            'user': "CREATE TABLE  user ("
                    "id int PRIMARY KEY AUTO_INCREMENT,"
                    "username VARCHAR (20) UNIQUE NOT NULL,"
                    "password VARCHAR (20) NOT NULL ,"
                    "email VARCHAR (100) UNIQUE NOT NULL,"
                    "first_name VARCHAR (25) NOT NULL,"
                    "last_name VARCHAR (45) NOT NULL,"
                    "gender INT(1) DEFAULT 1 NOT NULL,"
                    "question_number INT(1) NOT NULL,"
                    "answer VARCHAR (150) NOT NULL);",

            'repository': "CREATE TABLE repository ("
                          "id int PRIMARY KEY AUTO_INCREMENT,"
                          "repo_name VARCHAR (120) UNIQUE NOT NULL,"
                          "description VARCHAR (300),"
                          "is_private INT(1) DEFAULT 0,"
                          "is_forked INT(1) DEFAULT 0,"
                          "source_id INT DEFAULT -1,"
                          "owner_id INT NOT NULL,"
                          "create_date DATE,"
                          "FOREIGN KEY (owner_id) REFERENCES user(id));",

            'star': "CREATE TABLE star ("
                    "id int PRIMARY KEY AUTO_INCREMENT,"
                    "rep_id INT NOT NULL,"
                    "user_id INT NOT NULL,"
                    "FOREIGN KEY (user_id) REFERENCES user(id), "
                    "FOREIGN KEY (rep_id) REFERENCES repository(id));",

            'watch': "CREATE TABLE watch ("
                     "id int PRIMARY KEY AUTO_INCREMENT,"
                     "rep_id INT NOT NULL,"
                     "user_id INT NOT NULL,"
                     "FOREIGN  KEY  (user_id) REFERENCES  user(id),"
                     "FOREIGN  Key (rep_id) REFERENCES repository(id));",

            'issue': "CREATE TABLE issue ("
                     "id INT PRIMARY KEY AUTO_INCREMENT,"
                     "title VARCHAR(45) NOT NULL,"
                     "issue_type INT NOT NULL DEFAULT 1,"
                     "description VARCHAR (500) NOT NULL ,"
                     "rep_id INT NOT NULL ,"
                     "user_id INT NOT NULL ,"
                     "is_open INT NOT NULL DEFAULT 1,"
                     "FOREIGN KEY  (user_id) REFERENCES user(id),"
                     "FOREIGN KEY  (rep_id) REFERENCES repository(id));",

            'notification':"CREATE TABLE notification ( "
                "id INT PRIMARY KEY AUTO_INCREMENT, "
                "user_id INT NOT NULL ,"
                "title VARCHAR(45) NOT NULL, "
                "description VARCHAR (200) NOT NULL,"
                "link_id INT NOT NULL ,"
                "link_type INT(1) NOT NULL ,"
                "is_read INT (1) DEFAULT 0 , "
                "created_date DATE NOT NULL,"
                "FOREIGN KEY (user_id) REFERENCES user(id));",

            'answer':"CREATE TABLE answer ("
                "id INT PRIMARY  KEY AUTO_INCREMENT, "
                "user_id INT NOT NULL ,"
                "issue_id INT NOT  NULL ,"
                "title VARCHAR(45) NOT  NULL,"
                "description VARCHAR(200) NOT  NULL,"
                "is_correct INT(1) DEFAULT 0,"
                "created_date DATE NOT NULL,"
                "FOREIGN KEY (user_id) REFERENCES user(id),"
                "FOREIGN KEY (issue_id) REFERENCES issue(id));",

            'likeRep':"CREATE TABLE likeRep("
                "issue_id INT NOT NULL AUTO_INCREMENT,"
                "answer_id INT NOT NULL ,"
                "user_id INT NOT NULL,"
                "PRIMARY KEY (issue_id,answer_id,user_id),"
                "FOREIGN KEY (issue_id) REFERENCES issue(id),"
                "FOREIGN KEY (answer_id) REFERENCES answer(id),"
                "FOREIGN KEY (user_id) REFERENCES user(id));",
            'follow' :"""CREATE TABLE follow(
                      id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                      following_id INT NOT NULL,
                      follower_id INT NOT NULL CHECK (follower_id!=following_id),
                      FOREIGN KEY (following_id) REFERENCES user(id),
                      FOREIGN KEY (follower_id) REFERENCES user(id)
                      );"""
        }

        selectedQuery = switcher.get(tname, None)
        if selectedQuery is not None:
            cur.execute(selectedQuery)
        else:
            print(tname + " is not a valid table")


    @staticmethod
    def initialize():
        try:
            DatabaseMiddleWare.dbRef = pymysql.connect(host=hostname,port=3306, user=username, passwd=password,
                                                       db=databasename)
            # for s in tableName:
            #     if not DatabaseMiddleWare.checkTableExists(s):
            #         print("create "+s)
            #         DatabaseMiddleWare.createTable(s)
            #     else :
            #         print("table exists" + s)
        except:
            print("got to an exception")
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
    def getStarCount(repID):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute("SELECT count(*) AS stars FROM star WHERE rep_id = {RepoID}".format(RepoID=repID))
        record = cur.fetchone()
        return record

    @staticmethod
    def getUsersNumber():
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute(
            "SELECT count(username) AS count FROM user")
        record = cur.fetchall()
        return record
    @staticmethod
    def getUserById(id):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query="SELECT * FROM user WHERE id={id};".format(id=str(id))
        cur.execute(query)
        return cur.fetchone()

    @staticmethod
    def isFolowing(currentUser,targetUser):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "SELECT * FROM follow WHERE follower_id={currentUser} AND following_id={targetUser};".format(currentUser=str(currentUser),targetUser=str(targetUser))
        cur.execute(query)
        return cur.fetchone()
    @staticmethod
    def follow(currentUser,targetUser):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "INSERT INTO follow(follower_id,following_id) VALUES ({currentUser},{targetUser});".format(
            currentUser=str(currentUser), targetUser=str(targetUser))
        try:
            cur.execute(query)
            DatabaseMiddleWare.dbRef.commit()
        except Exception as e:
            print(str(e))

    @staticmethod
    def unfollow(currentUser, targetUser):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "DELETE FROM follow WHERE follower_id={currentUser} AND following_id={targetUser};".format(
            currentUser=str(currentUser), targetUser=str(targetUser))
        try:
            cur.execute(query)
            DatabaseMiddleWare.dbRef.commit()
        except Exception as e:
            print(str(e))
    @staticmethod
    def fetchIssuesForRepo(repo_id):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "SELECT * FROM issue is1 WHERE is1.rep_id={RepoID}".format(RepoID=repo_id)
        cur.execute(query)
        temp = cur.fetchall()
        print(str(temp))
        return temp

    @staticmethod
    def getTheAnswerOfIssue(my_issue_id):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "SELECT * FROM answer ans WHERE ans.issue_id = {IssueId}".format(IssueId=my_issue_id)
        print(query)
        cur.execute(query)
        temp = cur.fetchall()
        print(str(temp))
        return temp

    @staticmethod
    def fetchUser(username):
        usernameStr = str(username)
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute("SELECT * FROM user WHERE username = '{username}'".format(username=usernameStr))
        record = cur.fetchone()
        return record

    @staticmethod
    def checkTableExists(tablename):
        dbcur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        dbcur.execute("""SELECT COUNT(*) AS Count FROM information_schema.tables WHERE table_name = '{MyTable}';""".format(MyTable=tablename))
        temp = int(str(dbcur.fetchone()['Count']))
        if temp == 1:
            dbcur.close()
            return True
        dbcur.close()
        return False

    @staticmethod
    def recoverPassword(qNumber,answer,email):
        query="SELECT * FROM user WHERE user.email="+email
        dbcur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        dbcur.execute(query)
        if dbcur.fetchone()[0]['question_number']==qNumber:
            if dbcur.fetchone()[0]['answer']==answer:
                return dbcur.fetchone()[0]['password'];
            else:
                return "wrong answer dude!"
        else:
            return "wrong question dude!"

    @staticmethod
    def register(user):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        insertQuery = "INSERT INTO user(username,password,email,first_name,last_name,gender,question_number,answer)" \
                      "VALUES ('{username}','{password}','{email}','{first_name}','{last_name}','{gender}',1,'gogogol')"

        insertQueryfilled = insertQuery.format( username=user["username"],
                                                email=user["email"],
                                                password=user["password"],
                                                first_name=user["firstname"],
                                                gender=user["gender"],
                                                last_name=user["lastname"])
        try:
            cur.execute(insertQueryfilled)
            DatabaseMiddleWare.dbRef.commit()
        except:
            print("shit happens all the time")


    @staticmethod
    def getEntityByKey(tableName, **kwargs):
        """
        Fetching a tuple from table with key
        """
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        statement = ""
        for key in kwargs:
            statement2 = "{column} = {''}"
            statement += str(key) + "=" + str(kwargs[key]) + " AND "
        statement = statement[:-5]
        print(statement)
        query = "SELECT * FROM " + tableName + " WHERE " + statement
        cur.execute(query)
        return cur.fetchall()



    @staticmethod
    def createRepository(repositoryName, user_id, description, is_private):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        date = datetime.now()
        query = "INSERT INTO repository(repo_name, description , is_private , is_forked , source_id , owner_id , create_date) " \
                "values ('{RepoName}', '{Desc}' , {IsPrivate} , {IsForked},{SourceId} , {OwnerId} , '{CreateDate}');".format(RepoName=repositoryName,
                                                                                                                           OwnerId=user_id,
                                                                                                                           Desc=description,
                                                                                                                           IsPrivate=is_private,
                                                                                                                           IsForked=0,
                                                                                                                           SourceId=-1,
                                                                                                                           CreateDate=str(date)[:10])

        print(query)
        cur.execute(query)
        DatabaseMiddleWare.dbRef.commit()

    @staticmethod
    def forkRepository(source_id, user_id, is_private):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        date = datetime.datetime.now()

        query = "INSERT INTO TABLE repository (repo_name,description,is_forked,source_id,is_private,owner_id,create_date) " \
                "SELECT repo_name,description,1,source_id" + is_private + "," + user_id + "," + date + " FROM TABLE WHERE id=" + source_id + " UPDATE source_id CASE source_id=-1 THEN " + source_id
        cur.execute(query)

    @staticmethod
    def getIssueNumber():
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        cur.execute(
            "SELECT count(*) AS count FROM issue")
        record = cur.fetchall()
        return record

    @staticmethod
    def getAllRepoByName(name):
        print("fetching repo by name")
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        queryTemp = "SELECT r1.id repo_id ,us1.id user_id, repo_name , is_private , description , first_name , last_name " \
                "FROM repository r1,user us1 " \
                "WHERE us1.id = r1.owner_id  AND repo_name = '{repoName}' GROUP BY r1.id;"
        query = queryTemp.format(repoName = name)
        print(query)
        cur.execute(query)
        container = cur.fetchall()
        return container

    @staticmethod
    def findIssueByName(name):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query="SELECT title,repo_name,i.description,i.id as iid,r.id as rid from issue i ,repository r WHERE i.title LIKE '%{title}%' AND r.is_private=0 AND r.id=i.rep_id; ".format(title=name)
        print("find Issue " + query)
        cur.execute(query)
        result=cur.fetchall()
        return result

    @staticmethod
    def findUserByName(name):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "SELECT * from user WHERE username LIKE '%{name}%' OR first_name LIKE '%{name}%' OR last_name LIKE '%{name}%' ; ".format(name=name)
        print("find user= "+query)
        cur.execute(query)
        result = cur.fetchall()
        return result

    @staticmethod
    def findRepositoryByName(name):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        query = "SELECT repo_name,description,username,u.id as uid,r.id as rid from repository r ,user u WHERE repo_name LIKE '%{name}%'AND r.is_private=0 and u.id=r.owner_id; ".format(name=name)
        cur.execute(query)
        result = cur.fetchall()
        return result

    @staticmethod
    def getRepositoryByNameId(name,owner_id):
        print("fetching repo by name")
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        queryTemp = "SELECT * FROM repository WHERE repo_name='"+name+"' AND owner_id="+str(owner_id)+";"
        print("select= "+queryTemp)
        cur.execute(queryTemp)
        container = cur.fetchone()
        print("container= "+str(container))
        return container

    @staticmethod
    def fetchRepoDataById(id):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)
        queryTemp = "SELECT * from repository WHERE id={RepoID}".format(RepoID=id)
        print(queryTemp)
        cur.execute(queryTemp)
        temp = cur.fetchall()
        print(temp)
        return temp

    @staticmethod
    def getAllRepoOfTheUser(user):
        cur = DatabaseMiddleWare.dbRef.cursor(DatabaseMiddleWare.curType)

        querytemp = "SELECT  us1.first_name , us1.last_name ,r1.owner_id AS user_id, r1.id , repo_name , is_private , description " \
                "FROM repository r1 , user us1 " \
                "WHERE r1.owner_id={id} AND r1.owner_id = us1.id ;"
        query = querytemp.format(id=user["id"])
        print(query)
        cur.execute(query)
        temp = cur.fetchall()
        print("fetched \n"+str(temp))
        return temp

    def triggers(self):
        triggers ={
            "deleteIssues" : "CREATE TRIGGER dltIssue"
                             "AFTER DELETE ON repository"
                             "FOR EACH ROW"
                             "BEGIN"
                             "DELETE FROM issue WHERE issue.rep_id=repository.id;"
                             "END",

            "deleteAnswers" : "CREATE TRIGGER dltAnswer"
                              "AFTER DELETE ON issue"
                              "FOR EACH ROW"
                              "BEGIN"
                              "DELETE FROM answer WHERE answer.issue_id=issue.id;"
                              "END",

            "deleteStar" : "CREATE TRIGGER dltStar"
                           "AFTER DELETE ON repository"
                           "FOR EACH ROW"
                           "BEGIN"
                           "DELETE FROM star WHERE star.rep_id=repository.id;"
                           "END",

            "deleteStarUser" :  "CREATE TRIGGER dltStarUser"
                                "AFTER DELETE ON user AS u"
                                "FOR EACH ROW"
                                "BEGIN"
                                "DELETE FROM star WHERE star.user_id=u.id;"
                                "END",
            "createForkNotif" : "CREATE TRIGGER forkNotification"
                                "AFTER INSERT ON repository AS r"
                                "IF r.is_forked==1"
                                "BEGIN"
                                "INSERT INTO notification(user_id,title,description,link_id,link_type,is_read)"
                                "VALUES (SELECT id FROM user u WHERE u.id="
                                "(SELECT user_id FROM repository WHERE repository.id=r.source_id),"
                                "r.repo_name,CONCAT('forked by',(SELECT username FROM user WHERE user.id=r.user_id))"
                                ",r.id,'FORK',0);"
                                "END ",
            "createStarNotif" : "CREATE TRIGGER starNotification"
                                "AFTER INSERT ON star As s"
                                "FOR EACH ROW"
                                "BEGIN"
                                "INSERT INTO notification (user_id,title,description,link_id,link_type,is_read)"
                                "VALUES (SELECT user_id FROM repository r WHERE r.id=s.rep_id,"
                                "(SELECT repo_name FROM repository r WHERE r.id=s.rep_id ),"
                                "CONCAT('+1 for',SELECT name FROM repository r WHERE r.id=s.rep_id ),s.rep_id,'STAR',0);"
                                "END",

            "createWatchNotif" : "CREATE TRIGGER watchNotification"
                                 "AFTER INSERT ON watch As w"
                                 "FOR EACH ROW"
                                 "BEGIN"
                                 "INSERT INTO notification (user_id,title,description,link_id,link_type,is_read)"
                                 "VALUES (SELECT user_id FROM repository r WHERE r.id=w.rep_id,"
                                 "(SELECT repo_name FROM repository r WHERE r.id=s.rep_id ),"
                                 "CONCAT('+1 for',SELECT name FROM repository r WHERE r.id=sw.rep_id ),w.rep_id,'STAR',0);"
                                 "END"
        }

