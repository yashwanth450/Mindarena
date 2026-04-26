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
    start_game()
end=document.getElementById("end")
end.addEventListener("click", create_proxy(start))


def games(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit=document.getElementById("exit")
exit.addEventListener("click", create_proxy(games))


questions = [ """Tanya is older than Eric.
                 Cliff is older than Tanya.
                 Eric is older than Cliff.
                 If the first two statements are true, the third statement is """,
             """ If 12$34 = 10, 2$9 = 11 then what is the value of 6$27 = ?""",
             """If in a certain code, RAIN is written as 81#4 and CLOUD is written as 92#6, how will WIND be written?"""
              ]

options_list = [
    ["False", "True", "Uncertain", "No Enough Information"],
    ["33", "15", "20", "10"],
    ["71#6", "92#5", "91#5", "82#"]
]
answers=["False","33","91#5"]
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
    global answered, score, current # We need 'current' to know which answer to check

    if answered: 
        return
    # 2. STOP THE TIMER IMMEDIATELY (for both right and wrong answers)
    user_choice = e.target.innerText
    if user_choice == answers[current]:
        answered = True
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
    document.getElementById("sectionstart").style.display = "none"
    document.getElementById("sectionReasoning").style.display = "block"
    start_game()
def scoreboard():
    score = document.getElementById("score").value
    document.getElementById("scoreboard").innerText = f"Your Score: {score}/{len(questions)}"
