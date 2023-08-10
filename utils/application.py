from DBManager.UserInfo import UserRegist, UserLogin



def Application(environ, start_response):

    method = environ["REQUEST_METHOD"]
    path = environ["PATH_INFO"]

    if path == "/api/regist" and method == "POST":
        return UserRegist(request)
    if path == "/api/login" and method == "POST":
        return UserLogin(request)