#La casa de Hugo

import pronotepy
from pronotepy.ent import ent_auvergnerhonealpe
# importing ent specific function, you do not need to import anything if you dont use an ent

client = pronotepy.Client('https://0693446w.index-education.net/pronote/eleve.html',
                      username='h.camarasabira',
                      password='Patat0_Val2',
                      ent=ent_auvergnerhonealpe) # ent specific

if not client.logged_in:
    exit(1)  # the client has failed to log in

# print all the grades the user had in this school year
for period in client.periods:
    # Iterate over all the periods the user has. This includes semesters and trimesters.
    pass
    # for grade in period.grades: # the grades property returns a list of pronotepy.Grade
    #     print(grade.subject.name,grade.grade) # This prints the actual grade. Could be a number or for example "Absent" (always a string)
    # print(period.name)

def trimestre(n):
    period_list = []
    for period in client.periods:
        period_list.append(period)
    return period_list[n-1]

def calcul_moy_matiere(trim):
    trim = trimestre(trim)
    grades = []
    moyennes = {} # subject : average
    for grade in trim.grades:
        moyennes[grade.subject.name.replace(" ","_")]=float(grade.grade.replace(",",".")) + moyennes[grade.subject.name]
    return moyennes

print(calcul_moy_matiere(1))

# def calc_moy_generale(trim):
    
#     return float

