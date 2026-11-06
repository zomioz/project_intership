import PySimpleGUI as sg
import os
from training_model_bonus import training_model
from create_image_bonus import create_image
from math_function_bonus import calculate_precision, calculate_mse, calculate_r2
from get_value_bonus import get_students, output_file
from load_bonus import PERIODS

IMAGES = ['bonus_regression_all.png', 'bonus_regression_linearfunction.png', 'bonus_regression_scatter.png']
STUDENT_BUTTONS = ["Display csv file", "Display linear regression function", "Show Precision", "Display all"]
DEFAULT_PERIOD = "week"

def apply_modern_theme():

    '''
    Function that define a new theme for GUI
    Argument: None
    Return: None
    '''

    sg.theme('DarkBlue3')
    sg.set_options(
        font=('Segoe UI', 11),
        button_color=('#FFFFFF', '#0078D4'),
        element_padding=(5, 5),
        border_width=1,
        text_color='#FFFFFF'
    )


def remove_files():

    '''
    Function that remove all files created by the bonus
    Argument: None
    Return: None
    '''

    for file in IMAGES + [output_file(period) for period in PERIODS]:
        try:
            os.remove(file)
        except FileNotFoundError:
            continue


def show_image(filename):

    '''
    Function that display an image in a new window until it is closed
    Argument: the path of the image
    Return: None
    '''

    layout_img = [[sg.Image(filename=filename)], [sg.Button("Close")]]
    win_img = sg.Window("Image", layout_img)

    while True:
        event1, values1 = win_img.read()
        if event1 == sg.WIN_CLOSED or event1 == "Close":
            break
    win_img.close()


def refresh(window, period):

    '''
    Function that update the student list and enable or disable the buttons depending on
    the training already done for the selected period
    Argument: the window, the selected period ("day", "week" or "month")
    Return: True if the selected period has been trained
    '''

    students = get_students(output_file(period))
    trained = len(students) > 0

    window["student"].update(values=students, value=students[0] if trained else "", disabled=not trained)
    for button in STUDENT_BUTTONS:
        window[button].update(disabled=not trained)
    window["Quit and Clean"].update(disabled=not any(get_students(output_file(p)) for p in PERIODS))
    return trained


def display_gui():

    '''
    Function that display the GUi, and handle all button of GUI. Launch the appropriate function in each case.
    The linear regression is done for each student on his log time by day, week or month (selected in the list),
    the student displayed is selected in the list
    Argument: None
    Return: None
    '''

    apply_modern_theme()

    layout = [[sg.Text("Greetings from simple ft_linear_regression GUI\nFirst you should launch the training model right under")],
            [sg.Text("Period :"), sg.Combo(list(PERIODS), default_value=DEFAULT_PERIOD, key="period", readonly=True, enable_events=True)],
            [sg.Button("Launch Training Model")],
            [sg.Text("Student (login) :"), sg.Combo([], key="student", readonly=True, disabled=True, size=(20, 1))],
            [sg.Button("Display csv file", disabled=True)],
            [sg.Button("Display linear regression function", disabled=True)],
            [sg.Button("Show Precision", disabled=True)],
            [sg.Button("Display all", disabled=True)],
            [sg.Button("Simple Quit")],
            [sg.Button("Quit and Clean", disabled=True)]]

    window = sg.Window("Bonus_GUI", layout, margins=(500, 300), finalize=True)
    Training_done = refresh(window, DEFAULT_PERIOD)

    try:
        while True:

            event, values = window.read()

            if event == "Simple Quit" or event == sg.WIN_CLOSED:
                break


            if event == "Quit and Clean":
                remove_files()
                break


            if event == "period":
                Training_done = refresh(window, values["period"])


            if event == "Launch Training Model":
                period = values["period"]
                if training_model(period) == False:
                    sg.popup_quick_message('Data.csv isnt present, invalid or has less than two complete ' + period + 's, cant launch the training module', auto_close_duration=3)
                else:
                    Training_done = refresh(window, period)
                    sg.popup_quick_message('Training Complete!', auto_close_duration=2)


            if event in ("Show Precision", "Display csv file", "Display linear regression function", "Display all"):
                if not Training_done:
                    sg.popup_quick_message("Training hasnt been launch for this period. Please launch it before doing anything else.", auto_close_duration=3)
                    continue

                login = values["student"]
                period = values["period"]

                if event == "Show Precision":
                    mse, rmse, r2 = calculate_precision(login, period)
                    message = "The model of the student " + str(login) + " is: " + "{:.1f}".format(r2 * 100) + "% precise.\nOn average, its log time predictions are off by about: " + "{:.2f}".format(rmse) + " minutes per " + period
                    sg.popup_quick_message(message, auto_close_duration=6)
                    continue

                create_image(login, period)
                if event == "Display csv file":
                    show_image("bonus_regression_scatter.png")
                elif event == "Display linear regression function":
                    show_image("bonus_regression_linearfunction.png")
                else:
                    show_image("bonus_regression_all.png")

    except KeyboardInterrupt:
        print("Programme interrompu par l'utilisateur (Ctrl+C)")
        remove_files()
        window.close()
