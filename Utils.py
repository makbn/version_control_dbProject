from models import  User


class UIHelper:
    @staticmethod
    def backPressHandler(name,Parent=None):
        from ui import SplashWidget
        from ui import NewLogin
        from ui import RegisterPage
        from ui import DashbordWidget
        if name=="SplashWidget":
            return SplashWidget.SplashWidget(Parent)
        elif name=="NewLoginWidget":
            return NewLogin.NewLoginWidget(Parent)
        elif name=="RegisterPage":
            return RegisterPage.RegisterPage(Parent)
        else:
            return DashbordWidget.DashboardWidget(Parent)
class UserManager:
    @staticmethod
    def getCurrentUser():
        return User.USER_TEST