import webbrowser
import random

DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu"]
SLOTS_PER_DAY = {"Sun": 5, "Mon": 5, "Tue": 3, "Wed": 5, "Thu": 5}

courses = {
    "Securite": ("Teacher1", 2),
    "MF": ("Teacher2", 2),
    "AN": ("Teacher3", 2),
    "ENT": ("Teacher4", 1),
    "RO2": ("Teacher5", 2),
    "DAIC": ("Teacher6", 2),
    "RES": ("Teacher7", 2),
    "RES_TP": ("Teacher8", 1),
    "AI": ("Teacher11", 2),
    "AI_TP": ("Teacher12", 1),
}

teacher_courses = {}
for course, (teacher, _) in courses.items():
    teacher_courses.setdefault(teacher, []).append(course)

sessions = []
for course, (teacher, count) in courses.items():
    if course.endswith("_TP"):
        sessions.append((course, teacher))
    else:
        sessions.append((f"{course}_L", teacher))
        if count == 2:
            sessions.append((f"{course}_TD", teacher))

session_names = [s[0] for s in sessions]
session_teachers = [s[1] for s in sessions]

def generate_domains():
    domains = {}
    for session in session_names:
        dom = [(day, slot) for day in DAYS for slot in range(SLOTS_PER_DAY[day])]
        random.shuffle(dom)
        domains[session] = dom
    return domains

def is_valid(assignment, var, value):
    day, hour = value
    current_teacher = session_teachers[session_names.index(var)]

    for k, (d, h) in assignment.items():
        if d == day and h == hour:
            return False
        if d == day and h == hour and k.split("_")[0] == var.split("_")[0] and k != var:
            return False
        if d == day:
            if abs(h - hour) <= 2 and k != var:
                same_day_hours = sorted(set(
                    [hh for kk, (dd, hh) in assignment.items() if dd == day] + [hour]
                ))
                for i in range(len(same_day_hours) - 3):
                    if same_day_hours[i+3] - same_day_hours[i] == 3:
                        return False

    teacher_days = set()
    for k, (d, _) in assignment.items():
        if session_teachers[session_names.index(k)] == current_teacher:
            teacher_days.add(d)
    teacher_days.add(day)
    if len(teacher_days) > 2:
        return False

    return True

