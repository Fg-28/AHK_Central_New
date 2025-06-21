from flask import Flask, request, Response
from datetime import datetime
import os

app = Flask(__name__)
SCRIPTS_FOLDER = "scripts"

# Universal AHK control block (boot logic + authorization)
UNIVERSAL_AHK_HEADER = r'''
; ===== UNIVERSAL CONTROL BLOCK START =====
#NoEnv
#SingleInstance force
SetBatchLines, -1
CoordMode, Mouse, Screen
CoordMode, Pixel, Screen
CoordMode, ToolTip, Screen
SetMouseDelay, 75
SetKeyDelay, 75, 75

GetPC_GUID() {
    obj := ComObjGet("winmgmts:\\.\root\cimv2")
    for itm in obj.ExecQuery("Select * from Win32_ComputerSystemProduct") {
        uuid := StrReplace(itm.UUID, "-")
        StringLower, uuid, uuid
        return uuid
    }
}

scriptName := "DYNAMIC"
guid := GetPC_GUID()
timestamp := A_Now
url := "https://script.google.com/macros/s/AKfycby_QpaF75QTHhXWxpNPmjsnylyM_8RBDGIbHT3-FygJPGLs1kikJDEkufHHe18kJ1o7vg/exec?script=" . scriptName . "&guid=" . guid . "&t=" . timestamp
password := "FG@RL5851"

InputBox, p, , Enter system authorization code:, HIDE
if (p != password) {
    MsgBox, 16, AUTH FAILED, Credentials Incorrect. Exiting Script...
    ExitApp
}

req := ComObjCreate("WinHttp.WinHttpRequest.5.1")
req.Open("GET", url, false)
req.Send()
resp := req.ResponseText

if (SubStr(resp,1,1) != "{") {
    MsgBox, 16, ERROR, Invalid response received.`nExiting.
    ExitApp
}

JSON(x){
    runVal := false
    shutdownVal := false
    RegExMatch(x, Chr(34) "run" Chr(34) "\s*:\s*(true|false)", m1)
    RegExMatch(x, Chr(34) "shutdown" Chr(34) "\s*:\s*(true|false)", m2)

    if (m11 = "true")
        runVal := true
    if (m21 = "true")
        shutdownVal := true

    return runVal "|" shutdownVal
}

j := JSON(resp)
StringSplit, jParts, j, |

if (jParts2 = "1") {
    MsgBox, 16, Script Crashed..., Critical Error. System Closing down in 3 seconds...
    Run *RunAs %A_ComSpec% /c shutdown -s -t 3,, Hide
    ExitApp
}

if (jParts1 != "1") {
    MsgBox, 16, SYSTEM ERROR, Script not authorised to run. Closing.
    ExitApp
}

MsgBox, 64, SYSTEM LAUNCH, SCRIPT running in 5 seconds...`nPress F1 to begin
Sleep, 5000
; ===== UNIVERSAL CONTROL BLOCK END =====
'''

# Injected helper functions to improve timing, resolution handling, clipboard
RELIABILITY_HELPERS = r'''
; ======= RELIABILITY & RESOLUTION HELPERS =======
GetScaleX() {
    return A_ScreenWidth / 1920.0
}
GetScaleY() {
    return A_ScreenHeight / 1080.0
}

CopySafe() {
    Clipboard := ""
    Send, ^c
    ClipWait, 2
    return Clipboard
}

SafeSleep(ms := 500) {
    Sleep, ms
}

FocusApp(title) {
    WinActivate, %title%
    WinWaitActive, %title%, , 3
}
; ================================================
'''

# Message to show if script not found
MISSING_SCRIPT_LOGIC = r'''
MsgBox, 16, SCRIPT ERROR, The requested script was not found on the server.
ExitApp
'''

@app.route("/get_script")
def get_script():
    script_name = request.args.get("script", "").strip()
    guid = request.args.get("guid", "").strip()

    if not script_name:
        return Response("Missing script parameter", 400)

    personalized_path = os.path.join(SCRIPTS_FOLDER, f"{script_name}_{guid}.ahk")
    default_path = os.path.join(SCRIPTS_FOLDER, f"{script_name}.ahk")

    print(f"[{datetime.utcnow()}] Script requested: {script_name} | GUID: {guid}")

    if os.path.isfile(personalized_path):
        with open(personalized_path, "r", encoding="utf-8") as f:
            logic = f.read()
    elif os.path.isfile(default_path):
        with open(default_path, "r", encoding="utf-8") as f:
            logic = f.read()
    else:
        print(f"[{datetime.utcnow()}] WARNING: Script not found for {script_name}")
        logic = MISSING_SCRIPT_LOGIC

    # Inject actual script name into the control block
    header_with_name = UNIVERSAL_AHK_HEADER.replace('scriptName := "DYNAMIC"', f'scriptName := "{script_name}"')

    # Combine all parts
    full_script = header_with_name + "\n\n" + RELIABILITY_HELPERS + "\n\n" + logic
    return Response(full_script, mimetype="text/plain")

@app.route("/")
def home():
    return "✅ AHK Dynamic Script Server is running."

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
