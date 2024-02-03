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

def get_current_period():
    return client.current_period.name

def trimestre(n:int):
    """
    Function that returns the period we want, coming from a number
    """
    return client.periods[n-1]
    # type : object

def note_20(grade : object):
    """
    Returns the grade out of 20
    """
    return ((float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient))
    # type : float

def calc_avg_subject(trim:int):
    """
    Calculates the average of the student on every subject for an certain period
    """
    trim = trimestre(trim)
    optionnal = {}
    optionnal_coeff = {}
    coefficients = {}
    averages = {}
    # averages = {subject : grade out of 20}
    # coefficients = {subject : sum of coefficients}
    for grade in trim.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            if grade.subject.name not in averages:
                averages[grade.subject.name] = grade.grade
                coefficients[grade.subject.name] = grade.coefficient
        elif grade.is_optionnal:
            if grade.subject.name in optionnal:
                optionnal[grade.subject.name] += note_20(grade)
                optionnal_coeff[grade.subject.name] += float(grade.coefficient)
            else:
                optionnal[grade.subject.name] = note_20(grade)
                optionnal_coeff[grade.subject.name] = float(grade.coefficient)
        elif grade.subject.name in averages and averages[grade.subject.name] not in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            if grade.is_bonus and note_20(grade)>10:
                averages[grade.subject.name] += note_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
            elif grade.is_bonus == False:
                averages[grade.subject.name] += note_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
        else:
            if grade.is_bonus and note_20(grade)>10:
                averages[grade.subject.name] = note_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
            elif grade.is_bonus == False:
                averages[grade.subject.name] = note_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
    if optionnal != {}:
        for key in optionnal.keys():
            if key not in averages.keys():
                averages[key] = optionnal[key]
                coefficients[key] = optionnal_coeff[key]
            elif optionnal[key] > round(averages[key] / coefficients[key],2):
                averages[key] += optionnal[key]
                coefficients[key] += optionnal_coeff[key]
    for key in averages:
        if averages[key] not in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            averages[key] = round(averages[key] / coefficients[key],2)
    return averages, coefficients
    # type : dict

def calc_avg_overall(trim:int):
    """
    Calculates the overall average of the student for a certain period
    """
    overall_avg = 0
    for moy in calc_avg_subject(trim)[0].values():
        if moy not in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            overall_avg += moy
    return round(overall_avg / len(calc_avg_subject(trim)[0]), 2)
    # type : float


def anal_subjects(sbj_list:list):
    sbj_dico = {
        "ABIBAC HG" : "ABIBAC HG",
        "ACL" : "ACL",
        "HG BFI ITALOPHONE" : "HG ITALIEN",
        "HG POLO" : "HG POLONAIS",
        "HG BRITANNIQUE" : "HG BRITISH",
        "CDM" : "CDM",
        "HIST.GEO.EDUC.CIVIQ." : "HISTOIRE-GEO",
        "ANGLAIS EURO" : "ANGLAIS EURO",
        "ALLEMAND EURO" : "ALLEMAND EURO",
        "LITT. ANGLAIS" : "ANGLAIS",
        "MATHEMATIQUES" : "MATHS",
        "SCIENCES VIE & TERRE" : "SVT",
        "SC. ECONO.& SOCIALES" : "SES",
        "HIST.GEO.GEOPOL.S.P." : "HGGSP",
        "NUMERIQUE SC. INFORM." : "NSI",
        "PHYSIQUE-CHIMIE" : "PHYSIQUE-CHIMIE",
        "EDUCATION MUSICALE" : "MUSIQUE",
        "ITALIEN LV3" : "ITALIEN LV3",
        "ESPAGNOL LV3" : "ESPAGNOL LV3",
        "ARABE LV3" : "ARABE LV3",
        "FRANCAIS" : "FRANCAIS",
        "ENSEIGN SCIENTIFIQUE SPC" : "ES PC",
        "ENSEIGN.SCIENTIFIQUE SVT" : "ES SVT",
        "ALLEMAND LV2" : "ALLEMAND LV2",
        "LL ABIBAC" : "LL ABIBAC",
        "ANGLAIS LV1" : "ANGLAIS LV1",
        "DNL ANGLAIS SVT" : "DNL SVT",
        "HG BFI ARABOPHONE" : "HG ARABE",
        "HIST.GEO AMERICAINE" : "",
        "HLPHI O" : "",
        "ANGLAIS LV2" : "",
        "ACCOMPAGNEMENT. PERSO" : "",
        "DNL ALL" : "",
        "HG ESP" : "",
        "DNL ANGLAIS" : "",
        "MATHS" : "",
        "ED.PHYSIQUE & SPORT." : "",
        "HG PORT." : "",
        "Soutien LLCE" : "",
        "ACCOMPAGNEMT. PERSO" : "",
        "MATHS CHINOIS" : "",
        "CHINOIS LV3" : "",
        "FRANCAIS LANGUE SECONDE" : "",
        "DRAMA" : "",
        "LL PORTUGAISE" : "",
        "LL ESPAGNOLE" : "",
        "LL JAPONAISE" : "",
        "LL AROBOPHONE" : "",
        "LL ANGLOPHONE" : "",
        "HG SEC. ANGLOPHONE" : "",
        "ACCO PERSO FRANC" : "",
        "HG JAPO" : "",
        "ACCO PERSO MATH" : "",
        "SC.NUMERIQUE.TECHNOL." : "",
        "DS commun Maths" : "",
        "LL CHINOIS" : "",
        "HG ARABOPHONE" : "",
        "LL ITALIENNE" : "",
        "HG ITALIENNE" : "",
        "LITTERAT. LCA LATIN" : "",
        "LCA LATIN" : "",
    }
    
    return sbj_list

def get_subjects(trim:int):
    """
    Returns all the subjects in a list
    """
    subjects = []
    for x in trimestre(trim).grades:
        if x.subject.name not in subjects:    
            subjects.append(x.subject.name)
    return subjects 
    # type : list

def anal_grades(trim:int):
    """
    Returns a dictionnary of a bunch a specificities on every grade for every subject
    """
    notes_dict = {} ; period = trimestre(trim)
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, class average : float, subject name : str, period name : str]}
    for grade in period.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            if grade.subject.name in notes_dict:
                notes_dict[grade.subject.name] += [[grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
            else:
                notes_dict[grade.subject.name] = [[grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        elif grade.subject.name in notes_dict:
            notes_dict[grade.subject.name] += [[float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, 'class="contributes"' if float(grade.grade.replace(",",".")) > calc_avg_subject(trim)[0][grade.subject.name] else 'class="not_contributes"', float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        else:
            notes_dict[grade.subject.name] = [[float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, 'class="contributes"' if float(grade.grade.replace(",",".")) > calc_avg_subject(trim)[0][grade.subject.name] else 'class="not_contributes"', float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
    return notes_dict
    # type : dict

def convert_to_100(grade:float, out_of:float):
    """"
    Returns the parameter (a grade) into a grade out of 100
    """
    return round(grade / out_of * 100,2)
    # type : float

def calc_avg_evol(avg_old:float,avg_new:float):
    return round((avg_new-avg_old)/avg_old * 100, 2)
    # type : float

def get_periods():
    global client
    periodes = {} ; n=0
    for period in client.periods:
        n+=1
        periodes[period.name] = (n)
    return periodes
