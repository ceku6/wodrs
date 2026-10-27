Set WshShell = CreateObject("WScript.Shell")
WshShell.Run "pythonw.exe """ & WScript.Arguments(0) & """", 0, False
