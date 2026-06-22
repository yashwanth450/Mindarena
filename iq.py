from js import document, setInterval, clearInterval,window
from pyodide.ffi import create_proxy
import random

def username(e):
    global username_input, age_input_value
    name_input = document.getElementById("name")
    age_input = document.getElementById("age")
    name = name_input.value.strip()
    age = age_input.value.strip()
   
    def handle_error(input_element, error_id, message):
        existing_error = document.getElementById(error_id)
        if existing_error:
            existing_error.remove()
        err = document.createElement("p")
        err.id = error_id
        err.innerText = message
        err.style.color = "#eb0a0a"
        err.style.fontSize = "15px"
        err.style.marginTop = "5px"
        err.style.backgroundColor = "white"
        err.style.padding = "5px"
        err.style.borderRadius = "5px"
        input_element.parentNode.insertBefore(err, input_element.nextSibling)

    def clear_error(error_id):
        existing_error = document.getElementById(error_id)
        if existing_error:
            existing_error.remove()

    name_valid = True
    if not name:
        handle_error(name_input, "name-err", "⚠️ Please enter your name")
        name_valid = False
    elif not name.replace(" ", "").isalpha():
        handle_error(name_input, "name-err", "⚠️ Name should have alphabets only!")
        name_valid = False
    elif len(name) < 4:
        handle_error(name_input, "name-err", "⚠️ Name should be at least 4 characters long!")
        name_valid = False
    else:
        clear_error("name-err")

    age_valid = True
    if not age:
        handle_error(age_input, "age-err", "⚠️ Please enter your age")
        age_valid = False
    elif not age.isdigit():
        handle_error(age_input, "age-err", "⚠️ Age should be a number only! Example: 17")
        age_valid = False
    elif not (10 <= int(age) <= 30):
        handle_error(age_input, "age-err", "⚠️ Age should be between 10 and 30 years!")
        age_valid = False
    else:
        clear_error("age-err")

    if name_valid and age_valid:

         username_input = name.upper()
         age_input_value = age.upper()
         window.saveUser(username_input, age_input_value)
       
         
         def go():
          global games_completed

          games_completed = 0

          document.getElementById("display-username").innerText = f" {username_input}"

          document.getElementById("sectionlogin").style.display = "none"
          document.getElementById("sectiontest").style.display = "block"

          document.getElementById("games_completed").innerText = "2 more to go!"
          document.getElementById("games_completed").disabled = True
          document.getElementById("games_completed").style.opacity = "0.5"

          document.getElementById("play").disabled = False
          document.getElementById("play").style.opacity = "1"

          document.getElementById("play-missing").disabled = False
          document.getElementById("play-missing").style.opacity = "1"

          document.getElementById("tick-reasoning").style.display = "none"
          document.getElementById("tick-missing").style.display = "none"
         window.showLoader(5000, create_proxy(go))


btn = document.getElementById("btn")
btn.addEventListener("click", create_proxy(username))
def home(_):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionlogin").style.display = "block"

back = document.getElementById("back")
back.addEventListener("click", create_proxy(home))
def display_reasoning(e):

    def go():
        document.getElementById("sectiontest").style.display = "none"
        document.getElementById("sectionReasoning").style.display = "block"
        start_game()

    window.showLoader_game(3000, create_proxy(go))  

play = document.getElementById("play")
play.addEventListener("click", create_proxy(display_reasoning))

def display_missing(e):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionmissing").style.display = "block"
    start_game_2()
play2 = document.getElementById("play-missing")
play2.addEventListener("click", create_proxy(display_missing))

