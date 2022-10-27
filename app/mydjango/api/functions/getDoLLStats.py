import pandas


def calculateStats(data):
    numData = len(data)
    returnData = {
        "numSessions": len(data),
        "skillUsage": getSkillUsage(data),
        "topSkills": getTopSkills(data)
    }

    return returnData


def getSkillUsage(data):
    skillUsageStats = []

    for session in data:
        for skill in session['skillList']:
            skillName = skill['skillName']
            if len(skillUsageStats) > 0:
                skillFound = False
                for skillsIndex, skills in enumerate(skillUsageStats):
                    if skills['skillName'] == skillName:
                        skills['skillCount'] += 1
                        skills['matchXp'].append(session['xpTotal'])
                        skillFound = True
                        break
                if not skillFound:
                    skillUsageStats.append({
                        "skillName": skillName,
                        "skillCount": 1,
                        "matchXp": [session['xpTotal']]
                    })
            else:
                skillUsageStats.append({
                    "skillName": skillName,
                    "skillCount": 1,
                    "matchXp": [session['xpTotal']]
                })

    maxSkillCount = max(skill["skillCount"] for skill in skillUsageStats)

    for index, skill in enumerate(skillUsageStats):
        pandaXp = pandas.Series(skill['matchXp'])
        skillUsageStats[index]["quantiles"] = pandaXp.quantile(
            [0.75, 0.9, 0.95]).to_dict()
        powerScore = skillUsageStats[index]["quantiles"][0.95] * \
            (1 - .25*(1 - (skill["skillCount"] / maxSkillCount)))
        skillUsageStats[index]["powerScore"] = round(powerScore, 2)
        del skillUsageStats[index]["matchXp"]

    skillUsage = sorted(
        skillUsageStats, key=lambda k: k["powerScore"], reverse=True)
    return skillUsage


def getTopSkills(data):
    topUsageStats = []
    sortedData = sorted(data, key=lambda k: k["xpTotal"], reverse=True)[:20]
    for session in sortedData:
        for skill in session['skillList']:
            skillName = skill['skillName']
            if len(topUsageStats) > 0:
                skillFound = False
                for skillsIndex, skills in enumerate(topUsageStats):
                    if skills['skillName'] == skillName:
                        skills['skillCount'] += 1
                        skills['matchXp'].append(session['xpTotal'])
                        skillFound = True
                        break
                if not skillFound:
                    topUsageStats.append({
                        "skillName": skillName,
                        "skillCount": 1,
                        "matchXp": [session['xpTotal']]
                    })
            else:
                topUsageStats.append({
                    "skillName": skillName,
                    "skillCount": 1,
                    "matchXp": [session['xpTotal']]
                })

    maxSkillCount = max(skill["skillCount"] for skill in topUsageStats)

    for index, skill in enumerate(topUsageStats):
        pandaXp = pandas.Series(skill['matchXp'])
        topUsageStats[index]["quantiles"] = round(pandaXp.quantile(0.95), 2)
        powerScore = topUsageStats[index]["quantiles"] * \
            (1 - .25*(1 - (skill["skillCount"] / maxSkillCount)))

        skillScore = getSkillPowerScore(skill['skillName'])

        topUsageStats[index]["powerScore"] = round(powerScore, 2)
        topUsageStats[index]["skillScore"] = round(skillScore, 2)
        del topUsageStats[index]["matchXp"]

    topUsage = sorted(
        topUsageStats, key=lambda k: k["powerScore"], reverse=True)

    return topUsage


def getSkillPowerScore(skillName):
    distanceFactors = {
        "Orbit": 3.0,
    }
    skillData = {
        "skillName": "Snail Shell",
        "dps": 1.1,
        "healing" : {
            "hps": 0,
            "healType": "Lifesteal",
        },
        "sps": 0,
        "control": {
            "aim": "Self",
            "area": 1.0,
            "direction": "Orbit",
        },
        "cooldown": 1.2,
        "duration": 1.3,
        "distanceAxie": 3.0,
        "statusEffects": [],
        "knockback": {
            "amount": 1.5,
            "instancesPerSecond": 5 
        },
        "scaleFactor": 2.0,
    }
    directionFactor = distanceFactors[skillData["control"]["direction"]]
    damageFactor = skillData['dps'] * directionFactor * skillData["control"]['area']
    healFactor = skillData['healing']['hps'] * getHealTypeFactor(skillData["healing"]['healType'], skillData['dps'])
    shieldFactor = skillData['sps']
    statusEffectFactor = getStatusEffectFactor(skillData['statusEffects'])
    knockbackFactor = getKnockbackFactor(skillData['knockback'], skillData['control'] )
    extraFactor = 1*skillData['scaleFactor']*skillData['distanceAxie']
    
    skillScore = damageFactor + healFactor + shieldFactor + statusEffectFactor + knockbackFactor
    return skillScore
    
def getHealTypeFactor(healType, dps):
    if(healType == "Lifesteal"):
        return dps
    
def getStatusEffectFactor(statusEffects):
    return 0

def getKnockbackFactor(knockback, control):
    directionFactor = {
        "Orbit": 3.0,
    }
    knockbackFactor = knockback["amount"] * knockback["instancesPerSecond"] * control["area"] * directionFactor[control["direction"]]
    return knockbackFactor