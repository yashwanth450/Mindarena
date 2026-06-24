from js import document, setInterval, clearInterval, window
from pyodide.ffi import create_proxy
import random
import asyncio


username_input = ""
age_input_value = ""
current_user = None
games_completed = 0
final_score = 0


def register(e):
    name     = document.getElementById("reg-name").value.strip()
    age      = document.getElementById("reg-age").value.strip()
    password = document.getElementById("reg-password").value.strip()

    def show_err(msg):
        document.getElementById("reg-error").innerText = msg

    if not name:
        show_err("⚠️ Please enter your name")
        return
    if not age:
        show_err("⚠️ Please enter your age")
        return
    if len(password) < 6:
        show_err("⚠️ Password must be at least 6 characters")
        return

    global username_input, age_input_value, current_user

    username_input  = name.upper()
    age_input_value = age

    def go():
        global games_completed, current_user
        games_completed = 0

        current_user = type("User", (), {
            "name":           username_input,
            "age":            age_input_value,
            "total_score":    0,
            "total_games":    0,
            "fast_answers":   0,
            "medium_answers": 0,
            "slow_answers":   0,
        })()

        _enter_test_section()

    async def check_and_register():
        result = await window.registerUser(username_input, age_input_value, password)

        if not result.success:
            show_err(result.message)
            return

        show_err("")
        window.showLoader(2000, "Creating your account...", create_proxy(go))

    asyncio.create_task(check_and_register())

document.getElementById("btn-register").addEventListener(
    "click", create_proxy(register)
)


async def login(e):
    global current_user

    name     = document.getElementById("login-name").value.strip().upper()
    password = document.getElementById("login-password").value.strip()

    def show_err(msg):
        document.getElementById("login-error").innerText = msg

    if not name:
        show_err("⚠️ Please enter your name")
        return
    if not password:
        show_err("⚠️ Please enter your password")
        return

    result = await window.loginUser(name, password)

    if not result.success:
        show_err(result.message)
        return

    current_user = result.user
    show_err("✅ Login successful!")

    def go():
        document.getElementById("section_login").style.display = "none"
        _enter_test_section()

    window.showLoader(2000, "Logging you in...", create_proxy(go))

document.getElementById("btn-login").addEventListener(
    "click", create_proxy(login)
)


def main_page_create_new_profile(_):
    document.getElementById("sectionmain_page").style.display = "none"
    document.getElementById("section_new_profile").style.display = "block"

document.getElementById("create_new_profile").addEventListener(
    "click", create_proxy(main_page_create_new_profile)
)


def main_page_login(_):
    document.getElementById("sectionmain_page").style.display = "none"
    document.getElementById("section_login").style.display = "block"

document.getElementById("login_button").addEventListener(
    "click", create_proxy(main_page_login)
)


def _enter_test_section():
    global games_completed
    games_completed = 0

    document.getElementById("sectionmain_page").style.display   = "none"
    document.getElementById("section_new_profile").style.display = "none"
    document.getElementById("section_login").style.display       = "none"
    document.getElementById("sectiontest").style.display         = "block"

    document.getElementById("games_completed").disabled    = True
    document.getElementById("games_completed").style.opacity = "0.4"
    document.getElementById("games_completed").innerText   = "complete 3 games to go.."

    document.getElementById("tick-reasoning").style.display = "none"
    document.getElementById("tick-missing").style.display   = "none"
    document.getElementById("play").disabled        = False
    document.getElementById("play").style.opacity   = "1"
    document.getElementById("play-missing").disabled      = False
    document.getElementById("play-missing").style.opacity = "1"


def display_reasoning(e):
    def go():
        document.getElementById("sectiontest").style.display      = "none"
        document.getElementById("sectionReasoning").style.display = "block"
        start_game()
    window.showLoader_game(3000, create_proxy(go))

document.getElementById("play").addEventListener(
    "click", create_proxy(display_reasoning)
)


def display_missing(e):
    def go():
        document.getElementById("sectiontest").style.display  = "none"
        document.getElementById("sectionmissing").style.display = "block"
        start_game_2()
    window.showLoader_game(3000, create_proxy(go))

document.getElementById("play-missing").addEventListener(
    "click", create_proxy(display_missing)
)


