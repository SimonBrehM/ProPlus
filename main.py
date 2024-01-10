#  ▄▄▄     ▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄    ▄▄▄▄▄▄  ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
# █   █   █      █  █       █      █       █      █  █      ██       █  █  █ █  █  █ █  █       █       █
# █   █   █  ▄   █  █       █  ▄   █  ▄▄▄▄▄█  ▄   █  █  ▄    █    ▄▄▄█  █  █▄█  █  █ █  █   ▄▄▄▄█   ▄   █
# █   █   █ █▄█  █  █     ▄▄█ █▄█  █ █▄▄▄▄▄█ █▄█  █  █ █ █   █   █▄▄▄   █       █  █▄█  █  █  ▄▄█  █ █  █
# █   █▄▄▄█      █  █    █  █      █▄▄▄▄▄  █      █  █ █▄█   █    ▄▄▄█  █   ▄   █       █  █ █  █  █▄█  █
# █       █  ▄   █  █    █▄▄█  ▄   █▄▄▄▄▄█ █  ▄   █  █       █   █▄▄▄   █  █ █  █       █  █▄▄█ █       █
# █▄▄▄▄▄▄▄█▄█ █▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█▄█ █▄▄█  █▄▄▄▄▄▄██▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█


import pronotepy
from pronotepy.ent import ent_auvergnerhonealpe
# importing ent specific function, you do not need to import anything if you dont use an ent

client = None

def get_data(username, password):
    global client
    client = pronotepy.Client('https://0693446w.index-education.net/pronote/eleve.html',
                        username=username,
                        password=password,
                        ent=ent_auvergnerhonealpe) # ent specific

    if not client.logged_in:
        exit(1)  # the client has failed to log in

def trimestre(n:int):
    """Function that returns the period we want, coming from a number"""
    return client.periods[n-1]
    # type : object

def note_20(grade : object):
    """Returns the grade out of 20"""
    return ((float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient))
    # type : float

def calc_avg_subject(trim:int):
    """"Calculates the average of the student on every subject for an certain period"""
    trim = trimestre(trim)
    bonus = {}
    coefficients = {}
    averages = {}
    # averages = {subject : grade out of 20}
    for grade in trim.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu"):
            pass
        elif grade.is_bonus:
            if grade.subject in bonus:
                bonus[grade.subject.name] += note_20(grade)
            else:
                bonus[grade.subject.name] = note_20(grade)
        elif grade.subject.name in averages:
            if grade.is_optionnal and note_20(grade)>10:
                averages[grade.subject.name] += note_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
            elif grade.is_optionnal == False:
                averages[grade.subject.name] += note_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
            else:
                pass
        else:
            if grade.is_optionnal and note_20(grade)>10:
                averages[grade.subject.name] = note_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
            elif grade.is_optionnal == False:
                averages[grade.subject.name] = note_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
            else:
                pass
    if bonus != {}:
        for key in bonus.keys():
            if bonus[key] > round(averages[key] / coefficients[key],2):
                averages[key] += bonus[key]
            else:
                pass
    for key in averages.keys():
        averages[key] = round(averages[key] / coefficients[key],2)
    return averages
    # type : dict

def calc_avg_overall(trim:int):
    """Calculates the overall average of the student for a certain period"""
    overall_avg = 0
    subject_avg = calc_avg_subject(trim)
    for avg in subject_avg.values():
        overall_avg += avg
    return round(overall_avg / len(subject_avg), 2)
    # type : float


def get_subjects(trim:int):
    """Returns all the subjects in a list"""
    subjects = []
    for x in trimestre(trim).grades:
        if x.subject.name not in subjects:    
            subjects.append(x.subject.name)
    return subjects 
    # type : list

def grades_specs(trim:int):
    """Returns a dictionnary of a bunch a specificities on every grade for every subject"""
    notes_dict = {} ; period = trimestre(trim)
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, class average : float, subject name : str, period name : str]}
    for grade in period.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu"):
            if grade.subject.name in notes_dict:
                notes_dict[grade.subject.name] += [grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]
            else:
                notes_dict[grade.subject.name] = [grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]
        elif grade.subject.name in notes_dict:
            notes_dict[grade.subject.name] += [float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) >calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]
        else:
            notes_dict[grade.subject.name] = [float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) >calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]
    return notes_dict
    # type : dict

def convert_to_100(grade:float, out_of:float):
    """"Returns the parameter (a grade) into a grade out of 100"""
    return round(grade / out_of * 100,2)
    # type : float

def calc_avg_evol(avg_old:float,avg_new:float):
    return round((avg_new-avg_old)/avg_old * 100, 2)
    # type : float

def get_periods():
    global client
    global periods
    periodes = {} ; n=0
    for period in client.periods:
        periodes[period.name] = (n+1)
    return periodes