def games_reasoning(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit1 = document.getElementById("exit")
exit1.addEventListener("click", create_proxy(games_reasoning))

def games_missing(_):
    document.getElementById("sectionmissing").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit2 = document.getElementById("exit_2")
exit2.addEventListener("click", create_proxy(games_missing))
def section_scoreboard(_):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionscoreboard").style.display = "block"
    scoreboard()
view = document.getElementById("games_completed")
view.addEventListener("click", create_proxy(section_scoreboard))

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
            [5,  10, 15],
            [2,  4,  "?"]
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
        "type": "shape",
        "instruction": "What shape comes next?",
        "shapes": ["circle", "square", "triangle", "?"],
        "options": ["circle", "square", "triangle", "diamond"],
        "answer": "circle"
    },
    {
        "type": "shape",
        "instruction": "What shape comes next?",
        "shapes": ["triangle", "triangle", "square", "square", "?"],
        "options": ["triangle", "circle", "square", "diamond"],
        "answer": "circle"
    },
    {
        "type": "shape",
        "instruction": "What shape comes next?",
        "shapes": ["circle", "circle", "triangle", "circle", "circle", "?"],
        "options": ["circle", "square", "triangle", "diamond"],
        "answer": "triangle"
    },
    {
        "type": "shape",
        "instruction": "What shape comes next?",
        "shapes": ["square", "diamond", "square", "diamond", "?"],
        "options": ["triangle", "circle", "square", "diamond"],
        "answer": "square"
    },
    {
        "type": "color",
        "instruction": "What color comes next?",
        "colors": ["#ff4444", "#ff8800", "#ffd700", "#44ff44", "?"],
        "options": ["#ff4444", "#00aaff", "#aa44ff", "#ff44aa"],
        "option_labels": ["Red", "Blue", "Purple", "Pink"],
        "answer": "Blue",
        "answer_color": "#00aaff"
    },
    {
        "type": "color",
        "instruction": "What color comes next?",
        "colors": ["#ff4444", "#ff4444", "#0044ff", "#0044ff", "?"],
        "options": ["#ff4444", "#0044ff", "#ffd700", "#44ff44"],
        "option_labels": ["Red", "Blue", "Yellow", "Green"],
        "answer": "Red",
        "answer_color": "#ff4444"
    },
    {
        "type": "color",
        "instruction": "What color comes next?",
        "colors": ["#ffd700", "#888888", "#ffd700", "#888888", "?"],
        "options": ["#888888", "#ffd700", "#ff4444", "#00aaff"],
        "option_labels": ["Grey", "Gold", "Red", "Blue"],
        "answer": "Gold",
        "answer_color": "#ffd700"
    },
]

selected_questions = []
current = 0
answered = False
time_left = 15
timer_id = None
score = 0
fast_answers = 0
medium_answers = 0
slow_answers = 0


def render_pattern(q):
    """Renders the pattern into the pattern-display div based on question type"""
    display = document.getElementById("pattern-display")
    display.innerHTML = ""  

    if q["type"] == "grid":
        html = "<table class='pattern-grid'>"
        for row in q["grid"]:
            html += "<tr>"
            for cell in row:
                if cell == "?":
                    html += "<td class='missing'>?</td>"
                else:
                    html += f"<td>{cell}</td>"
            html += "</tr>"
        html += "</table>"
        display.innerHTML = html

    elif q["type"] == "shape":
        html = "<div class='shape-row'>"
        for i, shape in enumerate(q["shapes"]):
            if shape == "?":
                html += """
                <div class='shape-box missing'>
                    <svg width='44' height='44' viewBox='0 0 44 44'>
                        <text x='22' y='30' text-anchor='middle'
                        fill='#ffd700' font-size='24' font-weight='bold'>?</text>
                    </svg>
                </div>"""
            else:
                html += f"<div class='shape-box'>{get_svg(shape)}</div>"
            if i < len(q["shapes"]) - 1:
                html += "<span class='shape-arrow'>→</span>"
        html += "</div>"
        display.innerHTML = html

    elif q["type"] == "color":
        # Build color circles
        html = "<div class='color-row'>"
        for color in q["colors"]:
            if color == "?":
                html += "<div class='color-circle missing'>?</div>"
            else:
                html += f"<div class='color-circle' style='background:{color};'></div>"
        html += "</div>"
        display.innerHTML = html


def get_svg(shape):
    """Returns SVG string for a given shape name"""
    svgs = {
        "circle": "<svg width='44' height='44' viewBox='0 0 44 44'><circle cx='22' cy='22' r='17' fill='none' stroke='#ffd700' stroke-width='3'/></svg>",
        "square": "<svg width='44' height='44' viewBox='0 0 44 44'><rect x='5' y='5' width='34' height='34' fill='none' stroke='#ffd700' stroke-width='3'/></svg>",
        "triangle": "<svg width='44' height='44' viewBox='0 0 44 44'><polygon points='22,4 40,40 4,40' fill='none' stroke='#ffd700' stroke-width='3'/></svg>",
        "diamond": "<svg width='44' height='44' viewBox='0 0 44 44'><polygon points='22,4 40,22 22,40 4,22' fill='none' stroke='#ffd700' stroke-width='3'/></svg>",
    }
    return svgs.get(shape, "")


