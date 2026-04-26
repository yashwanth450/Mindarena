from js import document
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
    document.getElementById("sectionReasoning").style.display = "block"
play=document.getElementById("play")
play.addEventListener("click", create_proxy(display))


def games(_):
    document.getElementById("sectionReasoning").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
exit=document.getElementById("exit")
exit.addEventListener("click", create_proxy(games))
