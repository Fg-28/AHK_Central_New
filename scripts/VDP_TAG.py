#NoEnv
#Persistent
#SingleInstance Force
SetBatchLines, -1
CoordMode, Mouse, Screen
CoordMode, Pixel, Screen
CoordMode, ToolTip, Screen
SetMouseDelay, 50
SetKeyDelay, 50, 50
Sleep, 5000

; ===== DPI Scaling Helpers =====
GetScaleX() {
    return A_ScreenWidth / 1920.0
}
GetScaleY() {
    return A_ScreenHeight / 1080.0
}

MainLoop:
F1::
Loop
{
    x := Round(309 * GetScaleX())
    y := Round(284 * GetScaleY())
    MouseClick, Left, x, y
    Send, ^c
    Sleep, 350
    ClipWait
    VDP := Trim(Clipboard)
    if (VDP != "VDP" && VDP != "vdp" && VDP != "Vdp")
    {
        Sleep, 7000
        continue
    }

    x := Round(505 * GetScaleX())
    y := Round(260 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 350

    x := Round(543 * GetScaleX())
    y := Round(238 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 350
    Send, {Enter}
    Sleep, 350

    ; Copy the invoice number from Google Sheet
    Send, !{Tab}
    Sleep, 150
    Send, ^c
    CopiedData := Clipboard

    char3 := SubStr(CopiedData, 3, 1)
    char4 := SubStr(CopiedData, 4, 1)

    if (char3 = "" || char4 = "")
    {
        MsgBox, 16, Error, Invalid data! Invoice is blank.
        ExitApp
    }

    ; Pasting data into invoice in Party Recon
    Send, !{Tab}
    Sleep, 300
    x := Round(1093 * GetScaleX())
    y := Round(729 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 200
    Send, {Down}
    Sleep, 150
    Send, {Tab}
    Send, ^v
    Send, {Enter}
    Sleep, 350
    Clipboard := ""

    x := Round(505 * GetScaleX())
    y := Round(755 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 150

    x := Round(1551 * GetScaleX())
    y := Round(755 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 200
    MouseClick, Left, x, y, 2
    Sleep, 150
    Send, ^c
    Sleep, 150
    ClipWait
    Amount := Clipboard
    if (Amount == "0")
    {
        Send, !{Tab}
        Sleep, 150
        Send, {Down}
        Sleep, 250
        Send, ^c
        Sleep, 150
        Send, !{Tab}
        Sleep, 150

        x := Round(1093 * GetScaleX())
        y := Round(729 * GetScaleY())
        MouseClick, Left, x, y
        Sleep, 350

        Send, {Tab}
        Send, {Tab}
        Send, {Down}
        Send, {Tab}
        Send, {Down}
        Send, {Tab}
        Send, ^v
        Sleep, 150
        Send, {Enter}
        Sleep, 150

        x := Round(505 * GetScaleX())
        y := Round(780 * GetScaleY())
        MouseClick, Left, x, y
        Sleep, 150

        x := Round(1551 * GetScaleX())
        y := Round(780 * GetScaleY())
        MouseClick, Left, x, y
        Sleep, 150
        MouseClick, Left, x, y, 2
        Send, ^c
        Sleep, 150
        ClipWait
        Second := Clipboard
        if (Second == "0")
        {
            Send, !{Tab}
            Sleep, 150
            Send, {Down}
            Sleep, 150
            Send, !{Tab}
            Sleep, 150
        }
    }

    Send, ^s
    Sleep, 18000

    x := Round(100 * GetScaleX())
    y := Round(600 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 24000

    x := Round(1160 * GetScaleX())
    y := Round(300 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 150

    x := Round(100 * GetScaleX())
    y := Round(600 * GetScaleY())
    MouseClick, Left, x, y
    Sleep, 1000
    MouseClick, Left, x, y
    Sleep, 1000

    x := Round(1791 * GetScaleX())
    y := Round(700 * GetScaleY())
    MouseClick, Left, x, y, 2
    Send, ^c
    Sleep, 150
    ClipWait
    Total := Clipboard
    if (Total < 3)
    {
        ExitApp
        break
    }
}

Esc::ExitApp
`::Pause
