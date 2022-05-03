import re
import PySimpleGUI as sg
import Modules as m

sg.theme('Reddit')


def module_window(modules):
    for i in range(modules):
        newModule = m.Module(i)
        newModule.start()
        m.readyQueue.put(newModule)
        m.moduleAccess.append(newModule)

    statusCol = [
        sg.Text('Готовы к работе', text_color='orange'),
        sg.Text('         Работают', text_color='green'),
        sg.Text('         Завершились', text_color='red')
    ]
    readyLayout = [
        [sg.Text('Модуль №{}'.format(i), key='waiting{}'.format(i), text_color='black', visible=True)] for i in
        range(modules)
    ]
    workingLayout = [
        [sg.Button('Модуль №{}'.format(i), key='{}'.format(i), button_color=('black', 'white'),
                   visible=False)]
        for i in range(modules)]
    endedLayout = [[sg.Text('Модуль №{}'.format(i), key='STOPPED{}'.format(i), text_color='black', visible=False)] for i
                   in
                   range(modules)]
    managementButtons = [
        [sg.Button('Пуск', key='start')]
    ]
    statusLayout = [
        [
            sg.Text('Модуль №{} | Прогресс выполнения: '.format(i)),
            sg.Text('0', key='current{}'.format(i)),
            sg.Text('| Цель: '),
            sg.Text('{}'.format(m.moduleAccess[i].getGoal()))
        ] for i in range(modules)
    ]
    moduleLayout = [
        [
            managementButtons,
            statusCol,
            sg.Column(readyLayout, element_justification='top', pad=15),
            sg.Column(workingLayout, element_justification='top', pad=15),
            sg.Column(endedLayout, element_justification='c', pad=15)
        ],
        [sg.HorizontalSeparator()],
        statusLayout
    ]
    moduleWindow = sg.Window('Диспетчер', moduleLayout, size=(700, 370))
    pattern = '[0-9]'
    while True:
        event, values = moduleWindow.read(timeout=10)

        if event == sg.TIMEOUT_EVENT:
            for i in range(len(m.moduleAccess)):
                recentInfo = m.moduleAccess[i].getProgress()
                moduleWindow['current{}'.format(i)].Update(recentInfo)

        if m.killedQueue.qsize() != 0:
            while m.killedQueue.qsize() != 0:
                killedModule = m.killedQueue.get()
                moduleWindow[str(killedModule.getNum())].Update(visible=False, disabled=True)
                moduleWindow['STOPPED' + str(killedModule.getNum())].Update(visible=True)
        if event == sg.WIN_CLOSED:
            break
        if event == 'start' and m.readyQueue.qsize() != 0:
            module = m.readyQueue.get()
            module.resume()

            print('got module << Модуль{} >> out of queue'.format(module.getNum()))
            moduleWindow['waiting{}'.format(module.getNum())].Update(visible=False)
            moduleWindow['{}'.format(module.getNum())].Update(visible=True, disabled=False)

        if re.search(pattern, event):
            moduleWindow[event].Update(visible=False, disabled=True)
            modulePaused = m.moduleAccess[int(event)]
            if modulePaused.getStatus():
                moduleWindow['waiting' + event].Update(visible=False)
            else:
                moduleWindow['waiting' + event].Update(visible=True)
            m.readyQueue.put(modulePaused)
            modulePaused.pause()

    moduleWindow.close()
    while len(m.moduleAccess) != 0:
        endModule = m.moduleAccess.pop()
        endModule.join()
    while m.killedQueue.qsize() != 0:
        endModule = m.killedQueue.get()
        endModule.join()


def start_window():
    left_layout = [
        [sg.Text('Количество модулей: 0', key='streams')],
        [
            sg.Button('-', key='sub', size=(4, 2)),
            sg.Button('+', key='add', size=(4, 2))
        ],
        [sg.Text('  ')],
        [sg.Button('СОЗДАТЬ', key='start', size=(8, 2), button_color='red')],
    ]
    image_layout = [
        [sg.Image(filename='kbsp.png')],
        [sg.Text('Операционные системы. Практика 5')],
        [sg.Text('Выполнил студент группы БББО-11-20 Эберзин М.А')]
    ]
    layout_main = [
        [
            sg.Column(left_layout, element_justification='c'),
            sg.VSeparator(),
            sg.Column(image_layout, element_justification='c')
        ]
    ]

    streamCounter = 0
    window = sg.Window('OS lab №5', layout_main, size=(570, 290), icon='iConvert.ico')
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'add' and streamCounter < 3:
            streamCounter += 1
            window['streams'].Update('Количество модулей: {}'.format(streamCounter))
        if event == 'sub' and streamCounter != 0:
            streamCounter -= 1
            window['streams'].Update('Количество модулей: {}'.format(streamCounter))
        if event == 'start' and streamCounter != 0:
            window.Hide()
            module_window(streamCounter)
            window.UnHide()

        if streamCounter != 0:
            window['start'].Update(button_color='green')
        else:
            window['start'].Update(button_color='red')

    window.close()


if __name__ == '__main__':
    start_window()
