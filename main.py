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

def get_id():
  """Returns the 2 inputs of the user : their id and their password""""
  u_id = input("Entrez votre identifiant :  ")
  u_pwd = input("Entrez votre mot de passe :  ")
  return [u_id, u_pwd]

with open("uids.txt") as file:
  lines = file.readlines()
  
with open("uids.txt", "a") as file:
  if lines == []:
    u_ids = get_id()
    file.write(f"{u_ids[0]} \n {u_ids[1]}")
  else:
    u_ids = []
    for line in lines:
      u_ids.append(line.strip())


client = pronotepy.Client('https://0693446w.index-education.net/pronote/eleve.html',
                      username = u_ids[0],
                      password = u_ids[1],
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
        if grade.grade in ["Absent","NonNote","Inapte","NonRendu"]:
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

def calc_overall_avg(trim:int):
    """Calculates the overall average of the student for a certain period"""
    overall_avg = 0
    subject_avg = calc_avg_subject(trim)
    for avg in subject_avg.values():
        overall_avg += avg
    return round(overall_avg / len(subject_avg), 2)
    # type : float


def matieres():
    """Returns all the subjects in a list"""
    subjects = []
    for grade in trimestre(1).grades:
        if grade.subject.name not in subjects:    
            subjects.append(grade.subject.name)
    return subjects
    # type : list

def grades_specs(trim:int):
    """Returns a dictionnary of a bunch a specificities on every grade for every subject"""
    notes_dict = {}
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, is grade optionnal : bool, is grade bonus : bool]}
    for grade in trimestre(trim).grades:
        if grade.grade in ["Absent","NonNote","Inapte","NonRendu"]:
            if grade.subject.name in notes_dict:
                notes_dict[grade.subject.name].append([grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, grade.is_optionnal, grade.is_bonus])
            else:
                notes_dict[grade.subject.name] = [[grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, grade.is_optionnal, grade.is_bonus]]
        elif grade.subject.name in notes_dict:
            notes_dict[grade.subject.name].append([float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) > calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) > float(grade.average.replace(",",".")), grade.is_optionnal, grade.is_bonus])
        else:
            notes_dict[grade.subject.name] = [[float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, float(grade.grade.replace(",",".")) > calc_avg_subject(trim)[grade.subject.name], float(grade.grade.replace(",",".")) > float(grade.average.replace(",",".")), grade.is_optionnal, grade.is_bonus]]
    return notes_dict
    # type : dict

