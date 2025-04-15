from constraint import Problem


problem = Problem()


#var, domain

# Séc
problem.addVariable("Security_Lecture", [("Sun", 1), ("Mon", 1), ("Tue", 1), ("Wed", 2), ("Thu", 3)])
problem.addVariable("Security_TD", [("Sun", 2), ("Mon", 3), ("Tue", 2), ("Wed", 4), ("Thu", 5)])

# MF
problem.addVariable("Methods_Formelles_Lecture", [("Sun", 1), ("Mon", 2), ("Tue", 1), ("Wed", 4), ("Thu", 5)])
problem.addVariable("Methods_Formelles_TD", [("Sun", 2), ("Mon", 4), ("Tue", 1), ("Wed", 3), ("Thu", 5)])

# Anum
problem.addVariable("Numerical_Analysis_Lecture", [("Sun", 3), ("Mon", 2), ("Tue", 1), ("Wed", 3), ("Thu", 4)])
problem.addVariable("Numerical_Analysis_TD", [("Sun", 4), ("Mon", 3), ("Tue", 2), ("Wed", 2), ("Thu", 1)])

# ESN
problem.addVariable("Entrepreneurship_Lecture", [("Sun", 1), ("Mon", 2), ("Tue", 1), ("Wed", 3), ("Thu", 4)])

# RO2
problem.addVariable("Operations_Research_Lecture", [("Sun", 1), ("Mon", 3), ("Tue", 1), ("Wed", 2), ("Thu", 4)])
problem.addVariable("Operations_Research_TD", [("Sun", 2), ("Mon", 4), ("Tue", 2), ("Wed", 5), ("Thu", 3)])

# Archi
problem.addVariable("Distributed_Architecture_Lecture", [("Sun", 1), ("Mon", 2), ("Tue", 1), ("Wed", 3), ("Thu", 4)])
problem.addVariable("Distributed_Architecture_TD", [("Sun", 2), ("Mon", 3), ("Tue", 1), ("Wed", 4), ("Thu", 5)])

# RSX2
problem.addVariable("Networks_Lecture", [("Sun", 1), ("Mon", 2), ("Tue", 1), ("Wed", 3), ("Thu", 4)])
problem.addVariable("Networks_TD", [("Sun", 2), ("Mon", 3), ("Tue", 2), ("Wed", 4), ("Thu", 5)])
problem.addVariable("Networks_TP", [("Sun", 3), ("Mon", 4), ("Tue", 1), ("Wed", 5), ("Thu", 3)])

# AI 
problem.addVariable("AI_Lecture", [("Sun", 1), ("Mon", 2), ("Tue", 1), ("Wed", 3), ("Thu", 4)])
problem.addVariable("AI_TD", [("Sun", 2), ("Mon", 3), ("Tue", 1), ("Wed", 4), ("Thu", 5)])
problem.addVariable("AI_TP", [("Sun", 3), ("Mon", 4), ("Tue", 2), ("Wed", 5), ("Thu", 3)])

#---------------------------------------------------CONSTRAINTS----------------------------------------------------


# No overlapping cons
def no_overlap(sec_lecture, sec_td):
    return sec_lecture != sec_td

problem.addConstraint(no_overlap, ["Security_Lecture", "Security_TD"])
problem.addConstraint(no_overlap, ["Methods_Formelles_Lecture", "Methods_Formelles_TD"])
problem.addConstraint(no_overlap, ["Numerical_Analysis_Lecture", "Numerical_Analysis_TD"])
problem.addConstraint(no_overlap, ["Operations_Research_Lecture", "Operations_Research_TD"])
problem.addConstraint(no_overlap, ["Distributed_Architecture_Lecture", "Distributed_Architecture_TD"])
problem.addConstraint(no_overlap, ["Networks_Lecture", "Networks_TD", "Networks_TP"])
problem.addConstraint(no_overlap, ["AI_Lecture", "AI_TD", "AI_TP"])

# No more than 3 successive slots
def no_more_than_three_consecutive(*slots):
    # Check if any of the sessions are in consecutive slots
    for i in range(len(slots) - 1):
        day, slot = slots[i]
        next_day, next_slot = slots[i + 1]
        if day == next_day and slot + 1 == next_slot:
            return False  # consecutive slot
    return True


problem.addConstraint(no_more_than_three_consecutive, ["Security_Lecture", "Security_TD"])
problem.addConstraint(no_more_than_three_consecutive, ["Methods_Formelles_Lecture", "Methods_Formelles_TD"])
problem.addConstraint(no_more_than_three_consecutive, ["Numerical_Analysis_Lecture", "Numerical_Analysis_TD"])
problem.addConstraint(no_more_than_three_consecutive, ["Operations_Research_Lecture", "Operations_Research_TD"])
problem.addConstraint(no_more_than_three_consecutive, ["Distributed_Architecture_Lecture", "Distributed_Architecture_TD"])
problem.addConstraint(no_more_than_three_consecutive, ["Networks_Lecture", "Networks_TD", "Networks_TP"])
problem.addConstraint(no_more_than_three_consecutive, ["AI_Lecture", "AI_TD", "AI_TP"])

# no overlapping sessions for the same teacher
def teacher_not_in_two_places_at_same_time(*slots):
    seen = set()
    for day, slot in slots:
        if (day, slot) in seen:
            return False  
        seen.add((day, slot))
    return True


problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Security_Lecture", "Security_TD"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Methods_Formelles_Lecture", "Methods_Formelles_TD"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Numerical_Analysis_Lecture", "Numerical_Analysis_TD"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Operations_Research_Lecture", "Operations_Research_TD"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Distributed_Architecture_Lecture", "Distributed_Architecture_TD"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["Networks_Lecture", "Networks_TD", "Networks_TP"])
problem.addConstraint(teacher_not_in_two_places_at_same_time, ["AI_Lecture", "AI_TD", "AI_TP"])
