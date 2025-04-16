from constraint import *
from collections import defaultdict
from itertools import combinations

# --- Configuration des jours et créneaux ---
days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday"]
day_slots = {
    "Sunday": [1, 2, 3, 4, 5],
    "Monday": [1, 2, 3, 4, 5],
    "Tuesday": [1, 2, 3],  # mardi matin uniquement
    "Wednesday": [1, 2, 3, 4, 5],
    "Thursday": [1, 2, 3, 4, 5],
}

# Tous les créneaux disponibles (jour, slot)
def valid_slots():
    return [(day, slot) for day in days for slot in day_slots[day]]

# --- Matières et enseignants ---
courses = {
    "Securite": ["Brahmi"],
    "MethFormelles": ["Zedek"],
    "AnalyseNum": ["Alkama"],
    "Entrepreneuriat": ["Kaci"],
    "RO2": ["Issaadi"],
    "ArchDist": ["Djenadi"],
    "Reseaux2": ["Zenadji", "Sahli"],
    "AI": ["Lekehali", "Chelghoum", "Badache"],
}

# Création des variables
variables = []
teacher_map = {}

def add_course_vars(course, teachers, td=True, tp=False):
    lec = f"{course}_LEC"
    variables.append(lec)
    teacher_map[lec] = teachers[0]
    if td:
        td_name = f"{course}_TD"
        variables.append(td_name)
        teacher_map[td_name] = teachers[0]
    if tp:
        tp_name = f"{course}_TP"
        variables.append(tp_name)
        teacher_map[tp_name] = teachers[1:]  # Plusieurs profs TP

# Ajouter les cours
add_course_vars("Securite", ["Brahmi"])
add_course_vars("MethFormelles", ["Zedek"])
add_course_vars("AnalyseNum", ["Alkama"])
add_course_vars("Entrepreneuriat", ["Kaci"], td=False)
add_course_vars("RO2", ["Issaadi"])
add_course_vars("ArchDist", ["Djenadi"])
add_course_vars("Reseaux2", ["Zenadji", "Sahli"], tp=True)
add_course_vars("AI", ["Lekehali", "Chelghoum", "Badache"], tp=True)

# --- Initialisation du problème CSP ---
problem = Problem()
domain = valid_slots()

for var in variables:
    problem.addVariable(var, domain)

# --- Contraintes ---

# 1. Deux cours ne doivent pas être au même créneau
for var1, var2 in combinations(variables, 2):
    problem.addConstraint(lambda x, y: x != y, (var1, var2))

# 2. Pas 4 créneaux consécutifs pour un enseignant
def no_four_consecutive_slots(*args):
    day_slots_by_teacher = defaultdict(list)
    for var, (day, slot) in zip(variables, args):
        teacher = teacher_map[var]
        if isinstance(teacher, list):  # Cas TP
            teacher = teacher[0]
        day_slots_by_teacher[(teacher, day)].append(slot)

    for slots in day_slots_by_teacher.values():
        slots.sort()
        for i in range(len(slots) - 3):
            if slots[i+3] - slots[i] == 3:
                return False
    return True

problem.addConstraint(no_four_consecutive_slots, variables)

# 3. LEC et TD d’un même cours ne doivent pas être au même créneau
for course in courses:
    lec = f"{course}_LEC"
    td = f"{course}_TD"
    if lec in variables and td in variables:
        problem.addConstraint(lambda a, b: a != b, (lec, td))

# --- Résolution ---
solution = problem.getSolution()

# --- Affichage ---
if not solution:
    print("❌ Aucune solution trouvée.")
else:
    print("✅ Emploi du temps généré :\n")
    # Tri par jour et créneau
    sorted_solution = sorted(solution.items(), key=lambda x: (days.index(x[1][0]), x[1][1]))

    for var, (day, slot) in sorted_solution:
        prof = teacher_map[var]
        if isinstance(prof, list):  # si TP avec plusieurs profs
            prof = prof[0]  # choix arbitraire
        print(f"{var:<20} → {day} Slot {slot} | Prof: {prof}")
