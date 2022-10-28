import sys
from django.http import HttpResponse
from pathlib import Path
import json
from .functions.utils import getGameVersionInt
from .functions.getDoLLStats import calculateStats

# cd app/mydjango && python manage.py runserver
# Create your views here.
BASE_DIR = Path(__file__).resolve().parent.parent

def index(request):
    return HttpResponse("Welcome to the DoLL Django Gamesession API")

def getGameSessionData(request):
    print('--------STARTING GAME SESSIONS----------')
    version = request.GET.get('version')
    
    with open('static/gamesessions2.json') as f:
        data = json.load(f)
        
    if version is not None:
        data = list(filter(lambda x: x['version'] == version, data))
        print("FILTERED DATA", len(data))

    print("data loaded", len(data))

    return HttpResponse(json.dumps(data))

def getDoLLStats(request):
    print('--------STARTING DoLL Stats----------')
    
    version = request.GET.get('version')
    
    with open('static/gamesessions2.json') as f:
        data = json.load(f)
        
    if version is not None:
        data = list(filter(lambda x: x['version'] == version, data))
        print("FILTERED DATA", len(data))
    
    data = calculateStats(data)
    
    return HttpResponse(json.dumps(data))


def getGameVersions(request):
    print('--------STARTING DoLL Game Versions----------')
    
    return HttpResponse(json.dumps(data))

def change(request):
    print('------------------')
    print('loading data...')

    with open(str(BASE_DIR) + '\static\gamesessions.json') as f:
        data = json.load(f)

    print("data loaded", len(data))

    popList = []
    for sessionkey, gamesession in enumerate(data):
        if sessionkey % 100 == 0:
            print("sessionKey", sessionkey)
        if gamesession.get('version') is not None:
            if getGameVersionInt(gamesession['version']) < 112:
                if sessionkey not in popList:
                    popList.append(sessionkey)
            else:
                del gamesession['_id']
                if gamesession.get('shieldCreditConsumed') is not None:
                    del gamesession['shieldCreditConsumed']
                if gamesession.get('axies') is not None:
                    del gamesession['axies']

                if gamesession.get('sidekick') is not None:
                    del gamesession['sidekick']
                if gamesession.get('skillList') is not None:
                    if len(gamesession.get('skillList')) == 0:
                        if sessionkey not in popList:
                            popList.append(sessionkey)
                    else:
                        for skillkey, skill in enumerate(gamesession['skillList']):
                            for levelKey, levelData in enumerate(skill['skillData']):
                                if levelData['skillTime'] == -1 and levelKey == 0:
                                    print("WE HERE 1")
                                    print("skillkey", skillkey, skill)
                                    levelData['skillData'] = []
                                    break
                                elif levelData['skillTime'] == -1:
                                    del skill['skillData'][levelKey:len(
                                        levelData)]
                                    break
                                elif len(levelData) == 0:
                                    del gamesession[skillkey]
                                    break
        else:
            if sessionkey not in popList:
                popList.append(sessionkey)

    print("POPPING", len(popList))
    for sessionkey in reversed(popList):
        data.pop(sessionkey)

    print("data", len(data))

    with open(str(BASE_DIR) + '\static\gamesessions2.json', 'w') as f:
        json.dump(data, f)

    return HttpResponse("Data has been changed")


def getUserData(request):
    print('--------STARTING USER DATA----------')
    version1 = request.GET.get('version1')
    version2 = request.GET.get('version2')
    user = request.GET.get('user')
    
    print("version", version1, version2)
    print("user", user)
    
    with open('static/gamesessions.json') as f:
        data = json.load(f)
        
    def checkUser(gamesession, user):
        if gamesession.get('user') is not None:
            if gamesession['user']['username'] == user:
                return True
            else:
                return False
        else:
            return False
    
    def checkVersion(gamesession, version):
        if gamesession.get('version') is not None:
            if gamesession['version'] == version:
                return True
            else:
                return False
        else:
            return False
        
    if all(data is not None for item in [user, version1, version2]):
        print("Data is not none!")
        data = list(filter(lambda x: checkUser(x,user) and (checkVersion(x, version1) or checkVersion(x, version2)) , data))
        print("FILTERED DATA", len(data))
    else:
        print("NO VERSION OR USER")
        return HttpResponse("NO VERSION OR USER")
    
    with open('static/gamesessions' + user + '.json', 'w') as f:
        json.dump(data, f)

    print("data loaded", len(data))

    return HttpResponse("Data has been changed")