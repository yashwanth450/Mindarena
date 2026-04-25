from js import document
from pyodide.ffi import create_proxy

def username(e):
    
    name = document.getElementById("name").value
    
    document.getElementById("display-username").innerText = f" {name}".upper()
    
    document.getElementById("sectionlogin").style.display = "none"
    document.getElementById("sectiontest").style.display = "block"
btn = document.getElementById("btn")
btn.addEventListener("click", create_proxy(username))