#MaxThreadsPerHotkey 2
F2::
Toggle := !Toggle
Loop {
ImageSearch, X, Y, 0, 0, A_ScreenWidth, A_ScreenHeight, Untitled.png
If ErrorLevel {
Sleep 3000
} else {
MouseMove, %X%, %y%
Click 
}
Sleep 100
If not Toggle 
	break
}
return

^esc:: ExitApp