import cv2
import mediapipe as mp
import time
import mouse  # move function
import pyautogui  # click function
import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.core.window import Window

kivy.require("2.0.0")  # minimum kivy version


def came(firstArg, secondArg, thirdArg, fourthArg):
    cap = cv2.VideoCapture(0)
    pTime = 0
    mpDraw = mp.solutions.drawing_utils
    mpFaceMesh = mp.solutions.face_mesh
    faceMesh = mpFaceMesh.FaceMesh(max_num_faces=1)  # recognizes only one face at a time
    drawSpec = mpDraw.DrawingSpec(thickness=1, circle_radius=2)
    detected_eyebrows = 0
    start_time_eyebrow = 0
    end_time_eyebrow = 0
    detected_mouth_length = 0
    detected_mouth_width = 0
    end_time_eyebrow = 0
    while True:
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = faceMesh.process(imgRGB)
        if results.multi_face_landmarks:
            for faceLms in results.multi_face_landmarks:
                mpDraw.draw_landmarks(img, faceLms, mpFaceMesh.FACEMESH_CONTOURS, drawSpec, drawSpec)
                diff_mouth_width = float(faceLms.landmark[16].y) - float(faceLms.landmark[13].y)
                diff_mouth_length = float(faceLms.landmark[308].x) - float(faceLms.landmark[61].x)
                diff_eyebrows = float(faceLms.landmark[385].y) - float(faceLms.landmark[296].y)
                diff_nose_up = float(faceLms.landmark[152].y) - float(faceLms.landmark[1].y)
                diff_nose_down = float(faceLms.landmark[175].y) - float(faceLms.landmark[19].y)
                diff_nose_left = float(faceLms.landmark[1].x) - float(faceLms.landmark[123].x)
                diff_nose_right = float(faceLms.landmark[352].x) - float(faceLms.landmark[1].x)
                xx, yy = mouse.get_position()
                if diff_mouth_length > 0.166325 and detected_mouth_length == 0:
                    detected_mouth_length = 1
                    if firstArg == 1:
                        pyautogui.click(xx, yy)
                    if firstArg == 2:
                        pyautogui.doubleClick(xx, yy)
                    if firstArg == 3:
                        pyautogui.rightClick(xx, yy)
                    if firstArg == 4:
                        pyautogui.press("esc")
                if diff_mouth_width > 0.038823 and detected_mouth_width == 0:
                    detected_mouth_width = 1
                    if secondArg == 1:
                        pyautogui.click(xx, yy)
                    if secondArg == 2:
                        pyautogui.doubleClick(xx, yy)
                    if secondArg == 3:
                        pyautogui.rightClick(xx, yy)
                    if secondArg == 4:
                        pyautogui.press("esc")
                if diff_eyebrows > 0.091934:
                    start_time_eyebrow = time.time()
                    if (start_time_eyebrow - end_time_eyebrow) > 4.0 and detected_eyebrows == 0:
                        start_time_eyebrow = 0
                        end_time_eyebrow = 0
                        detected_eyebrows = 1
                        if thirdArg == 1:
                            pyautogui.click(xx, yy)
                        if thirdArg == 2:
                            pyautogui.doubleClick(xx, yy)
                        if thirdArg == 3:
                            pyautogui.rightClick(xx, yy)
                        if thirdArg == 4:
                            pyautogui.press("esc")
                    elif end_time_eyebrow != 0 and detected_eyebrows == 0:
                        detected_eyebrows = 1
                        start_time_eyebrow = 0
                        end_time_eyebrow = 0
                        if fourthArg == 1:
                            pyautogui.click(xx, yy)
                        if fourthArg == 2:
                            pyautogui.doubleClick(xx, yy)
                        if fourthArg == 3:
                            pyautogui.rightClick(xx, yy)
                        if fourthArg == 4:
                            pyautogui.press("esc")
                if diff_eyebrows < 0.076801:
                    end_time_eyebrow = time.time()
                if diff_nose_right > 0.194273:
                    detected_eyebrows = 0
                    detected_mouth_length = 0
                    detected_mouth_width = 0
                    mouse.move(10, 0, absolute=False, duration=0.05)
                if diff_nose_left > 0.194273:
                    detected_eyebrows = 0
                    detected_mouth_length = 0
                    detected_mouth_width = 0
                    mouse.move(-10, 0, absolute=False, duration=0.05)
                if diff_nose_up > 0.28375:
                    detected_eyebrows = 0
                    detected_mouth_length = 0
                    detected_mouth_width = 0
                    mouse.move(0, -10, absolute=False, duration=0.05)
                if diff_nose_down < 0.210376:
                    detected_eyebrows = 0
                    detected_mouth_length = 0
                    detected_mouth_width = 0
                    mouse.move(0, 10, absolute=False, duration=0.05)
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(img, str(int(fps)), (20, 70), cv2.FONT_HERSHEY_DUPLEX, 3, (0, 255, 0), 3)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == 27:  # if esc is pressed end the program
            # App.get_running_app().stop() # closes the whole program
            break


