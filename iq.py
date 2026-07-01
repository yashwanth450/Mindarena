from js import document, setInterval, clearInterval, window
from pyodide.ffi import create_proxy
import random
import asyncio


username_input = ""
age_input_value = ""
current_user = None
games_completed = 0
final_score = 0


def get_current_name():
    try:
        return current_user.name
    except Exception:
        try:
            return current_user["name"]
        except Exception:
            return ""
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
    if not age.isdigit():
        show_err("⚠️ Age must be a valid number")
        return
    age = int(age)

    if age <5  or age>100:
        show_err("⚠️ Please enter a valid age")
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
        window._currentUser = current_user

        _enter_test_section()
        document.getElementById("modal").classList.add("show")

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
    window._currentUser = result.user
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
    global games_completed,result
    games_completed = 0

    document.getElementById("sectionmain_page").style.display   = "none"
    document.getElementById("section_new_profile").style.display = "none"
    document.getElementById("section_login").style.display       = "none"
    document.getElementById("sectiontest").style.display         = "block"

    document.getElementById("games_completed").disabled    = True
    document.getElementById("games_completed").style.opacity = "0.4"
    document.getElementById("games_completed").innerText   = "complete 3 games to go.."

    document.getElementById("tick-pattern").style.display = "none"
    document.getElementById("tick-logic").style.display   = "none"
    document.getElementById("tick-number").style.display   = "none"
    document.getElementById("play-pattern").disabled        = False
    document.getElementById("play-pattern").style.opacity   = "1"
    document.getElementById("play-logic").disabled      = False
    document.getElementById("play-logic").style.opacity = "1"
    document.getElementById("play-number").disabled      = False
    document.getElementById("play-number").style.opacity = "1"
def reset_all_games():
    global games_completed
    global score, fast_answers, medium_answers, slow_answers, current, selected_questions, answered, timer_id
    global score_2, fast_answers_2, medium_answers_2, slow_answers_2, current_2, selected_questions_2, answered_2, timer_id_2
    global score_3, fast_answers_3, medium_answers_3, slow_answers_3, current_3, selected_questions_3, answered_3, timer_id_3

    # stop any running timers
    clearInterval(timer_id)
    clearInterval(timer_id_2)
    clearInterval(timer_id_3)

    # ---- reset game 1 (pattern) data ----
    score = 0
    fast_answers = medium_answers = slow_answers = 0
    current = 0
    selected_questions = []
    answered = False
    timer_id = None

    # ---- reset game 2 (logic) data ----
    score_2 = 0
    fast_answers_2 = medium_answers_2 = slow_answers_2 = 0
    current_2 = 0
    selected_questions_2 = []
    answered_2 = False
    timer_id_2 = None

    # ---- reset game 3 (number) data ----
    score_3 = 0
    fast_answers_3 = medium_answers_3 = slow_answers_3 = 0
    current_3 = 0
    selected_questions_3 = []
    answered_3 = False
    timer_id_3 = None

    games_completed = 0

    # ---- reset game 1 UI ----
    document.getElementById("score-card").innerText           = "Score: 0"
    document.getElementById("score-card").style.display       = "block"
    document.getElementById("question-number").style.display  = "block"
    document.getElementById("exit").style.display              = "block"
    document.getElementById("continue").style.display           = "none"
    document.getElementById("msg").innerText                    = ""
    document.getElementById("options").style.display            = "block"
    document.getElementById("timer").style.display              = "none"
    document.getElementById("progress-bar-bg").style.display    = "none"
    document.getElementById("pattern-display").innerHTML        = ""
    document.getElementById("pattern-instruction").innerText    = ""

    # ---- reset game 2 UI ----
    document.getElementById("score-card_2").innerText           = "Score: 0"
    document.getElementById("score-card_2").style.display       = "block"
    document.getElementById("question-number_2").style.display  = "block"
    document.getElementById("exit_2").style.display              = "block"
    document.getElementById("continue_2").style.display           = "none"
    document.getElementById("msg_2").innerText                    = ""
    document.getElementById("options_2").style.display            = "block"
    document.getElementById("timer_2").style.display              = "none"
    document.getElementById("progress-bar-bg_2").style.display    = "none"
    document.getElementById("question_2").innerText               = ""

    # ---- reset game 3 UI ----
    document.getElementById("score-card_3").innerText           = "Score: 0"
    document.getElementById("score-card_3").style.display       = "block"
    document.getElementById("question-number_3").style.display  = "block"
    document.getElementById("exit_3").style.display              = "block"
    document.getElementById("continue_3").style.display           = "none"
    document.getElementById("msg_3").innerText                    = ""
    document.getElementById("options_3").style.display            = "block"
    document.getElementById("timer_3").style.display              = "none"
    document.getElementById("progress-bar-bg_3").style.display    = "none"
    document.getElementById("question_3").innerText               = ""

    # ---- reset menu ticks / play buttons ----
    document.getElementById("tick-pattern").style.display = "none"
    document.getElementById("tick-logic").style.display   = "none"
    document.getElementById("tick-number").style.display  = "none"

    document.getElementById("play-pattern").disabled      = False
    document.getElementById("play-pattern").style.opacity = "1"
    document.getElementById("play-pattern").style.display = "block"

    document.getElementById("play-logic").disabled        = False
    document.getElementById("play-logic").style.opacity   = "1"
    document.getElementById("play-logic").style.display   = "block"

    document.getElementById("play-number").disabled       = False
    document.getElementById("play-number").style.opacity  = "1"
    document.getElementById("play-number").style.display  = "block"