def games_reasoning(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display      = "block"

document.getElementById("exit").addEventListener(
    "click", create_proxy(games_reasoning)
)


def games_missing(_):
    document.getElementById("sectionmissing").style.display = "none"
    document.getElementById("sectiontest").style.display    = "block"

document.getElementById("exit_2").addEventListener(
    "click", create_proxy(games_missing)
)



score = 0
fast_answers = 0
medium_answers = 0
slow_answers = 0

selected_questions = []
current = 0
answered = False
time_left = 15
timer_id = None

pattern_pool = [
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [2, 4, 8],
            [3, 6, 12],
            [4, 8, "?"]
        ],
        "options": ["12", "14", "16", "18"],
        "answer": "16"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [1, 2, 3],
            [4, 8, 12],
            [5, 10, "?"]
        ],
        "options": ["12", "15", "18", "20"],
        "answer": "15"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [3, 6, 9],
            [4, 8, 12],
            [5, 10, "?"]
        ],
        "options": ["12", "13", "15", "18"],
        "answer": "15"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [10, 20, 30],
            [5, 10, 15],
            [2, 4, "?"]
        ],
        "options": ["6", "8", "10", "12"],
        "answer": "6"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [1, 1, 2],
            [2, 4, 8],
            [3, 9, "?"]
        ],
        "options": ["18", "24", "27", "30"],
        "answer": "27"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [2, 3, 5],
            [3, 5, 8],
            [5, 8, "?"]
        ],
        "options": ["12", "13", "14", "15"],
        "answer": "13"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [1, 4, 9],
            [4, 9, 16],
            [9, 16, "?"]
        ],
        "options": ["25", "26", "27", "28"],
        "answer": "25"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [2, 6, 18],
            [3, 12, 48],
            [4, 20, "?"]
        ],
        "options": ["60", "80", "100", "120"],
        "answer": "100"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [5, 10, 15],
            [6, 12, 18],
            [7, 14, "?"]
        ],
        "options": ["20", "21", "22", "23"],
        "answer": "21"
    },
    {
        "type": "grid",
        "instruction": "Find the missing number:",
        "grid": [
            [1, 2, 2],
            [2, 4, 8],
            [3, 6, "?"]
        ],
        "options": ["16", "18", "20", "24"],
        "answer": "18"
    },
]


def start_timer():
    global timer_id, time_left, answered
    clearInterval(timer_id)
    time_left = 15

    def tick():
        global time_left, timer_id
        document.getElementById("timer").innerText = f"Time: {time_left}"
        time_left -= 1
        if time_left < 0:
            clearInterval(timer_id)
            document.getElementById("options").style.display = "none"
            document.getElementById("pattern-display").innerHTML = ""
            document.getElementById("pattern-instruction").innerText = ""
            document.getElementById("msg").innerText = "⏰ Time up!"
            document.getElementById("next").style.display = "block"

    timer_id = setInterval(create_proxy(tick), 1000)


def show_question():
    global answered
    answered = False
    current_q = selected_questions[current]

    document.getElementById("msg").innerText = ""
    document.getElementById("next").style.display = "none"
    document.getElementById("options").style.display = "block"
    
    document.getElementById("pattern-instruction").innerText = current_q["instruction"]
    
    # Render grid
    grid_html = "<table style='margin: 20px auto; border-collapse: collapse;'>"
    for row in current_q["grid"]:
        grid_html += "<tr>"
        for cell in row:
            grid_html += f"<td style='border: 1px solid #ccc; padding: 10px; text-align: center; width: 40px;'>{cell}</td>"
        grid_html += "</tr>"
    grid_html += "</table>"
    document.getElementById("pattern-display").innerHTML = grid_html

    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        opts[i].innerText = current_q["options"][i]
        opts[i].style.backgroundColor = ""
        opts[i].style.color = ""
        opts[i].style.borderColor = ""

    document.getElementById("question-number").innerText = f"Question {current + 1}/5"
    document.getElementById("progress-bar").style.width = f"{((current + 1) / 5) * 100}%"

    start_timer()


