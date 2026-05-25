from js import document, setInterval, clearInterval,window
from pyodide.ffi import create_proxy
import random

def username(e):
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
        document.getElementById("display-username").innerText = f" {name}".upper()
        document.getElementById("sectionlogin").style.display = "none"
        document.getElementById("sectiontest").style.display = "block"
        document.getElementById("games_completed").disabled = True
        document.getElementById("games_completed").style.opacity = "0.5"

btn = document.getElementById("btn")
btn.addEventListener("click", create_proxy(username))

def home(_):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionlogin").style.display = "block"
back = document.getElementById("back")
back.addEventListener("click", create_proxy(home))

def display_reasoning(e):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
    start_game()
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


question_pool = [
    {
        "question": "Tanya is older than Eric. Cliff is older than Tanya. Eric is older than Cliff. If the first two statements are true, the third statement is?",
        "options": ["False", "True", "Uncertain", "Not Enough Information"],
        "answer": "False"
    },
    {
        "question": "If 12$34 = 10, 2$9 = 11 then what is the value of 6$27?",
        "options": ["33", "15", "20", "10"],
        "answer": "33"
    },
    {
        "question": "If RAIN = 81#4 and CLOUD = 92#6, how will WIND be written?",
        "options": ["71#6", "92#5", "91#5", "82#4"],
        "answer": "91#5"
    },
    {
        "question": "2, 6, 7, 21, 22, ?",
        "options": ["44", "66", "23", "11"],
        "answer": "66"
    },
    {
        "question": "Find the odd one out: Cat, Dog, Rose, Cow",
        "options": ["Cat", "Dog", "Rose", "Cow"],
        "answer": "Rose"
    },
    {
        "question": "1, 4, 9, 16, 25, ?",
        "options": ["30", "36", "49", "35"],
        "answer": "36"
    },
    {
        "question": "Which number comes next? 3, 6, 11, 18, 27, ?",
        "options": ["38", "36", "40", "35"],
        "answer": "38"
    },
    {
        "question": "A is B's sister. C is B's mother. D is C's father. How is A related to D?",
        "options": ["Granddaughter", "Daughter", "Grandmother", "Sister"],
        "answer": "Granddaughter"
    },
    {
        "question": "All roses are flowers. Some flowers fade quickly. Therefore?",
        "options": ["All roses fade", "Some roses fade", "No roses fade", "Cannot be determined"],
        "answer": "Cannot be determined"
    },
    {
        "question": "If MANGO is coded as OCPIQ, how is APPLE coded?",
        "options": ["CRRNG", "CRRNF", "BQQMF", "DSSOH"],
        "answer": "CRRNG"
    },
]


selected_questions = []
current = 0
answered = False
time_left = 15
timer_id = None
score = 0
games_completed = 0
fast_answers = 0
medium_answers = 0
slow_answers = 0


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
            document.getElementById("question").innerText = ""
            document.getElementById("msg").innerText = "Time up Buddy!⏰"
            document.getElementById("next").style.display = "block"

    timer_id = setInterval(create_proxy(tick), 1000)


def show_question():
    global answered
    answered = False

    current_q = selected_questions[current]

    document.getElementById("msg").innerText = ""
    document.getElementById("next").style.display = "none"
    document.getElementById("options").style.display = "block"
    document.getElementById("question").innerText = current_q["question"]

    opts = document.getElementsByClassName("opt")
    for i in range(len(opts)):
        opts[i].innerText = current_q["options"][i]
        opts[i].style.backgroundColor = ""
        opts[i].style.color = ""

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
        option_text = opts[i].innerText
        if option_text == correct:
            opts[i].style.backgroundColor = "#3ADD19"
            opts[i].style.color = "white"
        elif option_text == user_choice:
            opts[i].style.backgroundColor = "#d2230f"
            opts[i].style.color = "white"

    if user_choice == correct:
        window.playCorrect() 
        if time_left >= 10:
            score += 5
            fast_answers += 1
        elif time_left >= 5:
            score += 3
            medium_answers += 1
        else:
            score += 1
            slow_answers += 1
    else:
     window.playWrong()
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
        document.getElementById("question").innerText = "Quiz Finished 🎉"
        document.getElementById("options").style.display = "none"
        document.getElementById("next").style.display = "none"
        document.getElementById("timer").style.display = "none"
        document.getElementById("msg").innerText = f"Your Final Score: {score}"
        document.getElementById("fast-answers").innerText = f"⚡ Within 5 sec: {fast_answers}"
        document.getElementById("medium-answers").innerText = f"🕐 Within 10 sec: {medium_answers}"

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

   
    selected_questions = random.sample(question_pool, 5)

    document.getElementById("score-card").innerText = f"Score: {score}"
    document.getElementById("timer").style.display = "block"
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
        window.playCorrect() 
        if time_left_2 >= 10:
            score_2 += 5
            fast_answers_2 += 1
        elif time_left_2 >= 5:
            score_2 += 3
            medium_answers_2 += 1
        else:
            score_2 += 1
            slow_answers_2 += 1
    else:
     window.playWrong()        

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
        document.getElementById("msg_2").innerText = f"Your Final Score: {score_2}"

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