def display_patternarena(e):
    async def check_limit():
        name = get_current_name()
        result = await window.getDailyPlayStatus(name)

        if not result.allowed:
            document.getElementById("games_completed").innerText = result.message
            document.getElementById("play-pattern").style.display = "none"
            
            document.getElementById("play-pattern").style.cursor = "not-allowed"
            document.getElementById("play-logic").style.display = "none"
            document.getElementById("play-logic").style.cursor = "not-allowed"
            document.getElementById("play-number").style.display = "none"
    
            document.getElementById("play-number").style.cursor = "not-allowed"

            document.getElementById("games_completed").innerText = result.message
            document.getElementById("games_completed").style.color = "red"
            document.getElementById("games_completed").style.opacity = "1"
            document.getElementById("games_completed").disabled = True
            return

        def go():
            document.getElementById("sectiontest").style.display      = "none"
            document.getElementById("sectionPatternArena").style.display = "block"
            start_game()

        window.showLoader_game(3000, create_proxy(go))

    asyncio.create_task(check_limit())


def display_logicclash(e):
    async def check_limit():
        global result
        name = get_current_name()
        result = await window.getDailyPlayStatus(name)

        if not result.allowed:
            document.getElementById("games_completed").innerText = result.message
            return

        def go():
            document.getElementById("sectiontest").style.display  = "none"
            document.getElementById("sectionLogicClash").style.display = "block"
            start_game_2()

        window.showLoader_game(3000, create_proxy(go))

    asyncio.create_task(check_limit())

def display_numberduel(e):
    async def check_limit():
        global result
        name = get_current_name()
        result = await window.getDailyPlayStatus(name)

        if not result.allowed:
            document.getElementById("games_completed").innerText = result.message
            return

        def go():
            document.getElementById("sectiontest").style.display  = "none"
            document.getElementById("sectionNumberDuel").style.display = "block"
            start_game_3()

        window.showLoader_game(3000, create_proxy(go))

    asyncio.create_task(check_limit())    
document.getElementById("play-pattern").addEventListener(
    "click", create_proxy(display_patternarena)
)

document.getElementById("play-logic").addEventListener(
    "click", create_proxy(display_logicclash)
)   
document.getElementById("play-number").addEventListener(
    "click", create_proxy(display_numberduel)
)     
def games_patternarena(_):
    document.getElementById("sectionPatternArena").style.display = "none"
    document.getElementById("sectiontest").style.display      = "block"

