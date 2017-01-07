#updates user list only when the form is being rendered
#maintains both a dict and a list for easy access
from django.contrib.auth.models import User

_userList = []
_userDict = {}
_userTuple = []

def update():
    global _userList
    global _userDict
    global _userTuple
    _userList = User.objects.filter(is_active=True).order_by('username')
    print _userList
    _userDict = dict((x.username, x) for x in _userList)
    _userTuple = [(x, x.username + ": " +  x.first_name + ' ' + x.last_name) for x in _userList]


def getUserList():
    return _userList

def getUserTuple():
    return _userTuple

def getUserDictionary():
    return _userDict





