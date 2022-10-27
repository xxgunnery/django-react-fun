
def getGameVersionInt(gameVersion):
    if gameVersion is not None:
        if gameVersion == "1.1.3A":
            return 113.1
        return float(gameVersion.replace('.', ''))
    else:
        return 0