document.getElementById("exit").addEventListener(
    "click", create_proxy(games_patternarena)
)
document.getElementById("continue").addEventListener(
    "click", create_proxy(games_patternarena)
)


def games_logicclash(_):
    document.getElementById("sectionLogicClash").style.display = "none"
    document.getElementById("sectiontest").style.display    = "block"

document.getElementById("exit_2").addEventListener(
    "click", create_proxy(games_logicclash)
)
document.getElementById("continue_2").addEventListener(
    "click", create_proxy(games_logicclash)
)
def games_numberduel(_):
    document.getElementById("sectionNumberDuel").style.display = "none"
    document.getElementById("sectiontest").style.display    = "block"

document.getElementById("exit_2").addEventListener(
    "click", create_proxy(games_numberduel)
)
document.getElementById("continue_3").addEventListener(
    "click", create_proxy(games_numberduel)
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
    "instruction": "Find the missing figure.",
    "grid": [
      ["○", "□", "△"],
      ["□", "△", "○"],
      ["△", "○", "?"]
    ],
    "options": ["□", "△", "○", "◇"],
    "answer": "□"
  },
  {
    "type": "grid",
    "instruction": "Find the missing arrow.",
    "grid": [
      ["↑", "→", "↓"],
      ["→", "↓", "←"],
      ["↓", "←", "?"]
    ],
    "options": ["↑", "→", "↓", "←"],
    "answer": "↑"
  },
  {
    "type": "grid",
    "instruction": "Find the missing mirror image.",
    "grid": [
      ["◁", "▷", "◁"],
      ["▷", "◁", "▷"],
      ["◁", "▷", "?"]
    ],
    "options": ["◁", "▷", "△", "□"],
    "answer": "◁"
  },
  {
    "type": "grid",
    "instruction": "Find the missing shaded shape.",
    "grid": [
      ["□", "◩", "■"],
      ["◩", "■", "□"],
      ["■", "□", "?"]
    ],
    "options": ["□", "◩", "■", "▲"],
    "answer": "◩"
  },
  {
    "type": "grid",
    "instruction": "Find the missing size progression.",
    "grid": [
      ["◦", "○", "⬤"],
      ["○", "⬤", "◦"],
      ["⬤", "◦", "?"]
    ],
    "options": ["◦", "○", "⬤", "●"],
    "answer": "○"
  },
  {
    "type": "grid",
    "instruction": "Find the missing position pattern.",
    "grid": [
      ["●□□", "□●□", "□□●"],
      ["□●□", "□□●", "●□□"],
      ["□□●", "●□□", "?"]
    ],
    "options": ["□●□", "●□□", "□□●", "●●□"],
    "answer": "□●□"
  },
  {
    "type": "grid",
    "instruction": "Find the transformed figure.",
    "grid": [
      ["○", "⊙", "◉"],
      ["□", "▣", "◼"],
      ["△", "▲", "?"]
    ],
    "options": ["◉", "△", "▲", "◬"],
    "answer": "◬"
  },
  {
    "type": "grid",
    "instruction": "Find the missing nested shape.",
    "grid": [
      ["○", "⊙", "◉"],
      ["□", "▣", "◈"],
      ["△", "⟁", "?"]
    ],
    "options": ["◭", "△", "▲", "◉"],
    "answer": "◭"
  },
  {
    "type": "grid",
    "instruction": "Find the missing overlay.",
    "grid": [
      ["○", "□", "⊕"],
      ["△", "□", "⌂"],
      ["○", "△", "?"]
    ],
    "options": ["⊗", "⊕", "⌂", "◇"],
    "answer": "⊗"
  },
  {
    "type": "grid",
    "instruction": "Complete the shape addition.",
    "grid": [
      ["○", "+", "⊕"],
      ["□", "+", "▣"],
      ["△", "+", "?"]
    ],
    "options": ["⟁", "△", "▲", "◬"],
    "answer": "⟁"
  },

  {
    "type": "grid",
    "instruction": "Identify the missing direction based on pattern.",
    "grid": [
      ["→ ↓ ←"],
      ["↑ → ↓"],
      ["← ↑ ?"]
    ],
    "options": ["A) →", "B) ←", "C) ↑", "D) ↓"],
    "answer": "A"
  },
  {
    "type": "grid",
    "instruction": "Find the missing number using pattern rule.",
    "grid": [
      [1, 2, 3],
      [2, 3, 4],
      [3, 4, "?"]
    ],
    "options": ["A) 3", "B) 5", "C) 6", "D) 4"],
    "answer": "B"
  },
  {
    "type": "grid",
    "instruction": "Find the next element in the sequence.",
    "grid": [
      ["○"],
      ["○○"],
      ["○○○"],
      ["○○○○"],
      ["?"]
    ],
    "options": ["A) ○○○", "B) ○○○○○", "C) ○", "D) ○○"],
    "answer": "B"
  },
  {
    "type": "grid",
    "instruction": "Find the missing rotated shape.",
    "grid": [
      ["└", "┌", "┐"],
      ["┘", "?", "└"]
    ],
    "options": ["A) ┌", "B) ┐", "C) └", "D) ┘"],
    "answer": "A"
  },
  {
    "type": "grid",
    "instruction": "Find the missing mirrored element.",
    "grid": [
      ["A", "B", "C"],
      ["C", "B", "A"],
      ["A", "B", "?"]
    ],
    "options": ["A) A", "B) B", "C) C", "D) D"],
    "answer": "C"
  },
  {
    "type": "grid",
    "instruction": "Find next alternating pattern element.",
    "grid": [
      ["★", "✦", "★", "✦", "?"]
    ],
    "options": ["A) ★", "B) ✦", "C) ✧", "D) ✪"],
    "answer": "A"
  },
  {
    "type": "grid",
    "instruction": "Find next shading progression.",
    "grid": [
      ["○", "◔", "◑", "◕", "●", "?"]
    ],
    "options": ["A) ○", "B) ◔", "C) ●", "D) ◕"],
    "answer": "A"
  },
  {
    "type": "grid",
    "instruction": "Find the missing pair using combined logic.",
    "grid": [
      ["A1", "B2"],
      ["B2", "C3"],
      ["C3", "?"]
    ],
    "options": ["A) D3", "B) D4", "C) C4", "D) E4"],
    "answer": "B"
  },
  {
    "type": "grid",
    "instruction": "Find missing element in sequence.",
    "grid": [
      ["■", "□", "■■", "□□", "■■■", "□□□□", "?"]
    ],
    "options": ["A) ■", "B) □□□□", "C) ■■", "D) □"],
    "answer": "B"
  },
  {
    "type": "grid",
    "instruction": "Find missing number using row-column logic.",
    "grid": [
      [2, 4, 6],
      [3, 6, 9],
      [4, 8, "?"]
    ],
    "options": ["A) 10", "B) 11", "C) 12", "D) 14"],
    "answer": "C"
  }
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
            grid_html += f"<td style='border: 1px solid #ccc; padding: 10px; text-align: center; width: 40px; color:white;'>{cell}</td>"
        grid_html += "</tr>"
    grid_html += "</table>"
    document.getElementById("pattern-display").innerHTML = grid_html

    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        opts[i].innerText = current_q["options"][i]
        opts[i].style.backgroundColor = ""
        opts[i].style.color = ""
        opts[i].style.borderColor = ""

    document.getElementById("question-number").innerText = f"Question {current + 1}/7"
    document.getElementById("progress-bar").style.width = f"{((current + 1) / 7) * 100}%"

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

    if current < 7:
        show_question()
    else:
        document.getElementById("pattern-display").innerHTML  = ""
        document.getElementById("pattern-instruction").innerText = ""
        document.getElementById("options").style.display      = "none"
        document.getElementById("next").style.display         = "none"
        document.getElementById("timer").style.display        = "none"
        document.getElementById("progress-bar-bg").style.display = "none"
        document.getElementById("msg").innerText              = "🎉 Pattern Master!"
        document.getElementById("exit").style.display         = "none"
        document.getElementById("continue").style.display         = "block"
        document.getElementById("score-card").style.display         = "none"
        document.getElementById("question-number").style.display         = "none"  


        games_completed += 1
        _update_games_completed_btn()

        document.getElementById("tick-pattern").style.display = "inline"
        document.getElementById("play-pattern").style.display = "none"
        document.getElementById("play-pattern").style.opacity = "0.5"


