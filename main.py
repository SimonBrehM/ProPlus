"""
Determines all main calculations related functions and definitions
"""
#   _                  _____           _____           _____  ______   _    _ _    _  _____  ____
#  | |        /\      / ____|   /\    / ____|  /\     |  __ \|  ____| | |  | | |  | |/ ____|/ __ \
#  | |       /  \    | |       /  \  | (___   /  \    | |  | | |__    | |__| | |  | | |  __| |  | |
#  | |      / /\ \   | |      / /\ \  \___ \ / /\ \   | |  | |  __|   |  __  | |  | | | |_ | |  | |
#  | |____ / ____ \  | |____ / ____ \ ____) / ____ \  | |__| | |____  | |  | | |__| | |__| | |__| |
#  |______/_/    \_\  \_____/_/    \_\_____/_/    \_\ |_____/|______| |_|  |_|\____/ \_____|\____/


from math import floor
import pronotepy
from pronotepy.ent import ent_auvergnerhonealpe
# importing ent specific function, you do not need to import anything if you dont use an ent

CLIENT = None

def get_data(username, password):
    """
    Makes the connection with Pronote
    """
    global CLIENT
    CLIENT = pronotepy.Client('https://0693446w.index-education.net/pronote/eleve.html',
                        username=username,
                        password=password,
                        ent=ent_auvergnerhonealpe) # ent specific

    if not CLIENT.logged_in:
        exit(1)  # the client has failed to log in

def get_current_period():
    """
    Returns the current period of the client
    """
    return CLIENT.current_period.name

def trimester(n:int):
    """
    Function that returns the period we want, coming from a number
    """
    return CLIENT.periods[n-1]
    # type : object

def grade_formatting(grade : object):
    """
    Returns the grade as a float
    """
    return float(grade.grade.replace(",","."))

def out_of_formatting(grade : object):
    """
    Returns the grade out of as a float
    """
    return float(grade.out_of.replace(",","."))

def coeff_formatting(grade : object):
    """
    Returns the grade coefficient as a float
    """
    return float(grade.coefficient.replace(",","."))

def grade_on_20(grade : object):
    """
    Returns the grade out of 20
    """
    return ((grade_formatting(grade) / grade_formatting(grade) * 20) * float(grade.coefficient))
    # type : float
iterations = 0
def calc_avg_subject(trim:int):
    """
    Calculates the average of the student on every subject for an certain period
    """
    trim = trimester(trim)
    optionnal = {}
    optionnal_coeff = {}
    coefficients = {}
    averages = {}
    invalid_grade = ("Absent","NonNote","Inapte","NonRendu", "AbsentZero", "NonRenduZero", "Dispense")
    # averages = {subject : grade out of 20}
    # coefficients = {subject : sum of coefficients}
    for grade in trim.grades:
        if grade.grade in invalid_grade:
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
        elif grade.subject.name in averages and averages[grade.subject.name] not in invalid_grade:
            if grade.is_bonus and grade_on_20(grade)>10:
                averages[grade.subject.name] += grade_on_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
            elif grade.is_bonus is False:
                averages[grade.subject.name] += grade_on_20(grade)
                coefficients[grade.subject.name] += float(grade.coefficient)
        else:
            if grade.is_bonus and grade_on_20(grade)>10:
                averages[grade.subject.name] = grade_on_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
            elif grade.is_bonus is False:
                averages[grade.subject.name] = grade_on_20(grade)
                coefficients[grade.subject.name] = float(grade.coefficient)
    if optionnal:
        for key, value in optionnal.items():
            if key not in averages:
                averages[key] = value
                coefficients[key] = optionnal_coeff[key]
            elif optionnal[key] > round(averages[key] / coefficients[key],2):
                averages[key] += value
                coefficients[key] += optionnal_coeff[key]
    for key, value in averages.items(): # do not use .items or find the way to truly change and access the value
        print(key, value)
        if value not in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero", "Dispense"):
            value = round(value / coefficients[key],2)
            print(key, value)
    print(averages)
    global iterations
    iterations += 1
    print(iterations)
    return averages, coefficients
    # type : dict

