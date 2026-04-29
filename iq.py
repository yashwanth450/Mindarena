from js import document, setInterval, clearInterval
from pyodide.ffi import create_proxy

def username(e):
    # 1. Get the inputs and values
    name_input = document.getElementById("name")
    age_input = document.getElementById("age")
    name = name_input.value.strip()
    age = age_input.value.strip()
     # 2. Helper function to show/remove errors
    def handle_error(input_element, error_id, message):
        existing_error = document.getElementById(error_id)
        if not input_element.value.strip():
            if not existing_error:
                # Create a new error paragraph
                err = document.createElement("p")
                err.id = error_id
                err.innerText = message
                err.style.color = "#eb0a0a"
                err.style.fontSize = "15px"
                err.style.marginTop = "5px"
                err.style.fontfamily = "Arial, sans-serif"
                err.style.fontweight = "bold"
                err.style.backgroundColor = "white"
                err.style.padding = "5px"
                err.style.borderRadius = "5px"
                
                input_element.parentNode.insertBefore(err, input_element.nextSibling)
            return False 
        else:
            if existing_error:
                existing_error.remove()
            return True # Validation passed

    # 3. Run validation for both fields
    name_valid = handle_error(name_input, "name-err", "⚠️ Please enter your name")
    age_valid = handle_error(age_input, "age-err", "⚠️ Please enter your age")

    if name_valid and age_valid:
        document.getElementById("display-username").innerText = f" {name}".upper()
        document.getElementById("sectionlogin").style.display = "none"
        document.getElementById("sectiontest").style.display = "block"


btn = document.getElementById("btn")
btn.addEventListener("click", create_proxy(username))

def home(_):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionlogin").style.display = "block"
back=document.getElementById("back")
back.addEventListener("click", create_proxy(home))

def display_reasoning(sectionReasoning):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
    start_game()
play=document.getElementById("play")
play.addEventListener("click", create_proxy(display_reasoning))


def display_missing(sectionmissing):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionmissing").style.display = "block"
    start_game_2()
play=document.getElementById("play-missing")
play.addEventListener("click", create_proxy(display_missing))

