from js import document, setInterval, clearInterval, window
from pyodide.ffi import create_proxy
import random
def register(e):
    name     = document.getElementById("reg-name").value.strip()
    age      = document.getElementById("reg-age").value.strip()
    password = document.getElementById("reg-password").value.strip()

    def show_err(msg):
        document.getElementById("reg-error").innerText = msg

    # ---- Validations first ----
    if not name:
        show_err("⚠️ Please enter your name"); return
    if not name.replace(" ", "").isalpha() or len(name) < 4:
        show_err("⚠️ Name must be 4+ letters only"); return
    if not age.isdigit() or not (10 <= int(age) <= 30):
        show_err("⚠️ Age must be between 10 and 30"); return
    if len(password) < 6:
        show_err("⚠️ Password must be at least 6 characters"); return

    show_err("")

    global username_input, age_input_value
    username_input = name.upper()
    age_input_value = age

    # ---- Check if name exists in Supabase ----
    def on_name_checked(exists):
        if exists:
            # Name already taken — show error
            document.getElementById("reg-error").innerText = "❌ This name is already taken! Try a different name."
            return

        # Name is free — proceed with registration
        def go():
            global games_completed
            games_completed = 0
            document.getElementById("display-username").innerText = f" {username_input}"
            document.getElementById("section_new_profile").style.display = "none"
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

        window.saveUser(username_input, age_input_value, password)
        window.showLoader(2000, "Creating your account...", create_proxy(go))

    # Call JS to check name, pass Python callback
    window.checkNameExists(name).then(create_proxy(on_name_checked))

document.getElementById("btn-register").addEventListener("click", create_proxy(register))

# ---- LOGIN ----
def login(e):
    name     = document.getElementById("login-name").value.strip()
    password = document.getElementById("login-password").value.strip()

    def show_err(msg):
        document.getElementById("login-error").innerText = msg

    if not name or not password:
        show_err("⚠️ Please fill all fields"); return

    show_err("")

    global username_input
    username_input = name.upper()

    def go():
        global games_completed
        games_completed = 0
        document.getElementById("display-username").innerText = f" {username_input}"
        document.getElementById("section_login").style.display = "none"
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

    window.loginUser(name, password)
    window.showLoader(2000, "Logging you in...", create_proxy(go))

document.getElementById("btn-login").addEventListener("click", create_proxy(login))


# ---- NAVIGATION ----
def main_page_create_new_profile(_):
    document.getElementById("sectionmain_page").style.display = "none"
    document.getElementById("section_new_profile").style.display = "block"

document.getElementById("create_new_profile").addEventListener("click", create_proxy(main_page_create_new_profile))

def main_page_login(_):
    document.getElementById("sectionmain_page").style.display = "none"
    document.getElementById("section_login").style.display = "block"

document.getElementById("login_button").addEventListener("click", create_proxy(main_page_login))

def home(_):
    document.getElementById("sectiontest").style.display = "none"
    document.getElementById("sectionmain_page").style.display = "block"

document.getElementById("back").addEventListener("click", create_proxy(home))