def choose_option(e):
    global answered, score, fast_answers, medium_answers, slow_answers
    if answered:
        return
    clearInterval(timer_id)
    answered = True

    user_choice = e.target.innerText
    correct = selected_questions[current]["answer"]

    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        opt_text = opts[i].innerText
        if opt_text == correct:
            opts[i].style.backgroundColor = "#0a2a0a"
            opts[i].style.borderColor = "#3ADD19"
            opts[i].style.color = "#3ADD19"
        elif opt_text == user_choice:
            opts[i].style.backgroundColor = "#2a0a0a"
            opts[i].style.borderColor = "#d2230f"
            opts[i].style.color = "#d2230f"

    if user_choice == correct:
        if time_left >= 10:
            score += 5
            fast_answers += 1
        elif time_left >= 5:
            score += 3
            medium_answers += 1
        else:
            score += 1
            slow_answers += 1

    document.getElementById("score-card").innerText = f"Score: {score}"
    document.getElementById("next").style.display = "block"


def next_q(e=None):
    global current, answered, games_completed
    clearInterval(timer_id)
    answered = False
    current += 1

    if current < 5:
        show_question()
    else:
        document.getElementById("pattern-display").innerHTML  = ""
        document.getElementById("pattern-instruction").innerText = ""
        document.getElementById("options").style.display      = "none"
        document.getElementById("next").style.display         = "none"
        document.getElementById("timer").style.display        = "none"
        document.getElementById("progress-bar-bg").style.display = "none"
        document.getElementById("msg").innerText              = "🎉 Pattern Master!"
        document.getElementById("question-number").innerText  = f"Final Score: {score}"

        games_completed += 1
        _update_games_completed_btn()

        document.getElementById("tick-reasoning").style.display = "inline"
        document.getElementById("play").disabled      = True
        document.getElementById("play").style.opacity = "0.5"


def start_game(e=None):
    global current, score, selected_questions
    global fast_answers, medium_answers, slow_answers

    current       = 0
    score         = 0
    fast_answers  = 0
    medium_answers = 0
    slow_answers  = 0

    selected_questions = random.sample(pattern_pool, 5)

    document.getElementById("score-card").innerText          = "Score: 0"
    document.getElementById("timer").style.display           = "block"
    document.getElementById("progress-bar-bg").style.display = "block"
    show_question()


opts = document.getElementsByClassName("opt")
for i in range(len(opts)):
    opts[i].addEventListener("click", create_proxy(choose_option))

document.getElementById("next").addEventListener("click", create_proxy(next_q))


score_2 = 0
fast_answers_2 = 0
medium_answers_2 = 0
slow_answers_2 = 0

selected_questions_2 = []
current_2 = 0
answered_2 = False
time_left_2 = 15
timer_id_2 = None

question_pool_2 = [
    {
        "question": "What number is missing? 2, 4, ?, 16, 32",
        "options": ["6", "8", "10", "12"],
        "answer": "8"
    },
    {
        "question": "Find the missing number: 5, 10, 17, 26, ?",
        "options": ["35", "36", "37", "38"],
        "answer": "37"
    },
    {
        "question": "What comes next? 100, 81, 64, 49, ?",
        "options": ["36", "25", "16", "40"],
        "answer": "36"
    },
    {
        "question": "Find the missing: 7, 14, 21, ?, 35",
        "options": ["26", "27", "28", "29"],
        "answer": "28"
    },
    {
        "question": "3, 9, 27, ?, 243",
        "options": ["54", "81", "72", "90"],
        "answer": "81"
    },
    {
        "question": "Missing number: 1, 1, 2, 3, 5, ?",
        "options": ["7", "8", "9", "10"],
        "answer": "8"
    },
    {
        "question": "6, 12, 20, 30, ?",
        "options": ["40", "42", "44", "45"],
        "answer": "42"
    },
    {
        "question": "Find missing: 144, 121, 100, 81, ?",
        "options": ["64", "60", "72", "56"],
        "answer": "64"
    },
    {
        "question": "2, 6, 12, 20, 30, ?",
        "options": ["40", "42", "44", "48"],
        "answer": "42"
    },
    {
        "question": "50, 45, 40, 35, ?",
        "options": ["25", "28", "30", "32"],
        "answer": "30"
    },
]


