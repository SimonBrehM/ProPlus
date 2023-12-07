#La casa de Hugo

import pronotepy
from pronotepy.ent import ent_auvergnerhonealpe
# importing ent specific function, you do not need to import anything if you dont use an ent

client = pronotepy.Client('https://0693446w.index-education.net/pronote/eleve.html',
                      username='h.camarasabira',
                      password='X',
                      ent=ent_auvergnerhonealpe) # ent specific

if not client.logged_in:
    exit(1)  # the client has failed to log in


def trimestre(n:int):
    """Function that selects the period we want, coming from a number"""
    period_list = []
    # list of all the periods
    for period in client.periods:
        period_list.append(period)
    return period_list[n-1]
    # return of the desired period ([n-1] because first index is 0)

def calcul_moy_matiere(trim:int):
    """"Calculates the average of the student on every subject for an certain period"""
    trim = trimestre(trim)
    # selection of the desired period thanks to the function trimestre
    coefficients = {}
    # dictionnary of the coefficients of every subject (coefficients[subject.name] = sum_of_all_coefficients_of_all_grades_from_one_subject)
    moyennes = {}
    # dictionnary of the grades of every subject (moyennes[subject.name] = sum(actual_grade * grade_coefficient))
    for grade in trim.grades:
    # go through every single grade of the student
        if grade.subject.name in moyennes:
        # checks if there is already a grade for this subject
            moyennes[grade.subject.name] += (float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient)
            # grade writting style : "18,5", changing it to "18.5" to convert to float | grade may not be out of 20 so putting out of 20
            coefficients[grade.subject.name] += float(grade.coefficient)
        else:
            moyennes[grade.subject.name] = (float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient)
            coefficients[grade.subject.name] = float(grade.coefficient)
    for key in moyennes.keys():
    # go through every key in the dictionnary
        moyennes[key] = round(moyennes[key] / coefficients[key],2)
        # calculate the average in every subject and put it in the dictionnary
    return moyennes
    # type : dict


def calcul_moy_generale(trim:int):
    """Calculates the overall average of the student for a certain period"""
    moyenne_g = 0
    # sum of all the averages in every subject
    for moy in calcul_moy_matiere(trim).values():
        moyenne_g += moy
    return round(moyenne_g / len(calcul_moy_matiere(trim)), 2)
    # type : float

