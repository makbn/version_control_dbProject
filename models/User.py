

class User:

    def __init__(self,id,username,firstName,lastName,email,gender,birthday):
        self.id=id
        self.username=username
        self.firstName=firstName
        self.lastName=lastName
        self.email=email
        self.gender=gender
        self.birthday=birthday


    def getId(self):
        return self.id
    def getUsername(self):
        return self.username
    def getFirstName(self):
        return self.firstName
    def getLastName(self):
        return self.lastName
    def getEmail(self):
        return self.email
    def getGender(self):
        return self.gender
    def getBirthday(self):
        return self.birthday

USER_TEST=User(123,"makbn","mehdi","akbarian","mehdi74akbarian@gmail.com","1","1996-01-25")

