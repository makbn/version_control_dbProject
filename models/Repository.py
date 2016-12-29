from random import randint

import Database


class Repository:

    def __init__(self,id,name,desc,isPrivate,isForked,owner_id,date,source_id=-1):
        self.id=id
        self.name=name
        self.description=desc
        self.isPrivate=isPrivate
        self.isForked=isForked
        self.ownerId=owner_id
        self.date=date
        self.sourceId=source_id
    def getStarCount(self):

        return randint(5,50) # TODO: should connect to DB

    def getSourceRepository(self):
        if self.isForked==True:
            #source=Database.getEntityByKey(id=self.sourceId)
            return REPOSITORY_TEST # TODO : should connect To db
        else:
            return None

    def getSourceRepositoryName(self):
        if self.isForked==True:
            return self.getSourceRepository().name
        else:
            return "NULL"

    def getOwner(self):
        user=Database.getEntityByKey(id=self.ownerId)
        return user
REPOSITORY_TEST=Repository(123,"angular","some bullshit for describe this bullshit",False,False,123,"2016-12-21")
