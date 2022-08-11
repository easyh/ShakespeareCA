import re 
import pandas as pd

textfile = f'data/ado.txt'

def readText(filename):
    text = open(filename, 'r')
    text = text.read()
    return text

def cleanText(text):
    text = re.sub('\W+', ' ',text)
    text = re.sub('LEONATO S BROTHER', 'LEONATOBROTHER', text)
    text = re.sub('DON JOHN', 'DONJOHN', text)
    text = re.sub('FIRST WATCHMAN', 'FIRSTWATCHMAN', text)
    text = re.sub('SECOND WATCHMAN', 'SECONDWATCHMAN', text)
    text = re.sub('Scene 1', 'scene', text)
    text = re.sub('Scene 2', 'scene', text)
    text = re.sub('Scene 3', 'scene', text)
    text = re.sub('Scene 4', 'scene', text)
    text = re.sub('Scene 5', 'scene', text)
    text_list = text.split()    
    return text_list 


def characters(text_list):
    character_list = ["scene", "LEONATO", "LEONATOBROTHER", "HERO", "BEATRICE", "MARGARET", "URSULA", "PRINCE", "CLAUDIO", "BENEDICK", "BALTHASAR", "ANTONIO", "DONJOHN", "BORACHIO", "CONRADE", "DOGBERRY", "VERGES", "SEACOAL", "FIRSTWATCHMAN", "SECONDWATCHMAN", "SEXTON", "FRIAR", "MESSENGER", "BOY"]
    character_order = []
    for character in text_list: 
        if character in character_list:
            character_order.append(character)
    return character_order

def characterInteractions(character_order):

    interactions = {}
    for i in range(len(character_order)-1): #bis zum vorletzten Wort (damit es noch ein Paar gibt)
        firstWord=character_order[i]#erstes Wort des Wortpaares ist auf Position i
        secondWord=character_order[i+1] #zweites Wort des Wortpaares 
        if (len(firstWord)>0 and len(secondWord)>0): 
            if not firstWord in interactions: 
                interactions[firstWord]={}
            if not secondWord in interactions[firstWord]:
                interactions[firstWord][secondWord]=0
            if secondWord in interactions[firstWord]:
                interactions[firstWord][secondWord]+=1

     print(interactions)           
  
    df = pd.DataFrame.from_dict(interactions)
    df = df.sort_index(axis=1)
    df = df.sort_index(axis=0)
    df = df.drop("scene",axis=1)
    df = df.drop("scene",axis=0)
    print(df)
    df.to_csv(f'data/ADO_interactions.csv', index=True)

def main(textfile):
    text=readText(textfile)
    text_list=cleanText(text)
    character_order=characters(text_list)
    text_list=characterInteractions(character_order)


main(textfile)