def render_options(q):
    """Renders option buttons based on question type"""
    opts = document.getElementsByClassName("opt")
    options = q["options"]

    for i in range(len(opts)):
        if q["type"] == "shape":
            opts[i].innerHTML = get_svg(options[i])
            opts[i].setAttribute("data-value", options[i])
        elif q["type"] == "color":
            label = q["option_labels"][i]
            color = options[i]
            opts[i].innerHTML = f"<div style='width:18px;height:18px;border-radius:50%;background:{color};border:1px solid rgba(255,255,255,0.2);'></div> {label}"
            opts[i].setAttribute("data-value", label)
        else:
            opts[i].innerHTML = options[i]
            opts[i].setAttribute("data-value", options[i])

        opts[i].style.backgroundColor = ""
        opts[i].style.color = ""
        opts[i].style.borderColor = ""


def start_timer():
    global timer_id, time_left, answered
    clearInterval(timer_id)
    time_left = 15

    def tick():
        global time_left, timer_id
        document.getElementById("timer").innerText = f"Time:{time_left}"
        time_left -= 1
        if time_left < 0:
            clearInterval(timer_id)
            document.getElementById("options").style.display = "none"
            document.getElementById("pattern-display").innerHTML = ""
            document.getElementById("msg").innerText = "Time up Buddy! ⏰"
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

    render_pattern(current_q)
    render_options(current_q)

    document.getElementById("question-number").innerText = f"{current + 1} of 5"
    progress = (current / 5) * 100
    document.getElementById("progress-bar").style.width = f"{progress}%"

    start_timer()


def choose_option(e):
    global answered, score, fast_answers, medium_answers, slow_answers

    if answered:
        return

    clearInterval(timer_id)
    answered = True

    current_q = selected_questions[current]

    user_choice = e.target.getAttribute("data-value")
    if not user_choice:
       
        user_choice = e.target.parentElement.getAttribute("data-value")

    correct = current_q["answer"]

  
    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        val = opts[i].getAttribute("data-value")
        if val == correct:
            opts[i].style.backgroundColor = "#0a2a0a"
            opts[i].style.borderColor = "#3ADD19"
            opts[i].style.color = "#3ADD19"
        elif val == user_choice:
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
    global current, answered, score, games_completed
    clearInterval(timer_id)
    answered = False
    current += 1

    if current < 5:
        show_question()
    else:
        document.getElementById("pattern-display").innerHTML = ""
        document.getElementById("pattern-instruction").innerText = ""
        document.getElementById("options").style.display = "none"
        document.getElementById("next").style.display = "none"
        document.getElementById("timer").style.display = "none"
        document.getElementById("progress-bar-bg").style.display = "none"
        document.getElementById("msg").innerText = "Pattern Master! 🎉"
        document.getElementById("question-number").innerText = f"Final Score: {score}"

        games_completed += 1
        if games_completed == 2:
            document.getElementById("games_completed").innerText = "View your IQ score"
            document.getElementById("games_completed").disabled = False
            document.getElementById("games_completed").style.opacity = "1"
        else:
            document.getElementById("games_completed").innerText = str(2 - games_completed) + " more to go!"
            document.getElementById("games_completed").disabled = True
            document.getElementById("games_completed").style.opacity = "0.5"

        document.getElementById("tick-reasoning").style.display = "inline"
        document.getElementById("play").disabled = True
        document.getElementById("play").style.opacity = "0.5"


def start_game(e=None):
    global current, score, selected_questions
    global fast_answers, medium_answers, slow_answers

    current = 0
    score = 0
    fast_answers = 0
    medium_answers = 0
    slow_answers = 0

    # Pick 5 random questions from pool
    selected_questions = random.sample(pattern_pool, 5)

    document.getElementById("score-card").innerText = "Score: 0"
    document.getElementById("timer").style.display = "block"
    document.getElementById("progress-bar-bg").style.display = "block"
    show_question()


