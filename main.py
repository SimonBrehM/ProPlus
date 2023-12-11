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
    """Function that returns the period we want, coming from a number"""
    return client.periods[n-1]
    # type : object

def calc_avg_subject(trim:int):
    """"Calculates the average of the student on every subject for an certain period"""
    trim = trimestre(trim)
    coefficients = {}
    averages = {}
    # averages = {subject : grade out of 20}
    for grade in trim.grades:
        if grade.subject.name in averages:
            averages[grade.subject.name] += (float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient)
            coefficients[grade.subject.name] += float(grade.coefficient)
        else:
            averages[grade.subject.name] = (float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient)
            coefficients[grade.subject.name] = float(grade.coefficient)
    for key in averages.keys():
        averages[key] = round(averages[key] / coefficients[key],2)
    return averages
    # type : dict



def calc_overall_avg(trim:int):
    """Calculates the overall average of the student for a certain period"""
    overall_avg = 0
    for moy in calc_avg_subject(trim).values():
        overall_avg += moy
    return round(overall_avg / len(calc_avg_subject(trim)), 2)
    # type : float

def matieres():
    """Returns all the subjects in a list"""
    subjects = []
    for x in trimestre(1).grades:
        if x.subject.name not in subjects:    
            subjects.append(x.subject.name)
    return subjects
    # type : list

def grades_specs(trim:int):
    """Returns a dictionnary of a bunch a specificities on every grade for every subject"""
    notes_dict = {}
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool]}
    for grade in trimestre(trim).grades:
        if grade.subject.name in notes_dict:
            notes_dict[grade.subject.name] += [float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) >calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")) ]
        else:
            notes_dict[grade.subject.name] = [float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) >calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")) ]
    return notes_dict
    # type : dict