class HomePage(GridLayout):
    def __init__(self, **kwargs):
        super(HomePage, self).__init__(**kwargs)
        self.cols = 2
        c = []
        c2 = []

        def callback(instance, x):
            c.insert(0, x)

        def callback2(instance, x):
            c.insert(1, x)

        def callback3(instance, x):
            c.insert(2, x)

        def callback4(instance, x):
            c.insert(3, x)

        def callback_save(instance):
            par1 = 0  # mouth_smile
            par2 = 0  # mouth_o
            par3 = 0  # eyebrows_up_more_3
            par4 = 0  # eyebrows_up_less_3
            lenC2 = len(c2)
            if lenC2 != 0:
                for i in range(0, lenC2):
                    if c2[i] == 'Smile wide with closed mouth' and c[i] == '"Esc" button':
                        par1 = 4
                    elif c2[i] == 'Smile wide with closed mouth' and c[i] == 'Left click':
                        par1 = 1
                    elif c2[i] == 'Smile wide with closed mouth' and c[i] == 'Double click':
                        par1 = 2
                    elif c2[i] == 'Smile wide with closed mouth' and c[i] == 'Right click':
                        par1 = 3
                    if c2[i] == 'Open your mouth as saying "o"' and c[i] == '"Esc" button':
                        par2 = 4
                    elif c2[i] == 'Open your mouth as saying "o"' and c[i] == 'Left click':
                        par2 = 1
                    elif c2[i] == 'Open your mouth as saying "o"' and c[i] == 'Double click':
                        par2 = 2
                    elif c2[i] == 'Open your mouth as saying "o"' and c[i] == 'Right click':
                        par2 = 3
                    if c2[i] == 'Raising the eyebrows for more than 3 sec' and c[i] == '"Esc" button':
                        par3 = 4
                    elif c2[i] == 'Raising the eyebrows for more than 3 sec' and c[i] == 'Left click':
                        par3 = 1
                    elif c2[i] == 'Raising the eyebrows for more than 3 sec' and c[i] == 'Double click':
                        par3 = 2
                    elif c2[i] == 'Raising the eyebrows for more than 3 sec' and c[i] == 'Right click':
                        par3 = 3
                    if c2[i] == 'Raising the eyebrows for less than 3 sec' and c[i] == '"Esc" button':
                        par4 = 4
                    elif c2[i] == 'Raising the eyebrows for less than 3 sec' and c[i] == 'Left click':
                        par4 = 1
                    elif c2[i] == 'Raising the eyebrows for less than 3 sec' and c[i] == 'Double click':
                        par4 = 2
                    elif c2[i] == 'Raising the eyebrows for less than 3 sec' and c[i] == 'Right click':
                        par4 = 3
            Window.close()
            came(par1, par2, par3, par4)  # while true

        def callback_s1(instance):
            c2.insert(0, instance.text)

        def callback_s2(instance):
            c2.insert(1, instance.text)

        def callback_s3(instance):
            c2.insert(2, instance.text)

        def callback_s4(instance):
            c2.insert(3, instance.text)

        dropdown = DropDown()
        btn_eyebrows_less_3_sec = Button(text='Left click', size_hint_y=None, height=40)
        btn_eyebrows_less_3_sec.bind(on_release=lambda btn_eyebrows_less_3_sec: dropdown.select(btn_eyebrows_less_3_sec.text))
        dropdown.add_widget(btn_eyebrows_less_3_sec)
        btn_eyebrows_more_3_sec = Button(text='Double click', size_hint_y=None, height=40)
        btn_eyebrows_more_3_sec.bind(on_release=lambda btn_eyebrows_more_3_sec: dropdown.select(btn_eyebrows_more_3_sec.text))
        dropdown.add_widget(btn_eyebrows_more_3_sec)
        btn_mouth_o = Button(text='"Esc" button', size_hint_y=None, height=40)
        btn_mouth_o.bind(on_release=lambda btn_mouth_o: dropdown.select(btn_mouth_o.text))
        dropdown.add_widget(btn_mouth_o)
        btn_mouth_smile = Button(text='Right click', size_hint_y=None, height=40)
        btn_mouth_smile.bind(on_release=lambda btn_mouth_smile: dropdown.select(btn_mouth_smile.text))
        dropdown.add_widget(btn_mouth_smile)
        
        dropdown2 = DropDown()
        btn_eyebrows_less_3_sec = Button(text='Left click', size_hint_y=None, height=40)
        btn_eyebrows_less_3_sec.bind(on_release=lambda btn_eyebrows_less_3_sec: dropdown2.select(btn_eyebrows_less_3_sec.text))
        dropdown2.add_widget(btn_eyebrows_less_3_sec)
        btn_eyebrows_more_3_sec = Button(text='Double click', size_hint_y=None, height=40)
        btn_eyebrows_more_3_sec.bind(on_release=lambda btn_eyebrows_more_3_sec: dropdown2.select(btn_eyebrows_more_3_sec.text))
        dropdown2.add_widget(btn_eyebrows_more_3_sec)
        btn_mouth_o = Button(text='"Esc" button', size_hint_y=None, height=40)
        btn_mouth_o.bind(on_release=lambda btn_mouth_o: dropdown2.select(btn_mouth_o.text))
        dropdown2.add_widget(btn_mouth_o)
        btn_mouth_smile = Button(text='Right click', size_hint_y=None, height=40)
        btn_mouth_smile.bind(on_release=lambda btn_mouth_smile: dropdown2.select(btn_mouth_smile.text))
        dropdown2.add_widget(btn_mouth_smile)

        dropdown3 = DropDown()
        btn_eyebrows_less_3_sec = Button(text='Left click', size_hint_y=None, height=40)
        btn_eyebrows_less_3_sec.bind(on_release=lambda btn_eyebrows_less_3_sec: dropdown3.select(btn_eyebrows_less_3_sec.text))
        dropdown3.add_widget(btn_eyebrows_less_3_sec)
        btn_eyebrows_more_3_sec = Button(text='Double click', size_hint_y=None, height=40)
        btn_eyebrows_more_3_sec.bind(on_release=lambda btn_eyebrows_more_3_sec: dropdown3.select(btn_eyebrows_more_3_sec.text))
        dropdown3.add_widget(btn_eyebrows_more_3_sec)
        btn_mouth_o = Button(text='"Esc" button', size_hint_y=None, height=40)
        btn_mouth_o.bind(on_release=lambda btn_mouth_o: dropdown3.select(btn_mouth_o.text))
        dropdown3.add_widget(btn_mouth_o)
        btn_mouth_smile = Button(text='Right click', size_hint_y=None, height=40)
        btn_mouth_smile.bind(on_release=lambda btn_mouth_smile: dropdown3.select(btn_mouth_smile.text))
        dropdown3.add_widget(btn_mouth_smile)

        dropdown4 = DropDown()
        btn_eyebrows_less_3_sec = Button(text='Left click', size_hint_y=None, height=40)
        btn_eyebrows_less_3_sec.bind(on_release=lambda btn_eyebrows_less_3_sec: dropdown4.select(btn_eyebrows_less_3_sec.text))
        dropdown4.add_widget(btn_eyebrows_less_3_sec)
        btn_eyebrows_more_3_sec = Button(text='Double click', size_hint_y=None, height=40)
        btn_eyebrows_more_3_sec.bind(on_release=lambda btn_eyebrows_more_3_sec: dropdown4.select(btn_eyebrows_more_3_sec.text))
        dropdown4.add_widget(btn_eyebrows_more_3_sec)
        btn_mouth_o = Button(text='"Esc" button', size_hint_y=None, height=40)
        btn_mouth_o.bind(on_release=lambda btn_mouth_o: dropdown4.select(btn_mouth_o.text))
        dropdown4.add_widget(btn_mouth_o)
        btn_mouth_smile = Button(text='Right click', size_hint_y=None, height=40)
        btn_mouth_smile.bind(on_release=lambda btn_mouth_smile: dropdown4.select(btn_mouth_smile.text))
        dropdown4.add_widget(btn_mouth_smile)

        self.add_widget(Label(text='Select action for Eyebrows Up for more then 3 sec:  --->\nSelect action for Eyebrows Up for more then 3 sec:  --->\nSelect action for Eyebrows Up for more then 3 sec:  --->\nSelect action for Eyebrows Up for more then 3 sec:  --->', size_hint=(.5, .2)))

        button1 = Button(text='Raising the eyebrows for less than 3 sec', size_hint=(.5, .2), pos_hint={'center_x': .5})
        button1.bind(on_release=dropdown.open)
        button1.bind(on_release=callback_s4)
        dropdown.bind(on_select=lambda instance, x: setattr(button1, 'text', x))
        dropdown.bind(on_select=callback4)
        self.add_widget(button1)

        button2 = Button(text='Raising the eyebrows for more than 3 sec', size_hint=(.5, .2), pos_hint={'center_x': .5})
        button2.bind(on_release=dropdown2.open)
        button2.bind(on_press=callback_s3)
        dropdown2.bind(on_select=lambda instance2, y: setattr(button2, 'text', y))
        dropdown2.bind(on_select=callback3)
        self.add_widget(button2)

        button3 = Button(text='Open your mouth as saying "o"', size_hint=(.5, .2), pos_hint={'center_x': .5})
        button3.bind(on_release=dropdown3.open)
        button3.bind(on_press=callback_s2)
        dropdown3.bind(on_select=lambda instance3, z: setattr(button3, 'text', z))
        dropdown3.bind(on_select=callback2)
        self.add_widget(button3)

        button4 = Button(text='Smile wide with closed mouth', size_hint=(.5, .2), pos_hint={'center_x': .5})
        button4.bind(on_release=dropdown4.open)
        button4.bind(on_press=callback_s1)
        dropdown4.bind(on_select=lambda instance4, a: setattr(button4, 'text', a))
        dropdown4.bind(on_select=callback)
        self.add_widget(button4)

        button5 = Button(text='Save', size_hint=(.10, .2))
        button5.bind(on_press=callback_save)
        self.add_widget(button5)


class MyApp(App):
    def build(self):
        return HomePage()


if __name__ == "__main__":
    MyApp().run()
