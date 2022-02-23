import labtasks as lab
import PySimpleGUI as sg

sg.theme('Reddit')


def win_init():
    layout_buttons = [
        [sg.Button('Вывести информацию о дисках', key='-1-', size=(20, 4))],
        [sg.Button('Работа с файлами', key='-2-', size=(20, 4))],
        [sg.Button('Работа с JSON', key='-3-', size=(20, 4))],
        [sg.Button('Работа с XML', key='-4-', size=(20, 4))],
        [sg.Button('Создать ZIP архив', key='-5-', size=(20, 4))],
    ]

    image_layout = [
        [sg.Image(filename='kbsp.png')],
        [sg.Text('Операционные системы. Практика 1')],
        [sg.Text('Выполнил студент группы БББО-11-20 Эберзин М.А')]
    ]
    layout = [
        [
            sg.Column(layout_buttons),
            sg.VSeparator(),
            sg.Column(image_layout, element_justification='c')
        ]
    ]
    window = sg.Window('OS lab №1', layout, size=(580, 415), icon='iConvert.ico')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-1-':
            lab.discScan()
        elif event == '-2-':
            window.Hide()
            lab.fileManagement()
            window.UnHide()
        elif event == '-3-':
            window.Hide()
            lab.jsonManagement()
            window.UnHide()
        elif event == '-4-':
            window.Hide()
            lab.xmlManagement()
            window.UnHide()
        elif event == '-5-':
            window.Hide()
            lab.zipManagement()
            window.UnHide()

    window.close()


if __name__ == '__main__':
    win_init()
