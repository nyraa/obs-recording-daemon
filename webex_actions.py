from pywinauto import application
from pywinauto.application import Application
from pywinauto import findwindows
from pywinauto.keyboard import send_keys
import pyautogui
import pyperclip
import time
import cv2
import ctypes

import utils

def wakeup_webex():
    send_keys('{LWIN}')
    time.sleep(0.3)

    pyperclip.copy('webex')
    time.sleep(0.3)

    send_keys('^v')
    time.sleep(2)

    send_keys('{ENTER}')
    time.sleep(5)

def join_meeting(room_id, name, email):
    wakeup_webex()

    img_join = cv2.imread('img/webex_join.png')
    x, y = pyautogui.locateCenterOnScreen(img_join, confidence=0.9)

    pyautogui.click(x, y)
    time.sleep(2)

    pyperclip.copy(room_id)
    time.sleep(0.3)
    send_keys('^v{TAB}{TAB}')

    pyperclip.copy(name)
    time.sleep(0.3)
    send_keys('^v{TAB}{TAB}')

    pyperclip.copy(email)
    time.sleep(0.3)
    send_keys('^v{TAB}{TAB}{ENTER}')

    # fullscreen
    img_fullscreen = cv2.imread('img/webex_fullscreen.png')
    x, y = pyautogui.locateCenterOnScreen(img_fullscreen, confidence=0.9)
    pyautogui.click(x, y)
    time.sleep(2)

def join_meeting_uia(room_id, name, email):
    wakeup_webex()
    webex = Application(backend='uia').connect(title='Webex', timeout=100)

    try:
        back_btn = webex.Webex.child_window(title=" 返回", auto_id="MainWindowClass.OnboardingView.onboardingScreen.backButton", control_type="Button").wrapper_object()
        back_btn.click_input()
    except:
        pass

    join_btn = webex.Webex.child_window(auto_id="MainWindowClass.OnboardingView.onboardingScreen.stackedWidget.normalViewsPage.onboardingStackWidget.OnboardingStartWidget.dataStackedWidget.dataWidget.joinMeetingButton", control_type="Button").wrapper_object()
    join_btn.click_input()
    time.sleep(1)

    room_id_textbox = webex.Webex.child_window(auto_id="MainWindowClass.OnboardingView.onboardingScreen.stackedWidget.normalViewsPage.onboardingStackWidget.OnboardingGuestJoinWidget.meetingInfo.textInput", control_type="Edit").wrapper_object()
    room_id_textbox.set_text(room_id)

    name_textbox = webex.Webex.child_window(auto_id="MainWindowClass.OnboardingView.onboardingScreen.stackedWidget.normalViewsPage.onboardingStackWidget.OnboardingGuestJoinWidget.displayName.textInput", control_type="Edit").wrapper_object()
    name_textbox.set_text(name)

    email_textbox = webex.Webex.child_window(auto_id="MainWindowClass.OnboardingView.onboardingScreen.stackedWidget.normalViewsPage.onboardingStackWidget.OnboardingGuestJoinWidget.email.textInput", control_type="Edit").wrapper_object()
    email_textbox.set_text(email)

    next_button = webex.Webex.child_window(title=" 下一步", auto_id="MainWindowClass.OnboardingView.onboardingScreen.stackedWidget.normalViewsPage.onboardingStackWidget.OnboardingGuestJoinWidget.nextButton", control_type="Button").wrapper_object()
    next_button.click_input()
    
    time.sleep(1)

    meeting_window_pid = application.process_from_module(module='atmgr.exe')
    webex_meeting_window = Application(backend='uia').connect(process=meeting_window_pid, timeout=20)

    time.sleep(3)
    # webex_meeting_window.Pane.print_control_identifiers()
    try:
        join_meeting_button = webex_meeting_window.Pane.Button7.wrapper_object()
        # join_meeting_button = webex_meeting_window.Pane.child_window(title="加入會議").wrapper_object()
        join_meeting_button.click_input()
    except Exception as e:
        print(e)
        pass

    time.sleep(3)
    
    # maximize
    window = findwindows.find_windows(process=meeting_window_pid)[0]
    webex_meeting_window.window_(handle=window).set_focus()
    ctypes.windll.user32.ShowWindow(window, 3)
    print('open fin')

def terminate_meeting_uia():
    meeting_window_pid = application.process_from_module(module='atmgr.exe')
    webex_meeting_window = Application(backend='uia').connect(process=meeting_window_pid, timeout=20)

    window = findwindows.find_windows(process=meeting_window_pid)[0]
    ctypes.windll.user32.SetForegroundWindow(window)

    time.sleep(0.5)
    webex_meeting_window.Pane.type_keys('{ESC}{ENTER}')
    # webex_meeting_window.Pane.type_keys('{LWIN down}{DOWN}{LWIN up}')

if __name__ == '__main__':
    join_meeting_uia('2644 679 5227', 'bar', 'example@example.com')
    time.sleep(5)
    print('close')
    terminate_meeting_uia()