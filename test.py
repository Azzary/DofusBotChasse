# import json
# import requests

# url = "https://github.com/bot4dofus/Datafus/raw/master/data/entities_json/MapPositions.json"
# resp = requests.get(url)
# data = json.loads(resp.text)

# new_data = {}
# for elem in data["data"]:
#     new_data[elem["id"]] = elem

# with open('MapPositions.json', 'w', encoding='utf-8') as f:
#     json.dump(new_data, f, ensure_ascii=False, indent=4)


from ctypes import *
import win32gui
import win32api
import win32con


user32 = windll.user32
kernel32 = windll.kernel32

class RECT(Structure):
 _fields_ = [
     ("left", c_ulong),
     ("top", c_ulong),
     ("right", c_ulong),
     ("bottom", c_ulong)
 ]

class GUITHREADINFO(Structure):
 _fields_ = [
     ("cbSize", c_ulong),
     ("flags", c_ulong),
     ("hwndActive", c_ulong),
     ("hwndFocus", c_ulong),
     ("hwndCapture", c_ulong),
     ("hwndMenuOwner", c_ulong),
     ("hwndMoveSize", c_ulong),
     ("hwndCaret", c_ulong),
     ("rcCaret", RECT)
 ]



def get_selected_text_from_front_window(): # As String
    ''' vb6 to python translation '''

    gui = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))
    txt=''
    ast_Clipboard_Obj=None
    Last_Clipboard_Temp = -1


    user32.GetGUIThreadInfo(0, byref(gui))

    txt = GetCaretWindowText(gui.hwndCaret, True)

    '''
    if Txt = "" Then
        LastClipboardClip = ""
        Last_Clipboard_Obj = GetClipboard
        Last_Clipboard_Temp = LastClipboardFormat
        SendKeys "^(c)"
        GetClipboard
        Txt = LastClipboardClip
        if LastClipboardClip <> "" Then Txt = LastClipboardClip
        RestoreClipboard Last_Clipboard_Obj, Last_Clipboard_Temp
        print "clbrd: " + Txt
    End If
    '''    
    return txt



def GetCaretWindowText(hWndCaret, Selected = False): # As String

    startpos =0
    endpos =0

    txt = ""

    if hWndCaret:

        buf_size = 1 + win32gui.SendMessage(hWndCaret, win32con.WM_GETTEXTLENGTH, 0, 0)
        if buf_size:
            buffer = win32gui.PyMakeBuffer(buf_size)
            win32gui.SendMessage(hWndCaret, win32con.WM_GETTEXT, buf_size, buffer)
            txt = buffer[:buf_size]

        if Selected and buf_size:
            selinfo  = win32gui.SendMessage(hWndCaret, win32con.EM_GETSEL, 0, 0)
            endpos   = win32api.HIWORD(selinfo)
            startpos = win32api.LOWORD(selinfo)
            return txt[startpos: endpos]

    return txt

if __name__ == '__main__':
    print(get_selected_text_from_front_window())
