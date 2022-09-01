import PySimpleGUI as sg
from func import AuthorToday
import threading



def main():
    sg.theme('DarkAmber')  # Add a touch of color

    layout = [[sg.Text('Ссылка на книгу'), sg.InputText(key='url'), sg.Button('Ok')],
              [sg.Button('Требуется авторизация', key='Login')],
              [sg.Text('Логин', visible=False, key='1'), sg.InputText(visible=False, key='2')],
              [sg.Text('Пароль', visible=False, key='3'), sg.InputText(visible=False, key='4')],
              [sg.Output(size=(50, 20), expand_x=True, visible=False, key='out')]
              ]

    window = sg.Window('Window Title', layout, element_justification='c')
    while True:
        event, values = window.read()
        if event == 'Login':
            for elem in window.element_list():
                elem.update(visible=True)
        if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
            break
        if event == "Ok":
            window.Element('out').update(visible=True)
            at = AuthorToday(values['url'])
            my_thread = threading.Thread(target=at.start)
            my_thread.start()

    window.close()


if __name__ == '__main__':
    main()