def games_reasoning(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit=document.getElementById("exit")
exit.addEventListener("click", create_proxy(games_reasoning))


def games_missing(_):
    document.getElementById("sectionmissing").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit=document.getElementById("exit_2")
exit.addEventListener("click", create_proxy(games_missing))


questions = [ """Tanya is older than Eric.
                 Cliff is older than Tanya.
                 Eric is older than Cliff.
                 If the first two statements are true, the third statement is """,
             """ If 12$34 = 10, 2$9 = 11 then what is the value of 6$27 = ?""",
             """If in a certain code, RAIN is written as 81#4 and CLOUD is written as 92#6, how will WIND be written?""",
                "2, 6, 7, 21, 22, ?",
                "1, 1, 2, 3, 5, 8, ?",
                 "3, 9, 27, 81, ?",
                 "4, 6, 9, 13, 18, ?",
                "If CAT = 24, DOG = 26, then BAT = ?",
                  "Find missing: 2, 10, 12, 60, 62, ?",
                "What comes next: Z, X, U, Q, ?",
                "If 5x = 20, then x = ?",
                 "A number doubled is 50. What is the number?",
                 "If 12 + 15 = 33, 13 + 16 = 35, then 14 + 17 = ?",
                "Which number is odd one out?",
               "Which word is different?",
                  "If all Bloops are Razzies and all Razzies are Lazzies, then all Bloops are?"
                ]

options_list = [
    ["False", "True", "Uncertain", "No Enough Information"],
    ["33", "15", "20", "10"],
    ["71#6", "92#5", "91#5", "82#"],
    ["44", "66", "23", "11"],
    ["11", "13", "10", "15"],
    ["162", "243", "108", "324"],
    ["22", "23", "24", "25"],
    ["21", "23", "25", "27"],
    ["300", "310", "320", "360"],
    ["M", "N", "O", "L"],
    ["2", "3", "4", "5"],
    ["20", "25", "30", "15"],
    ["37", "36", "38", "39"],
    ["121", "144", "169", "145"],
    ["Apple", "Banana", "Carrot", "Mango"],
    ["Lazzies", "Not Lazzies", "Some Lazzies", "None"]
]

answers=["False","33","91#5","66", "13", "243", "24", "23", "310", "M", "4", "25", "37", "145", "Carrot", "Lazzies"]

current = 0
answered = False
time_left = 15
timer_id = None
score=0

def start_timer():
    global timer_id, time_left, answered

    clearInterval(timer_id)
    time_left = 15

    def tick():
        global time_left,timer_id


        document.getElementById("timer").innerText = f"Time: {time_left}"

        time_left -= 1

        if time_left < 0:
          clearInterval(timer_id)
            
          document.getElementById("options").style.display = "none"
          document.getElementById("question").innerText = ""
          document.getElementById("msg").innerText = "Time up Buddy!⏰"
          document.getElementById("next").style.display = "block"

    timer_id = setInterval(create_proxy(tick), 1000)
def show_question():
    global answered

    answered = False

    document.getElementById("msg").innerText = ""
    document.getElementById("next").style.display = "none"
    document.getElementById("options").style.display = "block"
    document.getElementById("question").innerText = questions[current]

    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        opts[i].innerText = options_list[current][i]
        opts[i].style.backgroundColor = ""

    start_timer()
def choose_option(e):
    global answered, score

    if answered:
        return

    clearInterval(timer_id)
    answered = True

    user_choice = e.target.innerText
    correct = answers[current]

    opts = document.getElementsByClassName("opt")

    for i in range(len(opts)):
        option_text = opts[i].innerText

        if option_text == correct:
            # ✅ correct answer → always green
            opts[i].style.backgroundColor = "#3ADD19"
            opts[i].style.color = "white"

        elif option_text == user_choice:
            # ❌ wrong selected → red
            opts[i].style.backgroundColor = "#d2230f"
            opts[i].style.color = "white"
    if user_choice == correct:
         score += 1
    document.getElementById("score-card").innerText = f"Score: {score}"
    document.getElementById("next").style.display = "block"
def time_up():
    global answered

    if answered:
        return

    answered = True
    clearInterval(timer_id)

    document.getElementById("options").style.display = "none"
    document.getElementById("question").innerText = ""
    document.getElementById("msg").innerText = "Time up Buddy!⏰"
    document.getElementById("next").style.display = "block"

def next_q(e=None):
    global current, answered,score

    clearInterval(timer_id)
    answered = False

    current += 1

    if current < len(questions):
        show_question()
        document.getElementById("score-card").innerText = f"Score: {score}"
    else:
        document.getElementById("question").innerText = "Quiz Finished 🎉"
        document.getElementById("options").style.display = "none"
        document.getElementById("next").style.display = "none"
        document.getElementById("timer").innerText = ""
        document.getElementById("msg").innerText = f"Your Final Score: {score} / {len(questions)}"
        document.getElementById("brand").innerText = "Presented by SyrX"
        document.getElementById("ad").innerText = "Co-Founders- Saketh & Yashwanth"


def start_game(e=None):
    global current,score

    current = 0
    score=0
    document.getElementById("score-card").innerText = f"Score: {score}"
    show_question()

opts = document.getElementsByClassName("opt")

for i in range(len(opts)):
    opts[i].addEventListener("click", create_proxy(choose_option))

document.getElementById("next").addEventListener("click", create_proxy(next_q))

def display_game(e):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
    start_game()
def scoreboard():
    score = document.getElementById("score").value
    document.getElementById("scoreboard").innerText = f"Your Score: {score}/{len(questions)}"



    
questions_2 = [ """Tanya is older than Eric.
                 Cliff is older than Tanya.
                 Eric is older than Cliff.
                 If the first two statements are true, the third statement is """,
             """ If 12$34 = 10, 2$9 = 11 then what is the value of 6$27 = ?""",
             """If in a certain code, RAIN is written as 81#4 and CLOUD is written as 92#6, how will WIND be written?""",
                "2, 6, 7, 21, 22, ?",
                "1, 1, 2, 3, 5, 8, ?",
                 "3, 9, 27, 81, ?",
                 "4, 6, 9, 13, 18, ?",
                "If CAT = 24, DOG = 26, then BAT = ?",
                  "Find missing: 2, 10, 12, 60, 62, ?",
                "What comes next: Z, X, U, Q, ?",
                "If 5x = 20, then x = ?",
                 "A number doubled is 50. What is the number?",
                 "If 12 + 15 = 33, 13 + 16 = 35, then 14 + 17 = ?",
                "Which number is odd one out?",
               "Which word is different?",
                  "If all Bloops are Razzies and all Razzies are Lazzies, then all Bloops are?"
                ]

options_list_2 = [
    ["False", "True", "Uncertain", "No Enough Information"],
    ["33", "15", "20", "10"],
    ["71#6", "92#5", "91#5", "82#"],
    ["44", "66", "23", "11"],
    ["11", "13", "10", "15"],
    ["162", "243", "108", "324"],
    ["22", "23", "24", "25"],
    ["21", "23", "25", "27"],
    ["300", "310", "320", "360"],
    ["M", "N", "O", "L"],
    ["2", "3", "4", "5"],
    ["20", "25", "30", "15"],
    ["37", "36", "38", "39"],
    ["121", "144", "169", "145"],
    ["Apple", "Banana", "Carrot", "Mango"],
    ["Lazzies", "Not Lazzies", "Some Lazzies", "None"]
]

answers_2=["False","33","91#5","66", "13", "243", "24", "23", "310", "M", "4", "25", "37", "145", "Carrot", "Lazzies"]

current_2 = 0
answered_2 = False
time_left_2 = 15
timer_id_2 = None
score_2=0

def start_timer_2():
    global timer_id_2, time_left_2, answered_2

    clearInterval(timer_id_2)
    time_left_2 = 15

    def tick_2():
        global time_left_2,timer_id_2


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

    document.getElementById("msg_2").innerText = ""
    document.getElementById("next_2").style.display = "none"
    document.getElementById("options_2").style.display = "block"
    document.getElementById("question_2").innerText = questions_2[current_2]

    opts_2 = document.getElementsByClassName("opt_2")
    for i in range(len(opts_2)):
        opts_2[i].innerText = options_list_2[current_2][i]
        opts_2[i].style.backgroundColor = ""

    start_timer_2()
def choose_option_2(e):
    global answered_2, score_2

    if answered_2:
        return

    clearInterval(timer_id_2)
    answered_2 = True

    user_choice_2 = e.target.innerText
    correct_2 = answers_2[current_2]

    opts_2 = document.getElementsByClassName("opt_2")

    for i in range(len(opts_2)):
        option_text_2 = opts_2[i].innerText

        if option_text_2 == correct_2:
            # ✅ correct answer → always green
            opts_2[i].style.backgroundColor = "#3ADD19"
            opts_2[i].style.color = "white"

        elif option_text_2 == user_choice_2:
            # ❌ wrong selected → red
            opts_2[i].style.backgroundColor = "#d2230f"
            opts_2[i].style.color = "white"
    if user_choice_2 == correct_2:
         score_2 += 1
    document.getElementById("score-card_2").innerText = f"Score: {score_2}"
    document.getElementById("next_2").style.display = "block"
def time_up_2():
    global answered_2

    if answered_2:
        return

    answered_2 = True
    clearInterval(timer_id_2)

    document.getElementById("options_2").style.display = "none"
    document.getElementById("question_2").innerText = ""
    document.getElementById("msg_2").innerText = "Time up Buddy!⏰"
    document.getElementById("next_2").style.display = "block"

def next_q_2(e=None):
    global current_2, answered_2,score_2

    clearInterval(timer_id_2)
    answered_2 = False

    current_2 += 1

    if current_2 < len(questions_2):
        show_question_2()
        document.getElementById("score-card_2").innerText = f"Score: {score_2}"
    else:
        document.getElementById("question_2").innerText = "Quiz Finished 🎉"
        document.getElementById("options_2").style.display = "none"
        document.getElementById("next_2").style.display = "none"
        document.getElementById("timer_2").innerText = ""
        document.getElementById("msg_2").innerText = f"Your Final Score: {score_2} / {len(questions_2)}"
        document.getElementById("brand_2").innerText = "Presented by SyrX"
        document.getElementById("ad_2").innerText = "Co-Founders- Saketh & Yashwanth"


def start_game_2(e=None):
    global current_2,score_2

    current_2 = 0
    score_2=0
    document.getElementById("score-card_2").innerText = f"Score: {score_2}"
    show_question_2()

opts_2 = document.getElementsByClassName("opt_2")

for i in range(len(opts_2)):
    opts_2[i].addEventListener("click", create_proxy(choose_option_2))

document.getElementById("next_2").addEventListener("click", create_proxy(next_q_2))

def display_game_2(e):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionmissing").style.display = "block"
    start_game_2()
def scoreboard_2():
    score = document.getElementById("score_2").value
    document.getElementById("scoreboard_2").innerText = f"Your Score: {score_2}/{len(questions_2)}"