opts = document.getElementsByClassName("opt")
for i in range(len(opts)):
    opts[i].addEventListener("click", create_proxy(choose_option))

document.getElementById("next").addEventListener("click", create_proxy(next_q))

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

selected_questions_2 = []
current_2 = 0
answered_2 = False
time_left_2 = 15
timer_id_2 = None
score_2 = 0
fast_answers_2 = 0
medium_answers_2 = 0
slow_answers_2 = 0


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
            document.getElementById("options_2").style.display = "none"
            document.getElementById("question_2").innerText = ""
            document.getElementById("msg_2").innerText = "Time up Buddy!⏰"
            document.getElementById("next_2").style.display = "block"

    timer_id_2 = setInterval(create_proxy(tick_2), 1000)


def show_question_2():
    global answered_2
    answered_2 = False

    current_q_2 = selected_questions_2[current_2]

    document.getElementById("msg_2").innerText = ""
    document.getElementById("next_2").style.display = "none"
    document.getElementById("options_2").style.display = "block"
    document.getElementById("question_2").innerText = current_q_2["question"]

    opts_2 = document.getElementsByClassName("opt_2")
    for i in range(len(opts_2)):
        opts_2[i].innerText = current_q_2["options"][i]
        opts_2[i].style.backgroundColor = ""
        opts_2[i].style.color = ""

    start_timer_2()


def choose_option_2(e):
    global answered_2, score_2, fast_answers_2, medium_answers_2, slow_answers_2

    if answered_2:
        return

    clearInterval(timer_id_2)
    answered_2 = True

    user_choice_2 = e.target.innerText
    correct_2 = selected_questions_2[current_2]["answer"]

    opts_2 = document.getElementsByClassName("opt_2")
    for i in range(len(opts_2)):
        option_text_2 = opts_2[i].innerText
        if option_text_2 == correct_2:
            opts_2[i].style.backgroundColor = "#3ADD19"
            opts_2[i].style.color = "white"
        elif option_text_2 == user_choice_2:
            opts_2[i].style.backgroundColor = "#d2230f"
            opts_2[i].style.color = "white"

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
    document.getElementById("next_2").style.display = "block"


def next_q_2(e=None):
    global current_2, answered_2, score_2, games_completed
    clearInterval(timer_id_2)
    answered_2 = False
    current_2 += 1

    if current_2 < 5: 
        show_question_2()
    else:
        document.getElementById("question_2").innerText = "Quiz Finished 🎉"
        document.getElementById("options_2").style.display = "none"
        document.getElementById("next_2").style.display = "none"
        document.getElementById("timer_2").style.display = "none"
        
        games_completed += 1
        if games_completed == 2:
            document.getElementById("games_completed").innerText = "View your IQ score"
            document.getElementById("games_completed").disabled = False
            document.getElementById("games_completed").style.opacity = "1"
        else:
            document.getElementById("games_completed").innerText = str(2 - games_completed) + " more to go!"
            document.getElementById("games_completed").disabled = True
            document.getElementById("games_completed").style.opacity = "0.5"

        document.getElementById("tick-missing").style.display = "inline"
        document.getElementById("play-missing").disabled = True
        document.getElementById("play-missing").style.opacity = "0.5"


def start_game_2(e=None):
    global current_2, score_2, selected_questions_2
    global fast_answers_2, medium_answers_2, slow_answers_2

    current_2 = 0
    score_2 = 0
    fast_answers_2 = 0
    medium_answers_2 = 0
    slow_answers_2 = 0


    selected_questions_2 = random.sample(question_pool_2, 5)

    document.getElementById("score-card_2").innerText = f"Score: {score_2}"
    document.getElementById("timer_2").style.display = "block"
    show_question_2()


opts_2 = document.getElementsByClassName("opt_2")
for i in range(len(opts_2)):
    opts_2[i].addEventListener("click", create_proxy(choose_option_2))

document.getElementById("next_2").addEventListener("click", create_proxy(next_q_2))
def scoreboard():
    global score, score_2,username_input,age_input_value,final_score
    final_score = score + score_2
    document.getElementById("scoreboard_display").innerText = f"Your Final Score: {final_score}"
  
