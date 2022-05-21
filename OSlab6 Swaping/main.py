import PySimpleGUI as sg
import random as r
import os
import shutil
import re

sg.theme('Reddit')

maxMem = 65536
maxModuleMem = 65535
readyQueue = []
ramQueue = []
hddQueue = []


def taskManager(tasks):
    discArea = os.path.abspath('Диск')
    ramArea = os.path.abspath('ОЗУ')
    for i in range(tasks):
        name = 'Задача {}'.format(i)
        task = open(name, 'wb')
        task.seek(r.randint(1, maxModuleMem) - 1)
        task.write(b'\0')
        readyQueue.append(name)
        task.close()

    statusCol = [
        sg.Text('Готовы к работе', text_color='orange'),
        sg.Text('                в ОЗУ', text_color='green'),
        sg.Text('                 на Диске', text_color='red', pad=20)
    ]
    readyLayout = [
        [sg.Button(readyQueue[i] + '\n{}K'.format(os.path.getsize(readyQueue[i])), key=readyQueue[i] + 'WAIT',
                   button_color=('black', 'white'), size=(10, 2), visible=True)] for i in range(tasks)
    ]
    ramLayout = [
        [sg.Button(readyQueue[i] + '\n{}K'.format(os.path.getsize(readyQueue[i])), key=readyQueue[i] + 'RAM',
                   button_color=('black', 'white'), size=(10, 2), visible=False)] for i in range(tasks)]

    hddLayout = [
        [sg.Text(readyQueue[i] + '\n{}K'.format(os.path.getsize(readyQueue[i])), key=readyQueue[i] + 'HDD',
                 text_color='black', size=(10, 2), visible=False)] for i in range(tasks)
    ]

    statusLayout = [
        [
            sg.Text('Свободное место на ОЗУ: {}K'.format(maxMem), key='memory')
        ]
    ]
    moduleLayout = [
        [
            statusCol,
            sg.Column(readyLayout, element_justification='top', pad=15),
            sg.VSeparator(),
            sg.Column(ramLayout, element_justification='top', pad=15),
            sg.Column(hddLayout, element_justification='c', pad=15)
        ],
        [sg.HorizontalSeparator()],
        statusLayout
    ]

    memLeft = maxMem

    moduleWindow = sg.Window('Диспетчер', moduleLayout)
    while True:
        event, values = moduleWindow.read()
        if event == sg.WIN_CLOSED:
            break

        if re.search(r'WAIT', event):
            readyQueue.remove(event[0:-4])
            if memLeft - os.path.getsize(event[0:-4]) > 0:
                memLeft = memLeft - os.path.getsize(event[0:-4])
                ramQueue.append(event[0:-4])
                moduleWindow[event].Update(visible=False)
                moduleWindow[event[0:-4] + 'RAM'].Update(visible=True, disabled=False)
                moduleWindow['memory'].Update('Свободное место на ОЗУ: {}K'.format(memLeft))
                os.replace(os.path.abspath(event[0:-4]), ramArea + '\\' + event[0:-4])
            else:
                hddQueue.append(event[0:-4])
                moduleWindow[event].Update(visible=False, disabled=True)
                moduleWindow[event[0:-4] + 'HDD'].Update(visible=True)
                os.replace(os.path.abspath(event[0:-4]), discArea + '\\' + event[0:-4])

        if re.search(r'RAM', event):
            for i in range(len(ramQueue)):
                if ramQueue[i] == event[0:-3]:
                    ramQueue.pop(i)
                    break

            memLeft = memLeft + os.path.getsize(ramArea + '\\' + event[0:-3])
            moduleWindow[event].Update(visible=False, disabled=True)

            for i in range(len(hddQueue)):
                if memLeft - os.path.getsize(discArea + '\\' + hddQueue[i]) > 0:
                    memLeft = memLeft - os.path.getsize(discArea + '\\' + hddQueue[i])
                    ramQueue.append(hddQueue[i])
                    os.replace(discArea + '\\' + hddQueue[i], ramArea + '\\' + hddQueue[i])
                    moduleWindow[hddQueue[i] + 'HDD'].Update(visible=False)
                    moduleWindow[hddQueue[i] + 'RAM'].Update(visible=True, disabled=False)

            for i in range(len(ramQueue)):
                try:
                    hddQueue.remove(ramQueue[i])
                except ValueError:
                    pass
            moduleWindow['memory'].Update('Свободное место на ОЗУ: {}K'.format(memLeft))
            os.remove(ramArea + '\\' + event[0:-3])

        if len(ramQueue) + len(hddQueue) + len(readyQueue) == 0:
            sg.popup('Все процессы завершены')
            moduleWindow.close()
    moduleWindow.close()


def winInit():
    left_layout = [
        [sg.Text('Количество Задач: 0', key='tasks')],
        [
            sg.Button('-', key='sub', size=(4, 2)),
            sg.Button('+', key='add', size=(4, 2))
        ],
        [sg.Text('  ')],
        [sg.Button('СОЗДАТЬ', key='start', size=(8, 2), button_color='red')],
    ]
    image_layout = [
        [sg.Image(filename='kbsp.png')],
        [sg.Text('Операционные системы. Практика 6')],
        [sg.Text('Свопинг')],
        [sg.Text('Выполнил студент группы БББО-11-20 Эберзин М.А')]
    ]
    layout_main = [
        [
            sg.Column(left_layout, element_justification='c'),
            sg.VSeparator(),
            sg.Column(image_layout, element_justification='c')
        ]
    ]

    moduleCounter = 0
    window = sg.Window('OS lab №6 "Swapping"', layout_main, size=(570, 320), icon='iConvert.ico')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'add' and moduleCounter < 10:
            moduleCounter += 1
            window['tasks'].Update('Количество Задач: {}'.format(moduleCounter))
        if event == 'sub' and moduleCounter != 0:
            moduleCounter -= 1
            window['tasks'].Update('Количество Задач: {}'.format(moduleCounter))
        if event == 'start' and moduleCounter != 0:
            window.Hide()
            taskManager(moduleCounter)
            window.UnHide()

        if moduleCounter != 0:
            window['start'].Update(button_color='green')
        else:
            window['start'].Update(button_color='red')

    window.close()


if __name__ == '__main__':
    try:
        os.mkdir('ОЗУ')
        os.mkdir('Диск')
    except FileExistsError:
        pass

    winInit()