def start_timer_2():
    global timer_id_2, time_left_2, answered_2
    clearInterval(timer_id_2)
    time_left_2 = 15

    def tick_2():
        global time_left_2, timer_id_2
        document.getElementById("timer_2").innerText = f"Time: {time_left_2}"
        time_left_2 -= 1
        if time_left_2 < 0:
            clearInterval(timer_id_2)
            document.getElementById("options_2").style.display  = "none"
            document.getElementById("question_2").innerText     = ""
            document.getElementById("msg_2").innerText          = "⏰ Time up!"
            document.getElementById("next_2").style.display     = "block"

    timer_id_2 = setInterval(create_proxy(tick_2), 1000)


def show_question_2():
    global answered_2
    answered_2    = False
    current_q_2   = selected_questions_2[current_2]

    document.getElementById("msg_2").innerText        = ""
    document.getElementById("next_2").style.display   = "none"
    document.getElementById("options_2").style.display = "block"
    document.getElementById("question_2").innerText   = current_q_2["question"]

    opts_2 = document.getElementsByClassName("opt_2")
    for i in range(len(opts_2)):
        opts_2[i].innerText              = current_q_2["options"][i]
        opts_2[i].style.backgroundColor = ""
        opts_2[i].style.color            = ""
        opts_2[i].style.borderColor      = ""

    start_timer_2()


def choose_option_2(e):
    global answered_2, score_2, fast_answers_2, medium_answers_2, slow_answers_2
    if answered_2:
        return
    clearInterval(timer_id_2)
    answered_2    = True

    user_choice_2 = e.target.innerText
    correct_2     = selected_questions_2[current_2]["answer"]

    opts_2 = document.getElementsByClassName("opt_2")
    for i in range(len(opts_2)):
        opt_text = opts_2[i].innerText
        if opt_text == correct_2:
            opts_2[i].style.backgroundColor = "#0a2a0a"
            opts_2[i].style.borderColor      = "#3ADD19"
            opts_2[i].style.color            = "#3ADD19"
        elif opt_text == user_choice_2:
            opts_2[i].style.backgroundColor = "#2a0a0a"
            opts_2[i].style.borderColor      = "#d2230f"
            opts_2[i].style.color            = "#d2230f"

    if user_choice_2 == correct_2:
        if time_left_2 >= 10:
            score_2 += 5
            fast_answers_2 += 1
        elif time_left_2 >= 5:
            score_2 += 3
            medium_answers_2 += 1
        else:
            score_2 += 1
            slow_answers_2 += 1

    document.getElementById("score-card_2").innerText = f"Score: {score_2}"
    document.getElementById("next_2").style.display   = "block"


def next_q_2(e=None):
    global current_2, answered_2, games_completed
    clearInterval(timer_id_2)
    answered_2 = False
    current_2 += 1

    if current_2 < 5:
        show_question_2()
    else:
        document.getElementById("question_2").innerText        = "🎉 Quiz Finished!"
        document.getElementById("options_2").style.display     = "none"
        document.getElementById("next_2").style.display        = "none"
        document.getElementById("timer_2").style.display       = "none"

        games_completed += 1
        _update_games_completed_btn()

        document.getElementById("tick-missing").style.display      = "inline"
        document.getElementById("play-missing").disabled           = True
        document.getElementById("play-missing").style.opacity      = "0.5"


def start_game_2(e=None):
    global current_2, score_2, selected_questions_2
    global fast_answers_2, medium_answers_2, slow_answers_2

    current_2      = 0
    score_2        = 0
    fast_answers_2 = 0
    medium_answers_2 = 0
    slow_answers_2= 0

    selected_questions_2 = random.sample(question_pool_2, 5)

    document.getElementById("score-card_2").innerText = "Score: 0"
    document.getElementById("timer_2").style.display  = "block"
    show_question_2()


opts_2 = document.getElementsByClassName("opt_2")
for i in range(len(opts_2)):
    opts_2[i].addEventListener("click", create_proxy(choose_option_2))

document.getElementById("next_2").addEventListener("click", create_proxy(next_q_2))


