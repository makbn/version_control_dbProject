from models import  User



class UIHelper:
    @staticmethod
    def backPressHandler(name,Parent=None):
        from ui import SplashWidget
        from ui import NewLogin
        from ui import RegisterPage
        from ui import DashbordWidget
        from ui import SearchPage
        from ui import ProfileWidget
        if name=="SplashWidget":
            return SplashWidget.SplashWidget(Parent)
        elif name=="NewLoginWidget":
            return NewLogin.NewLoginWidget(Parent)
        elif name=="RegisterPage":
            return RegisterPage.RegisterPage(Parent)
        elif name=="SearchPage":
            return SearchPage.SearchPage(Parent)
        elif name=="ProfileWidget":
            return ProfileWidget.ProfileWidget(Parent)
        else:
            print(name+ "sth wrong")
            return DashbordWidget.DashboardWidget(Parent)
class UserManager:
    current_user = None

    @staticmethod
    def setCurrentUser(user):
        UserManager.current_user = user

    @staticmethod
    def resetUser():
        UserManager.current_user=None


    @staticmethod
    def getCurrentUser():
        return UserManager.current_user