def calc_avg_overall(trim:int):
    """
    Calculates the overall average of the student for a certain period
    """
    overall_avg = 0
    invalid_avg_count = 0
    for moy in calc_avg_subject(trim)[0].values():
        if moy not in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero", "Dispense"):
            overall_avg += moy
        else:
            invalid_avg_count += 1
    return round(overall_avg / (len(calc_avg_subject(trim)[0]) - invalid_avg_count), 2)
    # type : float


def anal_subjects(sbj_list:list, reverse:bool=False):
    """
    Takes a list of subjects as parameter and return a list of lists containing 
    the corrected name of the subject and the path of the white and dark icons
    """
    path = "static/img/icons/"
    sbj_dico = {
        "ABIBAC HG" : ["ABIBAC HG",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "ACL" : ["ACL",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "ACL > ACL" : ["ACL",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "HG BFI ITALOPHONE" : ["HG ITALIEN",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "HG POLO" : ["HG POLONAIS",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "HG BRITANNIQUE" : ["HG BRITISH",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "CDM" : ["CDM",f"{path}w_CDM_final.png",f"{path}d_CDM_final.png"],
        "CDM > CDM" : ["CDM",f"{path}w_CDM_final.png",f"{path}d_CDM_final.png"],
        "HIST.GEO.EDUC.CIVIQ." : ["HISTOIRE-GEO",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "ANGLAIS EURO":["ANGLAIS EURO",f"{path}w_EURO_eng_final.png",f"{path}d_EURO_eng_final.png"],
        "ALLEMAND EURO" : ["ALLEMAND EURO",f"{path}w_EURO_all_final.png",f"{path}d_EURO_all_final.png"],
        "LITT. ANGLAIS" : ["ANGLAIS",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "MATHEMATIQUES" : ["MATHS",f"{path}w_maths_final.png",f"{path}d_maths_final.png"],
        "SCIENCES VIE & TERRE" : ["SVT",f"{path}w_svt_final.png",f"{path}d_svt_final.png"],
        "SC. ECONO.& SOCIALES" : ["SES",f"{path}w_ses_final.png",f"{path}d_ses_final.png"],
        "EMC" : ["EMC",f"{path}w_EMC_final.png",f"{path}d_EMC_final.png"],
        "HIST.GEO.GEOPOL.S.P." : ["HGGSP",f"{path}w_HGGSP_final.png",f"{path}d_HGGSP_final.png"],
        "NUMERIQUE SC.INFORM." :[ "NSI",f"{path}w_nsi_final.png",f"{path}d_nsi_final.png"],
        "PHYSIQUE-CHIMIE" : ["PHYSIQUE-CHIMIE",f"{path}w_p-c_final.png",f"{path}d_p-c_final.png"],
        "EDUCATION MUSICALE" : ["MUSIQUE",f"{path}w_music_final.png",f"{path}d_music_final.png"],
        "ITALIEN LV3" : ["ITALIEN LV3",f"{path}w_LV3_ita_final.png",f"{path}d_LV3_ita_final.png"],
        "ESPAGNOL LV3" : ["ESPAGNOL LV3",f"{path}w_LV3_esp_final.png",f"{path}d_LV3_esp_final.png"],
        "ARABE LV3":["ARABE LV3",f"{path}w_LV3_general_final.png",f"{path}d_LV3_general_final.png"],
        "FRANCAIS":["FRANCAIS",f"{path}w_FR-HLP-PHILO_final.png",f"{path}d_FR-HLP-PHILO_final.png"],
        "ENSEIGN SCIENTIFIQUE SPC" : ["ES PC",f"{path}w_p-c_final.png",f"{path}d_p-c_final.png"],
        "ENSEIGN.SCIENTIFIQUE > PH-CH":["ES PC",f"{path}w_p-c_final.png",f"{path}d_p-c_final.png"],
        "ENSEIGN.SCIENTIFIQUE SVT" : ["ES SVT",f"{path}w_svt_final.png",f"{path}d_svt_final.png"],
        "ENSEIGN.SCIENTIFIQUE > SVT" : ["ES SVT",f"{path}w_svt_final.png",f"{path}d_svt_final.png"],
        "ALLEMAND LV2" : ["ALLEMAND LV2",f"{path}w_LV2_all_final.png",f"{path}d_LV2_all_final.png"],
        "ESPAGNOL LV2" : ["ESPAGNOL LV2",f"{path}w_LV2_esp_final.png",f"{path}d_LV2_esp_final.png"],
        "LL ABIBAC" : ["LL ABIBAC",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "ANGLAIS LV1" : ["ANGLAIS LV1",f"{path}w_LV1_eng_final.png",f"{path}d_LV1_eng_final.png"],
        "DNL ANGLAIS SVT" : ["DNL SVT",f"{path}w_svt_final.png",f"{path}d_svt_final.png"],
        "HG BFI ARABOPHONE" : ["HG ARABE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "HIST.GEO AMERICAINE" : ["HG AMERICAINE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "HIST.GEO AMERICAINE > HIST.GEO AMERICAINE" : ["HG AMERICAINE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "HLPHI O" : ["HLP",f"{path}w_FR-HLP-PHILO_final.png",f"{path}d_FR-HLP-PHILO_final.png"],
        "PHILOSOPHIE":["PHILO",f"{path}w_FR-HLP-PHILO_final.png",f"{path}d_FR-HLP-PHILO_final.png"],
        "PHILOSOPHIE > PHILOSOPHIE" : ["PHILO",f"{path}w_FR-HLP-PHILO_final.png",f"{path}d_FR-HLP-PHILO_final.png"],
        "ANGLAIS LV2" : ["ANGLAIS LV2",f"{path}w_LV2_eng_final.png",f"{path}d_LV2_eng_final.png"],
        "ACCOMPAGNEMENT. PERSO" : ["ACC. PERSO",f"{path}w_ACC-PERSO_final.png",f"{path}d_ACC-PERSO_final.png"],
        "DNL ALL" : ["DNL ALL",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "HG ESP" : ["HG ESP",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "DNL ANGLAIS" : ["DNL ANGLAIS",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "MATHS EXPERTES" : ["MATHEX",f"{path}w_mathex_final.png",f"{path}d_mathex_final.png"],
        "ED.PHYSIQUE & SPORT." : ["EPS",f"{path}w_EPS_final.png",f"{path}d_EPS_final.png"],
        "HG PORT." : ["HG PORTUGAIS",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "Soutien LLCE" : ["Soutien LLCE",f"{path}w_LLCE_final.png",f"{path}d_LLCE_final.png"],
        "ACCOMPAGNEMT. PERSO" : ["ACC. PERSO",f"{path}w_ACC-PERSO_final.png",f"{path}d_ACC-PERSO_final.png"],
        "MATHS CHINOIS" : ["MATHS CHINOIS",f"{path}w_maths_final.png",f"{path}d_maths_final.png"],
        "CHINOIS LV3":["CHINOIS LV3",f"{path}w_LV3_china_final.png",f"{path}d_LV3_china_final.png"],
        "FRANCAIS LANGUE SECONDE" : ["FLS",f"{path}w_FLS_final.png",f"{path}d_FLS_final.png"],
        "DRAMA" : ["DRAMA",f"{path}w_DRAMA_final.png",f"{path}d_DRAMA_final.png"],
        "LL PORTUGAISE" : ["LL PORTUGAISE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "LL ESPAGNOLE" : ["LL ESPAGNOLE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "LL JAPONAISE" : ["LL JAPONAISE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "LL AROBOPHONE" : ["LL ARABOPHONE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "LL ANGLOPHONE" : ["LL ANGLOPHONE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "HG SEC. ANGLOPHONE" : ["HG ANGLOPHONE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "ACCO PERSO FRANC" : ["ACC PERSO FR",f"{path}w_ACC-PERSO_final.png",f"{path}d_ACC-PERSO_final.png"],
        "HG JAPO" : ["HG JAPONAISE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "ACCO PERSO MATH" : ["ACC PERSO MATHS",f"{path}w_ACC-PERSO_final.png",f"{path}d_ACC-PERSO_final.png"],
        "SC.NUMERIQUE.TECHNOL." : ["SNT",f"{path}w_nsi_final.png",f"{path}d_nsi_final.png"],
        "DS commun Maths" : ["DS MATHS",f"{path}w_maths_final.png",f"{path}d_maths_final.png"],
        "LL CHINOIS" : ["LL CHINOIS",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "HG ARABOPHONE" : ["HG ARABOPHONE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "LL ITALIENNE" : ["LL ITALIENNE",f"{path}w_LL-ACL_final.png",f"{path}d_LL-ACL_final.png"],
        "HG ITALIENNE" : ["HG ITALIENNE",f"{path}w_HG_final.png",f"{path}d_HG_final.png"],
        "LITTERAT. LCA LATIN" : ["LLCE",f"{path}w_LLCE_final.png",f"{path}d_LLCE_final.png"],
        "LCA LATIN" : ["LLCE",f"{path}w_LLCE_final.png",f"{path}d_LLCE_final.png"],
    }
    if reverse:
        sbj_dico = {value[0]: key for key, value in sbj_dico.items()}
        sbj_list_clean = [sbj_dico[sbj] for sbj in sbj_list]
    else:
        sbj_list_clean = []
        for subject in sbj_list:
            if subject not in sbj_dico:
                sbj_list_clean.append([subject,f"{path}w_default_final.png",f"{path}d_default_final.png"])
            else:
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
    notes_dict = {}
    period = trimester(trim)
    # notes_dict = {subject : [actual grade : float, grade.out_of : float, grade.coefficient : float, grade description : str, is grade good for subject average : bool, is grade over class average : bool, class average : float, subject name : str, period name : str]}
    for grade in period.grades:
        if grade.grade in ("Absent","NonNote","Inapte","NonRendu","AbsentZero","NonRenduZero", "Dispense"):
            if grade.subject.name in notes_dict:
                notes_dict[grade.subject.name] += [[grade.grade , out_of_formatting(grade) , coeff_formatting(grade) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
            else:
                notes_dict[grade.subject.name] = [[grade.grade , out_of_formatting(grade) , coeff_formatting(grade) , grade.comment, None, None, float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        elif grade.subject.name in notes_dict:
            notes_dict[grade.subject.name] += [[grade_formatting(grade) , out_of_formatting(grade) , coeff_formatting(grade) , grade.comment, '#00BA00' if grade_formatting(grade)/out_of_formatting(grade) >= floor(calc_avg_subject(trim)[0][grade.subject.name])/20 else 'red', grade_formatting(grade) > float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
        else:
            notes_dict[grade.subject.name] = [[grade_formatting(grade) , out_of_formatting(grade) , coeff_formatting(grade) , grade.comment, '#00BA00' if grade_formatting(grade)/out_of_formatting(grade) >= floor(calc_avg_subject(trim)[0][grade.subject.name])/20 else 'red', grade_formatting(grade) > float(grade.average.replace(",",".")), float(grade.average.replace(",",".")), grade.subject.name, period.name]]
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
    global CLIENT
    periods = {}
    n=0
    for period in CLIENT.periods:
        n+=1
        periods[period.name] = n
    return periods

def str_to_float(value:str):
    """
    Converts and str to a float
    """
    return float(value.replace(',', '.'))
