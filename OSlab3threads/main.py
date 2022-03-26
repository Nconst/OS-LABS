import PySimpleGUI as sg
import Workers as w

sg.theme('Reddit')


def win_init():
    layout_workers = [
        [
            sg.Button(' - ', key='-producer(-)-'),
            sg.Text('Производители'),
            sg.Button(' + ', key='-producer(+)-')
        ],
        [sg.Text('(0)', key='-producer count-')],
        [
            sg.Button(' - ', key='-consumer(-)-'),
            sg.Text('Потребители'),
            sg.Button(' + ', key='-consumer(+)-')
        ],
        [sg.Text('(0)', key='-consumer count-')],
        [sg.Text('  ')],
        [sg.Text('  ')],
        [
            sg.Button('Старт', key='-start-', size=(9, 1)),
            sg.Button('Стоп', key='-stop-', size=(9, 1))
        ]
    ]

    image_layout = [
        [sg.Image(filename='kbsp.png')],
        [sg.Text('Операционные системы. Практика 3')],
        [sg.Text('Выполнил студент группы БББО-11-20 Эберзин М.А')]
    ]
    layout = [
        [
            sg.Column(layout_workers, vertical_alignment='middle', element_justification='c'),
            sg.VSeparator(),
            sg.Column(image_layout, element_justification='c')
        ]
    ]
    window = sg.Window('OS lab №3', layout, size=(580, 290), icon='iConvert.ico')

    consumer_count = 0
    producer_count = 0
    producer_list = []
    consumer_list = []
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-producer(-)-' and producer_count > 0:
            producer_count -= 1
            window['-producer count-'].Update('({})'.format(producer_count))
            del producer_list[-1]
        if event == '-producer(+)-' and producer_count < 10:
            producer_count += 1
            window['-producer count-'].Update('({})'.format(producer_count))
            producer_list.append(w.Producer())
        if event == '-consumer(-)-' and consumer_count > 0:
            consumer_count -= 1
            window['-consumer count-'].Update('({})'.format(consumer_count))
            del consumer_list[-1]
        if event == '-consumer(+)-' and consumer_count < 10:
            consumer_count += 1
            window['-consumer count-'].Update('({})'.format(consumer_count))
            consumer_list.append(w.Consumer())

        if event == '-start-' and producer_count != 0 and consumer_count != 0:
            for i in range(len(producer_list)):
                producer_list[i].start()
            for i in range(len(consumer_list)):
                consumer_list[i].start()
            producer_count = 0
            consumer_count = 0
            window['-consumer count-'].Update('({})'.format(consumer_count))
            window['-producer count-'].Update('({})'.format(producer_count))

        if event == '-stop-':
            for i in range(len(producer_list)):
                producer_list[i].sit_down()
                producer_list[i].join()
            producer_list = []
            for i in range(len(consumer_list)):
                consumer_list[i].last_day_of_work()
                consumer_list[i].join()
            consumer_list = []

    window.close()


if __name__ == '__main__':
    win_init()
