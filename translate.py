import json

sourceDir = input('Please enter the path to the Steam Common folder where Tale of Immortal is installed (format: [Drive]:\\path\\to\\steamapps\\common): ')
sourceDir = sourceDir.strip('\\').strip('/')
localtextPath = '\鬼谷八荒\Mod\modFQA\配置修改教程\配置（只读）Json格式\LocalText.json'

localTextFile = open(sourceDir + localtextPath, 'r')
localTextJson = json.load(localTextFile)

def getTextTranslation(textCh: str):
    items = [x for x in localTextJson if x['ch'] == textCh]
    for item in items:
        if item['en'] != '' and item['en'] != textCh:
            item['en'] = item['en'].replace('\\', '')
            return item['en']
        
    return ''


def getIdTranslation(key: str, id: str) -> str:
    id = id.strip('\ufeff') #Strip ZWNBSP
    item = [x for x in localTextJson if x['key'] == key + str(id)]
    
    if item.__len__() == 0:
        item = {}
        prefix = key.split('_')[key.split('_').__len__()-1]
        item['en'] = f'{prefix}_{id}'
    else:
        item = item[0]

    text:str = item['en']
    text = text.replace('\\', '')
    return text


def readFile(filename: str, key: str, idPos: int = 0, multipropSeparator: str = ''):
    data = []
    with open(filename, "r") as file:
        for line in file:
            line = line.strip('\n')
            lineProps = []
            if (multipropSeparator != ''):
                lineProps = line.split(multipropSeparator)
            else:
                lineProps.append(line)

            newLine = ''
            for prop in lineProps:
                id = prop.split(',')[idPos]
                text = getIdTranslation(key, id)
                newProp = prop.split(',')
                newProp[idPos+1] = text
                newLine += ','.join(newProp) + multipropSeparator
            
            newLine = newLine.strip(multipropSeparator)
            data.append(newLine)
    
    return data


def translateById(filename: str, key: str, idPos: int = 0, multipropSeparator: str = ''):
    print(f'Translating {filename}...', end='')
    
    data = readFile(filename, key, idPos, multipropSeparator)
    with open(filename, 'w') as file:
        file.write('\n'.join(data))

    print('Done')
    return


def translateSkills(prop: dict, textIdx: int):
    if (prop[textIdx].__len__() > 1):
        weapon, skill = prop[textIdx].split('-')
        translatedWeapon = getTextTranslation(weapon)
        translatedSkill = getTextTranslation(skill)
        prop[textIdx] = translatedWeapon+'-'+translatedSkill
    else:
        name = prop[textIdx]
        translatedName = getTextTranslation(name)
        prop[textIdx] = translatedName
        
    return prop


def translateByText(filename:str, textIdx: int = 1):
    print(f'Translating {filename}...', end='')
    data = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('\n')
            prop = line.split(',')
            if filename == 'SkillID.csv':
                prop = translateSkills(prop, textIdx)
            else:
                text = prop[textIdx]
                translatedText = getTextTranslation(text)
                prop[textIdx] = translatedText
            data.append(','.join(prop))

    with open(filename, 'w') as file:
        file.write('\n'.join(data))

    print('Done')
    return


def translateStatusIds(filename: str):
    print(f'Translating {filename}...', end='')
    data = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip('\n')
            prop = line.split(',')
            prop[1] = getIdTranslation('role_feature_postnatal_name', prop[0])
            prop[2] = getIdTranslation('role_feature_postnatal_tips', prop[0])
            data.append(','.join(prop))

    with open(filename, 'w') as file:
        file.write('\n'.join(data))

    print('Done')
    return


print("Translating...")
translateById('AddLuckIDs.csv', 'role_feature_postnatal_name', multipropSeparator='|')
translateById('AddLuckDescIDs.csv', 'role_feature_postnatal_tips')
translateById('HobbyIDs.csv', 'role_hobby_name')
translateById('ItemIDs.csv', 'item_name')
translateById('LuckIDs.csv', 'role_feature_congenital_name')
translateByText('NamingIDs.csv', 2)
translateByText('SchoolFateIDs.csv')
translateByText('SchoolSloganIDs.csv', 2)
translateByText('SkillID.csv', 2)
translateStatusIds('StatusIDs.csv')
translateById('TaoistHeartIDs.csv', 'TaoistHeartName')
translateById('TaoistTitleIDs.csv', 'AppellationTitleName')
translateById('TrailIDs.csv', 'role_character_name')
print("Translating complete!")