def start_game(e=None):
    global current, score, selected_questions
    global fast_answers, medium_answers, slow_answers

    current       = 0
    score         = 0
    fast_answers  = 0
    medium_answers = 0
    slow_answers  = 0

    selected_questions = random.sample(pattern_pool, 7)

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
    document.getElementById("question-number_2").innerText = f"Question {current_2 + 1}/7"
    document.getElementById("progress-bar_2").style.width = f"{((current_2 + 1) / 7) * 100}%"    

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

    if current_2 < 7:
        show_question_2()
    else:
        document.getElementById("question_2").innerText        = "🎉 missing master"
        document.getElementById("options_2").style.display     = "none"
        document.getElementById("next_2").style.display        = "none"
        document.getElementById("exit_2").style.display        = "none"
        document.getElementById("timer_2").style.display       = "none"
        document.getElementById("progress-bar-bg_2").style.display = "none"
        document.getElementById("score-card_2").style.display         = "none"
        document.getElementById("question-number_2").style.display         = "none" 
        document.getElementById("continue_2").style.display         = "block"
        games_completed += 1
        _update_games_completed_btn()

        document.getElementById("tick-logic").style.display      = "inline"
        document.getElementById("play-logic").style.display      = "none"
        document.getElementById("play-logic").style.opacity      = "0.5"


