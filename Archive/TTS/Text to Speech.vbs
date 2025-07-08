Dim msg, sapi
msg=InputBox("Text to Speech")
Set sapi=CreateObject("sapi.spvoice")
sapi.Speak msg