def select_unassigned(assignment, domains):
    unassigned = [v for v in session_names if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

def order_domain_values(var, domains):
    values = domains[var]
    return sorted(values, key=lambda val: count_conflicts(var, val, domains))

def count_conflicts(var, value, domains):
    conflicts = 0
    day, hour = value
    current_teacher = session_teachers[session_names.index(var)]

    for other_var in domains:
        if other_var != var:
            for other_val in domains[other_var]:
                other_day, other_hour = other_val
                other_teacher = session_teachers[session_names.index(other_var)]

                if day == other_day and hour == other_hour:
                    conflicts += 1
                if day == other_day and hour == other_hour and other_var.split("_")[0] == var.split("_")[0]:
                    conflicts += 1
                if other_teacher == current_teacher and other_day == day:
                    teacher_days = set()
                    for v in domains:
                        if v != var and v != other_var:
                            for d, _ in domains[v]:
                                if session_teachers[session_names.index(v)] == current_teacher:
                                    teacher_days.add(d)
                    teacher_days.add(day)
                    if len(teacher_days) > 2:
                        conflicts += 1
    return conflicts

def backtrack(assignment, domains):
    if len(assignment) == len(session_names):
        return assignment
    var = select_unassigned(assignment, domains)
    for value in order_domain_values(var, domains):
        if is_valid(assignment, var, value):
            assignment[var] = value
            new_domains = {}
            for v in domains:
                if v in assignment:
                    new_domains[v] = [assignment[v]]
                else:
                    new_domains[v] = [val for val in domains[v] if is_valid(assignment, v, val)]
            result = backtrack(assignment, new_domains)
            if result:
                return result
            del assignment[var]
    return None

COLORS = {
    'Securite': '#FFC0CB',
    'MF': '#ADD8E6',
    'AN': '#90EE90',
    'ENT': '#FFD700',
    'RO2': '#1E90FF',
    'DAIC': '#FFA07A',
    'RES': '#D3D3D3',
    'RES_TP': '#C0C0C0',
    'AI': '#BA55D3',
    'AI_TP': '#9370DB'
}

LABELS = {
    "Securite_L": "SEC-L", "Securite_TD": "SEC-TD",
    "MF_L": "MF-L", "MF_TD": "MF-TD",
    "AN_L": "AN-L", "AN_TD": "AN-TD",
    "ENT_L": "ENT",
    "RO2_L": "RO2-L", "RO2_TD": "RO2-TD",
    "DAIC_L": "DAIC-L", "DAIC_TD": "DAIC-TD",
    "RES_L": "RES-L", "RES_TD": "RES-TD", "RES_TP": "RES-TP",
    "AI_L": "AI-L", "AI_TD": "AI-TD", "AI_TP": "AI-TP"
}

def get_subject(key):
    return key.split("_")[0]

def generate_html(solution):
    html = """
    <html><head>
    <meta charset="UTF-8">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            background: #f4f6f9;
            margin: 20px;
            color: #333;
        }
        h2, h3 {
            text-align: center;
            color: #2c3e50;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px auto;
            background: #fff;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
            border-radius: 8px;
            overflow: hidden;
        }
        th, td {
            border: 1px solid #e0e0e0;
            padding: 12px;
            text-align: center;
        }
        th {
            background-color: #f7f9fc;
            font-weight: 600;
        }
        td {
            background-color: #fafafa;
        }
        .empty {
            color: #aaa;
            font-style: italic;
        }
        div.session {
            border-radius: 8px;
            padding: 8px;
            color: #222;
            font-weight: 500;
            line-height: 1.4em;
            box-shadow: inset 0 0 0 1px rgba(0,0,0,0.05);
        }
        .session small {
            display: block;
            font-size: 0.8em;
            color: #555;
            margin-top: 4px;
        }
        table:last-of-type {
            width: 60%;
        }
    </style>
    </head><body>
    <h2>📅 Semester 2 Timetable - Group 1CS</h2>
    <table>
      <tr><th>Day / Slot</th>""" + "".join(f"<th>Slot {i+1}</th>" for i in range(5)) + "</tr>"

    for day in DAYS:
        html += f"<tr><th>{day}</th>"
        for slot in range(5):
            cell = ""
            for session, (d, h) in solution.items():
                if d == day and h == slot:
                    subject = get_subject(session)
                    label = LABELS.get(session, session[:6])
                    teacher = session_teachers[session_names.index(session)]
                    color = COLORS.get(subject, "#FFFFFF")
                    cell = (
                        f'<div class="session" style="background:{color}">'
                        f"{label}<small>{teacher}</small></div>"
                    )
                    break
            if not cell and slot < SLOTS_PER_DAY[day]:
                cell = '<div class="empty">Free</div>'
            elif not cell:
                cell = '<div class="empty">-</div>'
            html += f"<td>{cell}</td>"
        html += "</tr>"

    html += """
    </table>
    <h3>👩‍🏫 Teacher Workload Summary</h3>
    <table>
        <tr><th>Teacher</th><th>Days Working</th><th>Courses</th></tr>"""

    teacher_stats = {}
    for teacher in teacher_courses:
        days = set()
        for session, (d, _) in solution.items():
            if session_teachers[session_names.index(session)] == teacher:
                days.add(d)
        teacher_stats[teacher] = {
            'days': len(days),
            'courses': ", ".join(teacher_courses[teacher])
        }

    for teacher, stats in teacher_stats.items():
        html += f"<tr><td>{teacher}</td><td>{stats['days']}</td><td>{stats['courses']}</td></tr>"

    html += "</table></body></html>"

    with open("output.html", "w", encoding="utf-8") as f:
        f.write(html)
    webbrowser.open("output.html")

if __name__ == "__main__":
    while True:
        solution = backtrack({}, generate_domains())
        if solution:
            generate_html(solution)
            break
        else:
            print("No valid timetable found, retrying...")