def start_game_2(e=None):
    global current_2, score_2, selected_questions_2
    global fast_answers_2, medium_answers_2, slow_answers_2

    current_2      = 0
    score_2        = 0
    fast_answers_2 = 0
    medium_answers_2 = 0
    slow_answers_2= 0

    selected_questions_2 = random.sample(question_pool_2, 7)

    document.getElementById("score-card_2").innerText = "Score: 0"
    document.getElementById("timer_2").style.display  = "block"
    document.getElementById("progress-bar-bg_2").style.display = "block"
    show_question_2()


opts_2 = document.getElementsByClassName("opt_2")
for i in range(len(opts_2)):
    opts_2[i].addEventListener("click", create_proxy(choose_option_2))

document.getElementById("next_2").addEventListener("click", create_proxy(next_q_2))



score_3 = 0
fast_answers_3 = 0
medium_answers_3 = 0
slow_answers_3 = 0

selected_questions_3 = []
current_3 = 0
answered_3 = False
time_left_3 = 15
timer_id_3 = None

question_pool_3 = [
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


def start_timer_3():
    global timer_id_3, time_left_3, answered_3
    clearInterval(timer_id_3)
    time_left_3 = 15

    def tick_3():
        global time_left_3, timer_id_3
        document.getElementById("timer_3").innerText = f"Time: {time_left_3}"
        time_left_3 -= 1
        if time_left_3 < 0:
            clearInterval(timer_id_3)
            document.getElementById("options_3").style.display  = "none"
            document.getElementById("question_3").innerText     = ""
            document.getElementById("msg_3").innerText          = "⏰ Time up!"
            document.getElementById("next_3").style.display     = "block"

    timer_id_3 = setInterval(create_proxy(tick_3), 1000)


def show_question_3():
    global answered_3
    answered_3    = False
    current_q_3   = selected_questions_3[current_3]

    document.getElementById("msg_3").innerText        = ""
    document.getElementById("next_3").style.display   = "none"
    document.getElementById("options_3").style.display = "block"
    document.getElementById("question_3").innerText   = current_q_3["question"]

    opts_3 = document.getElementsByClassName("opt_3")
    for i in range(len(opts_3)):
        opts_3[i].innerText              = current_q_3["options"][i]
        opts_3[i].style.backgroundColor = ""
        opts_3[i].style.color            = ""
        opts_3[i].style.borderColor      = ""
    document.getElementById("question-number_3").innerText = f"Question {current_3 + 1}/6"
    document.getElementById("progress-bar_3").style.width = f"{((current_3 + 1) / 6) * 100}%"    

    start_timer_3()


def choose_option_3(e):
    global answered_3, score_3, fast_answers_3, medium_answers_3, slow_answers_3
    if answered_3:
        return
    clearInterval(timer_id_3)
    answered_3   = True

    user_choice_3 = e.target.innerText
    correct_3    = selected_questions_3[current_3]["answer"]

    opts_3 = document.getElementsByClassName("opt_3")
    for i in range(len(opts_3)):
        opt_text = opts_3[i].innerText
        if opt_text == correct_3:
            opts_3[i].style.backgroundColor = "#0a2a0a"
            opts_3[i].style.borderColor      = "#3ADD19"
            opts_3[i].style.color            = "#3ADD19"
        elif opt_text == user_choice_3:
            opts_3[i].style.backgroundColor = "#2a0a0a"
            opts_3[i].style.borderColor      = "#d2230f"
            opts_3[i].style.color            = "#d2230f"



    if user_choice_3 == correct_3:
        if time_left_3 >= 10:
            score_3 += 5
            fast_answers_3 += 1
        elif time_left_3 >= 5:
            score_3 += 3
            medium_answers_3 += 1
        else:
            score_3 += 1
            slow_answers_3 += 1

    document.getElementById("score-card_3").innerText = f"Score: {score_3}"
    document.getElementById("next_3").style.display   = "block"


def next_q_3(e=None):
    global current_3, answered_3, games_completed
    clearInterval(timer_id_3)
    answered_3 = False
    current_3 += 1

    if current_3 < 6:
        show_question_3()
    else:
        document.getElementById("question_3").innerText        = "🎉 missing master"
        document.getElementById("options_3").style.display     = "none"
        document.getElementById("next_3").style.display        = "none"
        document.getElementById("exit_3").style.display        = "none"
        document.getElementById("timer_3").style.display       = "none"
        document.getElementById("progress-bar-bg_3").style.display = "none"
        document.getElementById("score-card_3").style.display         = "none"
        document.getElementById("question-number_3").style.display         = "none" 
        document.getElementById("continue_3").style.display         = "block"
        games_completed += 1
        _update_games_completed_btn()

        document.getElementById("tick-number").style.display      = "inline"
        document.getElementById("play-number").style.display      = "none"
        document.getElementById("play-number").style.opacity      = "0.5"


def start_game_3(e=None):
    global current_3, score_3, selected_questions_3
    global fast_answers_3, medium_answers_3, slow_answers_3

    current_3      = 0
    score_3        = 0
    fast_answers_3 = 0
    medium_answers_3 = 0
    slow_answers_3= 0

    selected_questions_3 = random.sample(question_pool_3, 6)

    document.getElementById("score-card_3").innerText = "Score: 0"
    document.getElementById("timer_3").style.display  = "block"
    document.getElementById("progress-bar-bg_3").style.display = "block"
    show_question_3()


opts_3 = document.getElementsByClassName("opt_3")
for i in range(len(opts_3)):
    opts_3[i].addEventListener("click", create_proxy(choose_option_3))

document.getElementById("next_3").addEventListener("click", create_proxy(next_q_3))


def load_profile(e):
    global total_score,total_games,fast_answers,medium_answers,slow_answers,accuracy
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

    max = 100 * tg
    if max == 0:
      avg_iq = 0
    else:
     raw =(fa * 6.5) +(ma * 5) +(sa * 3.5)
     performance = raw / max
     avg_iq = round(100 + (performance - 0.5) * 60)

    document.getElementById("profile-name").innerText  = name
    document.getElementById("profile-age").innerText   = f"{age}"
    document.getElementById("profile-iqscore").innerText  =str(avg_iq)
    document.getElementById("games-played").innerText  = str(tg)
    document.getElementById("fast-answers").innerText  = str(fa)
    document.getElementById("correct-answers").innerText  = (fa+ma+sa)
    document.getElementById("xp").innerText  = f"{ts} XP"
    async def set_profile_rank():
     rank = await window.getUserRank(name)
     if rank:
        document.getElementById("profile-rank").innerText = f"#{rank}"
     else:
        document.getElementById("profile-rank").innerText = "N/A"

    document.getElementById("profile-rank").innerText = "..."
    asyncio.create_task(set_profile_rank())
    if tg == 0:
      document.getElementById("accuracy").innerText = "0%"
    else:
     fast_acc   = (fa /20*tg)*100
     medium_acc = (ma / 20*tg)*100
     slow_acc   = (sa / 20*tg)*100
     overall_accuracy = round (0.5 * fast_acc + 0.3 * medium_acc + 0.2 * slow_acc)
     document.getElementById("accuracy").innerText = f"{(overall_accuracy)}%"

    if ts >= 75 and overall_acc >= 98:
      document.getElementById("profile-badge").innerText =  "Mastermind"
      document.getElementById("profile-quote").innerText =  "Champion Mind Activated."

    elif ts >= 50 and overall_acc >= 95:
       document.getElementById("profile-badge").innerText ="Elite Mind";
       document.getElementById("profile-quote").innerText =  "Pure Genius Energy."
    elif ts >= 35 and overall_acc >= 90:
      document.getElementById("profile-badge").innerText = "Genius";
      document.getElementById("profile-quote").innerText = "Great Progress Ahead."
    elif ts >= 20 and overall_acc >= 80:
       document.getElementById("profile-badge").innerText = "Strategist";
       document.getElementById("profile-quote").innerText = "Keep Climbing Higher."
    elif ts >= 10 and overall_acc >= 70:
        document.getElementById("profile-badge").innerText = "Thinker";
        document.getElementById("profile-quote").innerText = "Keep Training Daily."
    elif ts >= 5 and overall_acc >= 60:
       document.getElementById("profile-badge").innerText = "Learner";
       document.getElementById("profile-quote").innerText =  "Think Beyond Limits."
    elif ts >= 1:
       document.getElementById("profile-badge").innerText = "Rising Mind";
       document.getElementById("profile-quote").innerText =  "Every Answer Counts."
    else:
       document.getElementById("profile-badge").innerText = "No Badge"; 
       document.getElementById("profile-quote").innerText = "Stay Hungry. Think."
    
       
window._load_profile_proxy = create_proxy(load_profile)  
reset_all_games()      


def section_scoreboard(_):
    document.getElementById("sectiontest").style.display       = "none"
    document.getElementById("sectionscoreboard").style.display = "block"
    scoreboard()

document.getElementById("games_completed").addEventListener(
    "click", create_proxy(section_scoreboard)
)

def scoreboard():
    global score, score_2, final_score, current_user,score_3
    global fast_answers, medium_answers, slow_answers
    global fast_answers_2, medium_answers_2, slow_answers_2
    global fast_answers_3, medium_answers_3, slow_answers_3,overall_accuracy,avg_iq

    if games_completed < 3:
        return

    final_score    = score + score_2+ score_3
    total_fast     = fast_answers   + fast_answers_2 + fast_answers_3
    total_medium   = medium_answers + medium_answers_2 + medium_answers_3
    total_slow     = slow_answers   + slow_answers_2 + slow_answers_3
    total_answered = total_fast + total_medium + total_slow

    total = total_fast + total_medium + total_slow
    if total == 0:
        instant_accuracy = 0
    else:    

       fast_acc   = (total_fast /total)*100
       medium_acc = (total_medium / total)*100
       slow_acc   = (total_slow / total)*100
       instant_accuracy = round (0.5 * fast_acc + 0.3 * medium_acc + 0.2 * slow_acc)

    document.getElementById("scoreboard_display").innerText = str(final_score)
    document.getElementById("accuracy_scoreboard").innerText = f"{instant_accuracy}%"
    document.getElementById("fastanswers_scoreboard").innerText = str(total_fast)

  
    document.getElementById("accuracy-bar").style.setProperty("--bar-w", f"{instant_accuracy}%")
    document.getElementById("fast-bar").style.setProperty("--bar-w", f"{min(total_fast * 20, 100)}%")
    document.getElementById("score-bar").style.setProperty("--bar-w", f"{min(final_score * 2, 100)}%")

    if total_answered>0:
     max = 100 
     raw =(total_fast * 6.5) +(total_medium * 5) +(total_slow * 3.5)
     performance = raw / max
     instant_iq = round(100 + (performance - 0.5) * 60)
     document.getElementById("instant_iq_score").innerText = round(instant_iq)

    

    if total_fast == 20:
        document.getElementById("answer_speed").innerText = "⚡100%"
    elif total_fast >= 15:
        document.getElementById("answer_speed").innerText = "⚡75%"
    elif total_fast >= 10:
        document.getElementById("answer_speed").innerText = "⚡50%"
    elif total_fast >= 5:
        document.getElementById("answer_speed").innerText = "⚡15%"
    elif total_fast >= 1:
        document.getElementById("answer_speed").innerText = "⚡5%"
    else:
        document.getElementById("answer_speed").innerText = "⚡0%"

 
    if final_score >= 70:
        document.getElementById("compliment").innerText = "Great minds aren't born—they're built. Today, you've proven your potential."
        document.getElementById("badge_scoreboard").innerText = "🥇 Genius"
    elif final_score >= 40:
        document.getElementById("compliment").innerText = "You're climbing fast. Stay consistent and the leaderboard will soon know your name."
        document.getElementById("badge_scoreboard").innerText = "🥈 Smart Thinker"
    else:
        document.getElementById("compliment").innerText = "Success isn't measured by one game. Every attempt makes you smarter than yesterday."
        document.getElementById("badge_scoreboard").innerText = "🥉 Rising Mind"

  
    async def save_and_rank():
        global current_user
        name = ""
        try:
            name = current_user.name
        except:
            try:
                name = current_user["name"]
            except:
                pass

        if not name:
            document.getElementById("result-rank").innerText = "N/A"
            return

        tg = 0
        try:
            tg = int(current_user.total_games or 0)
        except:
            try:
                tg = int(current_user["total_games"] or 0)
            except:
                pass
        tg += 1

     
        limit_result = await window.increaseDailyPlay(name)

        if not limit_result.allowed:
            document.getElementById("compliment").innerText = str(limit_result.message)
            return

        await window.updateScore(
            name,
            final_score,
            total_fast,
            total_medium,
            total_slow,
            tg,
            instant_accuracy
            
        )
        # Get rank
        rank = await window.getUserRank(name)
        if rank:
            document.getElementById("result-rank").innerText = f"#{rank}"
        else:
            document.getElementById("result-rank").innerText = "—"

    asyncio.create_task(save_and_rank())

def exit_scoreboard(_):
    document.getElementById("sectionscoreboard").style.display       = "none"
    document.getElementById("section_login").style.display = "block"
    document.getElementById("modal-scoreboard").classList.add("show")
    reset_all_games()

document.getElementById("exit_scoreboard").addEventListener(
    "click", create_proxy(exit_scoreboard)
)    

def _update_games_completed_btn():
    remaining = 3 - games_completed
    btn = document.getElementById("games_completed")
    if games_completed >= 3:
        btn.innerText        = "🏆 View your IQ Score"
        btn.disabled         = False
        btn.style.opacity    = "1"
    else:
        btn.innerText        = f"{remaining} more game(s) to go!"
        btn.disabled         = True
        btn.style.opacity    = "0.5"
window._pythonReady = True        