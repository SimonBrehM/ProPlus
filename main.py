#  ▄▄▄     ▄▄▄▄▄▄    ▄▄▄▄▄▄▄ ▄▄▄▄▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄    ▄▄▄▄▄▄  ▄▄▄▄▄▄▄    ▄▄   ▄▄ ▄▄   ▄▄ ▄▄▄▄▄▄▄ ▄▄▄▄▄▄▄ 
# █   █   █      █  █       █      █       █      █  █      ██       █  █  █ █  █  █ █  █       █       █
# █   █   █  ▄   █  █       █  ▄   █  ▄▄▄▄▄█  ▄   █  █  ▄    █    ▄▄▄█  █  █▄█  █  █ █  █   ▄▄▄▄█   ▄   █
# █   █   █ █▄█  █  █     ▄▄█ █▄█  █ █▄▄▄▄▄█ █▄█  █  █ █ █   █   █▄▄▄   █       █  █▄█  █  █  ▄▄█  █ █  █
# █   █▄▄▄█      █  █    █  █      █▄▄▄▄▄  █      █  █ █▄█   █    ▄▄▄█  █   ▄   █       █  █ █  █  █▄█  █
# █       █  ▄   █  █    █▄▄█  ▄   █▄▄▄▄▄█ █  ▄   █  █       █   █▄▄▄   █  █ █  █       █  █▄▄█ █       █
# █▄▄▄▄▄▄▄█▄█ █▄▄█  █▄▄▄▄▄▄▄█▄█ █▄▄█▄▄▄▄▄▄▄█▄█ █▄▄█  █▄▄▄▄▄▄██▄▄▄▄▄▄▄█  █▄▄█ █▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█▄▄▄▄▄▄▄█


import pronotepy
from pronotepy.ent import ent_auvergnerhonealpe
from math import floor
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

def trimester(n:int):
    """
    Function that returns the period we want, coming from a number
    """
    return client.periods[n-1]
    # type : object

def grade_on_20(grade : object):
    """
    Returns the grade out of 20
    """
    return ((float(grade.grade.replace(",",".")) / float(grade.out_of.replace(",",".")) * 20) * float(grade.coefficient))
    # type : float

def calc_avg_subject(trim:int):
    """
    Calculates the average of the student on every subject for an certain period
    """
    trim = trimester(trim)
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
                optionnal[grade.subject.name] += grade_on_20(grade)
                optionnal_coeff[grade.subject.name] += float(grade.coefficient)
            else:
                optionnal[grade.subject.name] = grade_on_20(grade)
                optionnal_coeff[grade.subject.name] = float(grade.coefficient)
        elif grade.subject.name in averages and averages[grade.subject.name] not in ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero"):
            if grade.is_bonus and grade_on_20(grade)>10:
                averages[grade.subject.name] += grade_on_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
            elif grade.is_bonus == False:
                averages[grade.subject.name] += grade_on_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
        else:
            if grade.is_bonus and grade_on_20(grade)>10:
                averages[grade.subject.name] = grade_on_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
            elif grade.is_bonus == False:
                averages[grade.subject.name] = grade_on_20(grade)
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
        if averages[key] not in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero"):
            averages[key] = round(averages[key] / coefficients[key],2)
    return averages, coefficients
    # type : dict

def calc_avg_overall(trim:int):
    """
    Calculates the overall average of the student for a certain period
    """
    overall_avg = 0
    invalid_avg_count = 0
    for moy in calc_avg_subject(trim)[0].values():
        if moy not in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero"):
            overall_avg += moy
        else:
            invalid_avg_count += 1
    return round(overall_avg / (len(calc_avg_subject(trim)[0]) - invalid_avg_count), 2)
    # type : float


