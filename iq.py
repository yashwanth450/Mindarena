from js import document, setInterval, clearInterval
from pyodide.ffi import create_proxy

def username(e):
    
    name = document.getElementById("name").value
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

def display(sectionId):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionstart").style.display = "block"
play=document.getElementById("play")
play.addEventListener("click", create_proxy(display))

def start(_):
    document.getElementById("sectionstart").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
end=document.getElementById("end")
end.addEventListener("click", create_proxy(start))


def games(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit=document.getElementById("exit")
exit.addEventListener("click", create_proxy(games))


questions = [ """2+3 = 10, 7+2 = 63, 6+5 = 66, 8+4 = 96 then what is the value of 9+3 = ?""",
             """ If 12$34 = 10, 2$9 = 11 then what is the value of 6$27 = ?""",
             """If in a certain code, RAIN is written as 81#4 and CLOUD is written as 92#6, how will WIND be written?"""
              ]

options_list = [
    ["1", "2", "Uncertain", "No Enough Information"],
    ["33", "15", "20", "10"],
    ["71#6", "92#5", "91#5", "82#"]
]
current = 0
answered = False
time_left = 15
timer_id = None

def start_timer():
    global timer_id, time_left, answered

    clearInterval(timer_id)
    time_left = 15

    def tick():
        global time_left

        if answered:
            clearInterval(timer_id)
            return

        document.getElementById("timer").innerText = f"Time: {time_left}"

        time_left -= 1

        if time_left < 0:
            time_up()

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

    start_timer()
def choose_option(e):
    global answered

    if answered:
        return

    answered = True
    clearInterval(timer_id)

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
    global current, answered

    clearInterval(timer_id)
    answered = False

    current += 1

    if current < len(questions):
        show_question()
    else:
        document.getElementById("question").innerText = "Quiz Finished 🎉"
        document.getElementById("options").style.display = "none"
        document.getElementById("next").style.display = "none"
        document.getElementById("timer").innerText = ""
        document.getElementById("msg").innerText = ""

def start_game(e=None):
    global current

    current = 0
    show_question()

opts = document.getElementsByClassName("opt")

for i in range(len(opts)):
    opts[i].addEventListener("click", create_proxy(choose_option))

document.getElementById("next").addEventListener("click", create_proxy(next_q))

def display_game(e):
    document.getElementById("sectionstart").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
    start_game()