def load_profile(e):
    global current_user
    document.getElementById("sectiontest").style.display    = "none"
    document.getElementById("section_profile").style.display = "block"

    if not current_user:
        return

    name  = getattr(current_user, "name",  "") or current_user["name"]  if isinstance(current_user, dict) else current_user.name
    age   = getattr(current_user, "age",   "") or ""
    ts    = int(getattr(current_user, "total_score",  0) or 0)
    tg    = int(getattr(current_user, "total_games",  0) or 0)
    fa    = int(getattr(current_user, "fast_answers",  0) or 0)
    ma    = int(getattr(current_user, "medium_answers",0) or 0)
    sa    = int(getattr(current_user, "slow_answers",  0) or 0)
    overall_acc = int(getattr(current_user, "accuracy", 0) or 0) 

    document.getElementById("profile-name").innerText  = name
    document.getElementById("profile-age").innerText   = f"Age: {age}"
    document.getElementById("iq_score").innerText      = str(ts)
    document.getElementById("games-played").innerText  = str(tg)
    document.getElementById("fast-answers").innerText  = str(fa)

    document.getElementById("accuracy").innerText = f"{overall_acc}%"
 
    # Display streak
    document.getElementById("streak").innerText = f"🔥 {tg}"

    if ts >= 40:
        badge = "🥇 Genius"
    elif ts >= 25:
        badge = "🥈 Smart Thinker"
    else:
        badge = "🥉 Rising Mind"

    badges_el = document.querySelector(".badges")
    if badges_el:
        badges_el.innerText = badge

document.getElementById("profile_status").addEventListener(
    "click", create_proxy(load_profile)
)


def section_scoreboard(_):
    document.getElementById("sectiontest").style.display       = "none"
    document.getElementById("sectionscoreboard").style.display = "block"
    scoreboard()

document.getElementById("games_completed").addEventListener(
    "click", create_proxy(section_scoreboard)
)


def scoreboard():
    global score, score_2, final_score, current_user
    global fast_answers, medium_answers, slow_answers
    global fast_answers_2, medium_answers_2, slow_answers_2

    if games_completed < 2:
        return

    final_score    = score + score_2
    total_fast     = fast_answers   + fast_answers_2
    total_medium   = medium_answers + medium_answers_2
    total_slow     = slow_answers   + slow_answers_2
    total_answered = total_fast + total_medium + total_slow

    document.getElementById("scoreboard_display").innerText = str(final_score)
    if total_answered > 0:
        instant_accuracy = round((total_fast / total_answered) * 100)
    else:
        instant_accuracy = 0
 
    document.getElementById("accuracy_scoreboard").innerText = f"{instant_accuracy}%"

    if final_score >= 40:
        badge_icon = "🥇"
        badge_name = "Genius"
    elif final_score >= 25:
        badge_icon = "🥈"
        badge_name = "Smart Thinker"
    else:
        badge_icon = "🥉"
        badge_name = "Rising Mind"

    document.getElementById("result-badge-icon").innerText = badge_icon
    document.getElementById("result-badge-name").innerText = badge_name

    async def save_and_rank():
        global current_user

        name = ""
        try:
            name = current_user.name
        except Exception:
            try:
                name = current_user["name"]
            except Exception:
                pass

        if not name:
            document.getElementById("result-rank").innerText = "N/A"
            return

        tg = 0
        try:
            tg = int(current_user.total_games or 0)
        except Exception:
            try:
                tg = int(current_user["total_games"] or 0)
            except Exception:
                pass
        tg += 1

        await window.updateScore(
            name,
            final_score,
            total_fast,
            total_medium,
            total_slow,
            tg
        )

        rank = await window.getUserRank(name)
        if rank:
            document.getElementById("result-rank").innerText = f"#{rank}"
        else:
            document.getElementById("result-rank").innerText = "—"

        try:
            current_user.total_score    = final_score
            current_user.fast_answers   = total_fast
            current_user.medium_answers = total_medium
            current_user.slow_answers   = total_slow
            current_user.total_games    = tg
        except Exception:
            pass

    asyncio.create_task(save_and_rank())


def _update_games_completed_btn():
    remaining = 2 - games_completed
    btn = document.getElementById("games_completed")
    if games_completed >= 2:
        btn.innerText        = "🏆 View your IQ Score"
        btn.disabled         = False
        btn.style.opacity    = "1"
    else:
        btn.innerText        = f"{remaining} more game(s) to go!"
        btn.disabled         = True
        btn.style.opacity    = "0.5"