def anal_subjects(sbj_list:list):
    """
    Takes a list of subjects as parameter and return a list of lists containing the corrected name of the subject and the path of the white and dark icons
    """
    sbj_dico = {
        "ABIBAC HG" : ["ABIBAC HG","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "ACL" : ["ACL","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "HG BFI ITALOPHONE" : ["HG ITALIEN","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "HG POLO" : ["HG POLONAIS","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "HG BRITANNIQUE" : ["HG BRITISH","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "CDM" : ["CDM","static/img/icons/w_CDM_final.png","static/img/icons/d_CDM_final.png"],
        "HIST.GEO.EDUC.CIVIQ." : ["HISTOIRE-GEO","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "ANGLAIS EURO" : ["ANGLAIS EURO","static/img/icons/w_EURO_eng_final.png","static/img/icons/d_EURO_eng_final.png"],
        "ALLEMAND EURO" : ["ALLEMAND EURO","static/img/icons/w_EURO_all_final.png","static/img/icons/d_EURO_all_final.png"],
        "LITT. ANGLAIS" : ["ANGLAIS","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "MATHEMATIQUES" : ["MATHS","static/img/icons/w_maths_final.png","static/img/icons/d_maths_final.png"],
        "SCIENCES VIE & TERRE" : ["SVT","static/img/icons/w_svt_final.png","static/img/icons/d_svt_final.png"],
        "SC. ECONO.& SOCIALES" : ["SES","static/img/icons/w_ses_final.png","static/img/icons/d_ses_final.png"],
        "HIST.GEO.GEOPOL.S.P." : ["HGGSP","static/img/icons/w_HGGSP_final.png","static/img/icons/d_HGGSP_final.png"],
        "NUMERIQUE SC. INFORM." :[ "NSI","static/img/icons/w_nsi_final.png","static/img/icons/d_nsi_final.png"],
        "PHYSIQUE-CHIMIE" : ["PHYSIQUE-CHIMIE","static/img/icons/w_p-c_final.png","static/img/icons/d_p-c_final.png"],
        "EDUCATION MUSICALE" : ["MUSIQUE","static/img/icons/w_music_final.png","static/img/icons/d_music_final.png"],
        "ITALIEN LV3" : ["ITALIEN LV3","static/img/icons/w_LV3_ita_final.png","static/img/icons/d_LV3_ita_final.png"],
        "ESPAGNOL LV3" : ["ESPAGNOL LV3","static/img/icons/w_LV3_esp_final.png","static/img/icons/d_LV3_esp_final.png"],
        "ARABE LV3" : ["ARABE LV3","static/img/icons/w_LV3_general_final.png","static/img/icons/d_LV3_general_final.png"],
        "FRANCAIS" : ["FRANCAIS","static/img/icons/w_FR-HLP-PHILO_final.png","static/img/icons/d_FR-HLP-PHILO_final.png"],
        "ENSEIGN SCIENTIFIQUE SPC" : ["ES PC","static/img/icons/w_p-c_final.png","static/img/icons/d_p-c_final.png"],
        "ENSEIGN.SCIENTIFIQUE SVT" : ["ES SVT","static/img/icons/w_svt_final.png","static/img/icons/d_svt_final.png"],
        "ALLEMAND LV2" : ["ALLEMAND LV2","static/img/icons/w_LV2_all_final.png","static/img/icons/d_LV2_all_final.png"],
        "LL ABIBAC" : ["LL ABIBAC","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "ANGLAIS LV1" : ["ANGLAIS LV1","static/img/icons/w_LV1_eng_final.png","static/img/icons/d_LV1_eng_final.png"],
        "DNL ANGLAIS SVT" : ["DNL SVT","static/img/icons/w_svt_final.png","static/img/icons/d_svt_final.png"],
        "HG BFI ARABOPHONE" : ["HG ARABE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "HIST.GEO AMERICAINE" : ["HG AMERICAINE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "HLPHI O" : ["HLP","static/img/icons/w_FR-HLP-PHILO_final.png","static/img/icons/d_FR-HLP-PHILO_final.png"],
        "ANGLAIS LV2" : ["ANGLAIS LV2","static/img/icons/w_LV2_eng_final.png","static/img/icons/d_LV2_eng_final.png"],
        "ACCOMPAGNEMENT. PERSO" : ["ACC. PERSO","static/img/icons/w_ACC-PERSO_final.png","static/img/icons/d_ACC-PERSO_final.png"],
        "DNL ALL" : ["DNL ALL","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "HG ESP" : ["HG ESP","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "DNL ANGLAIS" : ["DNL ANGLAIS","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "MATHS" : ["MATHS","static/img/icons/w_maths_final.png","static/img/icons/d_maths_final.png"],
        "ED.PHYSIQUE & SPORT." : ["EPS","static/img/icons/w_EPS_final.png","static/img/icons/d_EPS_final.png"],
        "HG PORT." : ["HG PORTUGAIS","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "Soutien LLCE" : ["Soutien LLCE","static/img/icons/w_LLCE_final.png","static/img/icons/d_LLCE_final.png"],
        "ACCOMPAGNEMT. PERSO" : ["ACC. PERSO","static/img/icons/w_ACC-PERSO_final.png","static/img/icons/d_ACC-PERSO_final.png"],
        "MATHS CHINOIS" : ["MATHS CHINOIS","static/img/icons/w_maths_final.png","static/img/icons/d_maths_final.png"],
        "CHINOIS LV3" : ["CHINOIS LV3","static/img/icons/w_LV3_china_final.png","static/img/icons/d_LV3_china_final.png"],
        "FRANCAIS LANGUE SECONDE" : ["FLS","static/img/icons/w_FLS_final.png","static/img/icons/d_FLS_final.png"],
        "DRAMA" : ["DRAMA","static/img/icons/w_DRAMA_final.png","static/img/icons/d_DRAMA_final.png"],
        "LL PORTUGAISE" : ["LL PORTUGAISE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "LL ESPAGNOLE" : ["LL ESPAGNOLE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "LL JAPONAISE" : ["LL JAPONAISE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "LL AROBOPHONE" : ["LL ARABOPHONE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "LL ANGLOPHONE" : ["LL ANGLOPHONE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "HG SEC. ANGLOPHONE" : ["HG ANGLOPHONE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "ACCO PERSO FRANC" : ["ACC PERSO FR","static/img/icons/w_ACC-PERSO_final.png","static/img/icons/d_ACC-PERSO_final.png"],
        "HG JAPO" : ["HG JAPONAISE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "ACCO PERSO MATH" : ["ACC PERSO MATHS","static/img/icons/w_ACC-PERSO_final.png","static/img/icons/d_ACC-PERSO_final.png"],
        "SC.NUMERIQUE.TECHNOL." : ["SNT","static/img/icons/w_nsi_final.png","static/img/icons/d_nsi_final.png"],
        "DS commun Maths" : ["DS MATHS","static/img/icons/w_maths_final.png","static/img/icons/d_maths_final.png"],
        "LL CHINOIS" : ["LL CHINOIS","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "HG ARABOPHONE" : ["HG ARABOPHONE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "LL ITALIENNE" : ["LL ITALIENNE","static/img/icons/w_LL-ACL_final.png","static/img/icons/d_LL-ACL_final.png"],
        "HG ITALIENNE" : ["HG ITALIENNE","static/img/icons/w_HG_final.png","static/img/icons/d_HG_final.png"],
        "LITTERAT. LCA LATIN" : ["LLCE","static/img/icons/w_LLCE_final.png","static/img/icons/d_LLCE_final.png"],
        "LCA LATIN" : ["LLCE","static/img/icons/w_LLCE_final.png","static/img/icons/d_LLCE_final.png"],
    }
    sbj_list_clean = []
    for subject in sbj_list:
        sbj_list_clean.append(sbj_dico[subject])    
    return sbj_list_clean
    # type : list

def get_subjects(trim:int):
    """
    Returns all the subjects in a list
    """
    subjects = []
    for x in trimester(trim).grades:
        if x.subject.name not in subjects:    
            subjects.append(x.subject.name)
    return subjects 
    # type : list

def anal_grades(trim:int):
    """
    Returns a dictionnary of a bunch a specificities on every grade for every subject
    """
    notes_dict = {} ; period = trimester(trim)
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, class average : float, subject name : str, period name : str]}
    for grade in period.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero"):
            if grade.subject.name in notes_dict:
                notes_dict[grade.subject.name] += [[grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
            else:
                notes_dict[grade.subject.name] = [[grade.grade , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        elif grade.subject.name in notes_dict:
            notes_dict[grade.subject.name] += [[float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, 'green' if grade_on_20(grade) >= floor(calc_avg_subject(trim)[0][grade.subject.name]) else 'red', float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        else:
            notes_dict[grade.subject.name] = [[float(grade.grade.replace(",",".")) , float(grade.out_of.replace(",",".")) , float(grade.coefficient.replace(",",".")) , grade.comment, 'green' if grade_on_20(grade) >= floor(calc_avg_subject(trim)[0][grade.subject.name]) else 'red', float(grade.grade.replace(",",".")) >float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
    return notes_dict
    # type : dict

def convert_to_100(grade:float, out_of:float):
    """"
    Returns the parameter (a grade) into a grade out of 100
    """
    return round(grade / out_of * 100,2)
    # type : float

def convert_to(grade: float, out_of:float, convert:int):
    """
    Converts and returns the grade into a desired out of
    """
    return round(grade / out_of * convert,2)
    # type : float

def calc_avg_evol(avg_old:float,avg_new:float):
    """
    Compares two averages and returns the evolution
    """
    return round((avg_new-avg_old)/avg_old * 100, 2)
    # type : float

def get_periods():
    """
    Returns a list with all the periods of the client
    """
    global client
    periods = {} ; n=0
    for period in client.periods:
        n+=1
        periods[period.name] = (n)
    return periods
