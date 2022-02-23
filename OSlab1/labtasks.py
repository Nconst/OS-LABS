import json
import os
import psutil
import PySimpleGUI as sg
import xml.etree.cElementTree as ET
import zipfile as z


def getInfoLayout():
    info_fields = [
        [
            sg.Text(' ' * 29 + 'Фамилия'),
            sg.InputText(key='surname', size=(50, 1), do_not_clear=False)
        ],
        [
            sg.Text(' ' * 37 + 'Имя'),
            sg.InputText(key='name', size=(50, 1), do_not_clear=False)
        ],
        [
            sg.Text(' ' * 33 + 'Группа'),
            sg.InputText(key='group', size=(50, 1), do_not_clear=False)
        ],
        [
            sg.Text('Имя пользователя на GitHub'),
            sg.InputText(key='git', size=(50, 1), do_not_clear=False)
        ],
        [
            sg.Button('Добавить', key='add'),
            sg.Button('Продолжить', key='Ok', visible=False),
            sg.Button('Назад', key='back'),
            sg.Text(text='Добавлено: 0', text_color='green', key='success')
        ]
    ]
    return info_fields


def menuLayout(button1, button2, button3, button4):
    navigation_buttons = [
        [sg.Button(button1, key='-0-', size=(18, 2))],
        [sg.Button(button2, key='-1-', size=(18, 2))],
        [sg.Button(button3, key='-2-', size=(18, 2))],
        [sg.Button(button4, key='-3-', size=(18, 2))]
    ]
    go_back_button = [[sg.Button('>', key='back', size=(4, 1), button_color='#f84c4c')]]
    complete_layout = [
        [
            sg.Column(navigation_buttons),
            sg.VSeparator(),
            sg.Column(go_back_button, element_justification='right', vertical_alignment='bottom')
        ]
    ]
    return complete_layout


def discScan():
    d = psutil.disk_partitions()
    i = 0
    disc_info = ''
    for disc in d:
        try:
            p = psutil.disk_usage(d[i][0])
            disc_info += 'Диск {} \n'.format(d[i][0])
            disc_info += 'Тип файловой системы: {}\n'.format(d[i][3])
            disc_info += 'Обьем: {} ГБ\n'.format(p[0] // (2 ** 30))
            disc_info += 'Свободно: {} ГБ\n'.format(p[2] // (2 ** 30)) + '-' * 50 + '\n'
        except (BaseException, SystemError):
            disc_info += 'Диск {} не используется\n'.format(d[i][0]) + '-' * 50 + '\n'
        i += 1
    sg.Popup(disc_info, title='Диски')


def fileManagement():
    layout = menuLayout('Создать файл', 'Записать данные', 'Прочитать файл', 'Удалить файл')

    file_window = sg.Window('Файлы', layout, size=(265, 210))
    while True:
        event, values = file_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        if event == '-0-':
            try:
                entered_name = sg.popup_get_text('Название файла', title='Создать файл')
                while entered_name.isspace() or len(entered_name) == 0:
                    sg.popup('Поле не может быть пустым')
                    entered_name = sg.popup_get_text('Введите имя файла', title='Создать файл')

                new_file = open('{}.txt'.format(entered_name), 'w+')
                new_file.close()
                sg.popup('Файл успешно создан')
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-1-':
            try:
                to_append = open(sg.popup_get_file('Выберите файл для записи', title='Запись в файл',
                                                   file_types=(('ALL Files', '*.txt'),)), 'a+')
                to_append.write(sg.popup_get_text('Введите текст', title=''))
                to_append.close()
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-2-':
            try:
                to_read = open(sg.popup_get_file('Выберите файл для чтения', title='Чтение файла',
                                                 file_types=(('ALL Files', '*.txt'),)), 'r')
                sg.popup(to_read.read(), title='Содержимое файла')
                to_read.close()
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-3-':
            try:
                os.remove(sg.popup_get_file('Выберите файл для удаления', title='Удалить файл',
                                            file_types=(('ALL Files', '*.txt'),)))
                sg.popup('Файл успешно удален', title='Success')
            except (FileNotFoundError, BaseException):
                sg.popup('Невозможно удалить файл', title='Something went wrong')
    file_window.close()


def getInfoForJson():
    layout = getInfoLayout()
    enter_window = sg.Window('Ввод данных', layout)

    success_counter = 0
    entered_info = {}
    while True:
        event, values = enter_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        elif event == 'add':
            success_counter += 1
            entered_info['colleague{}'.format(success_counter)] = []
            entered_info['colleague{}'.format(success_counter)].append({
                'NAME': values['name'],
                'SURNAME': values['surname'],
                'GROUP': values['group'],
                'GIT': 'https://github.com/{}'.format(values['git'])
            })
            enter_window['success'].update('Добавлено {}'.format(success_counter))
            enter_window['Ok'].update(visible=True)

        elif event == 'Ok':
            try:
                add_file = open(sg.popup_get_file('Выберите файл для записи', file_types=(('ALL Files', '*.json'),)),
                                'w')
                json.dump(entered_info, add_file)
                add_file.close()
                sg.popup('Информация обновлена')
                break
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

    enter_window.close()


def jsonManagement():
    layout = menuLayout('Создать файл JSON', 'Создать объект и записать в файл', 'Прочитать файл JSON', 'Удалить файл')

    json_window = sg.Window('Работа с JSON', layout, size=(265, 210))
    while True:
        event, values = json_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        if event == '-0-':
            try:
                entered_name = sg.popup_get_text('Введите имя файла', title='Создать json')
                while entered_name.isspace() or len(entered_name) == 0:
                    sg.popup('Поле не может быть пустым')
                    entered_name = sg.popup_get_text('Введите имя файла', title='Создать json')

                outfile = open('{}.json'.format(entered_name), 'w')
                outfile.close()
                sg.popup('Файл успешно создан')
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-1-':
            json_window.Hide()
            getInfoForJson()
            json_window.UnHide()

        elif event == '-2-':
            try:
                with open(sg.popup_get_file('Выберите файл для прочтения', file_types=(('ALL Files', '*.json'),),
                                            title='Прочитать файл')) as json_file:
                    json_data = json.load(json_file)

                    message_text = ''
                    for i in range(1, len(json_data) + 1):
                        for person in json_data['colleague{}'.format(i)]:
                            message_text += person['NAME'] + '\n' + person['SURNAME'] + '\n' + person['GROUP'] + '\n' + \
                                            person['GIT'] + '\n' + '-' * 50 + '\n'
                json_file.close()
                sg.popup(message_text, title='Считанные данные')

            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-3-':
            try:
                os.remove(sg.popup_get_file('Выберите файл для удаления', title='Удалить файл',
                                            file_types=(('ALL Files', '*.json'),)))
                sg.popup('Файл успешно удален', title='Success')
            except (FileNotFoundError, BaseException):
                sg.popup('Невозможно удалить файл', title='Something went wrong')

    json_window.close()


def getInfoForXml():
    layout = getInfoLayout()
    enter_window = sg.Window('Ввод данных', layout)

    file_to_parse = sg.popup_get_file('Выберите файл для записи', title='Запись в файл',
                                      file_types=(('ALL Files', '*.xml'),))
    if file_to_parse is None:
        return
    elif file_to_parse.isspace() or len(file_to_parse) == 0:
        sg.popup('Невозможно найти файл')
        return

    success_counter = 0
    while True:
        event, values = enter_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        elif event == 'add':
            success_counter += 1
            tree = ET.parse(file_to_parse)
            root = tree.getroot()
            data = root[0]
            entern = ET.SubElement(data, 'colleague')
            ET.SubElement(entern, 'name').text = values['name']
            ET.SubElement(entern, 'surname').text = values['surname']
            ET.SubElement(entern, 'group').text = values['group']
            ET.SubElement(entern, 'git').text = 'https://github.com/{}'.format(values['git'])
            tree.write(file_to_parse)
            enter_window['success'].update('Добавлено {}'.format(success_counter))

    enter_window.close()


def xmlManagement():
    layout = menuLayout('Создать файл XML', 'Создать объект и записать в файл', 'Прочитать файл XML', 'Удалить файл')

    xml_window = sg.Window('Работа с XML', layout, size=(265, 210))
    while True:
        event, values = xml_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        elif event == '-0-':
            try:
                entered_name = sg.popup_get_text('Введите имя файла', title='Создать XML')
                while entered_name.isspace() or len(entered_name) == 0:
                    sg.popup('Поле не может быть пустым')
                    entered_name = sg.popup_get_text('Введите имя файла', title='Создать XML')

                root = ET.Element('root')
                ET.SubElement(root, 'data')

                tree = ET.ElementTree(root)
                tree.write('{}.xml'.format(entered_name))
                sg.popup('Файл успешно создан')
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Error')

        elif event == '-1-':
            xml_window.Hide()
            getInfoForXml()
            xml_window.UnHide()

        elif event == '-2-':
            try:
                xml_to_read = sg.popup_get_file('Выберите файл для считывания', title='Прочитать файл',
                                                file_types=(('ALL Files', '*.xml'),))
                output_text = ''
                tree = ET.parse(xml_to_read)
                root = tree.getroot()
                for data in root:
                    for entities in data:
                        for entity_info in entities:
                            output_text += entity_info.text + '\n'
                        output_text += '-' * 60 + '\n'
                sg.popup(output_text, title='Считанные данные')
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так', title='Something went wrong')

        elif event == '-3-':
            try:
                os.remove(sg.popup_get_file('Выберите файл для удаления', title='Удалить файл',
                                            file_types=(('ALL Files', '*.xml'),)))
                sg.popup('Файл успешно удален', title='Success')
            except (FileNotFoundError, BaseException):
                sg.popup('Невозможно удалить файл', title='Something went wrong')

    xml_window.close()


def zipManagement():
    layout = menuLayout('Создать архив', 'Добавить в архив', 'Разархивировать и вывести данные', 'Удалить архив')

    zip_window = sg.Window('Работа с ZIP архивами', layout, size=(265, 210))
    while True:
        event, values = zip_window.read()
        if event == sg.WIN_CLOSED or event == 'back':
            break
        if event == '-0-':
            try:
                zip_name = sg.popup_get_text('Назовите архив', title='Создать архив')
                while zip_name.isspace() or len(zip_name) == 0:
                    sg.popup('Имя архива не может быть пустым', title='user dumb')
                    zip_name = sg.popup_get_text('Назовите архив', title='Создать архив')

                zip_file = z.ZipFile('{}.zip'.format(zip_name), mode='w')
                zip_file.close()
                sg.popup('Архив успешно создан')
            except (FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так')
        elif event == '-1-':
            try:
                zip_folder = z.ZipFile(sg.popup_get_file('Выберите в какой архив поместить файл', title='Выбор архива',
                                                         file_types=(('ALL Files', '*.zip'),)), mode='a')
                file_to_zip = sg.popup_get_file('Выберите файл для аривации', title='Архивирование')
                zip_folder.write(file_to_zip)
                zip_folder.close()
            except(FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так')
        elif event == '-2-':
            try:
                zip_to_unzip = z.ZipFile(sg.popup_get_file('Выберите архив для извлечения', title='Выбор архива',
                                                           file_types=(('ALL Files', '*.zip'),)), mode='r')
                zip_to_unzip.extractall('unzipped data')

                unzipped_info = ''
                for data in zip_to_unzip.infolist():
                    unzipped_info += data.filename + '\n'
                    unzipped_info += '|Дата создания: {0}:{1}:{2} \n'.format(data.date_time[2], data.date_time[1],
                                                                             data.date_time[0])
                    unzipped_info += '|Размер: {}'.format(data.file_size) + '\n' + '-' * 70 + '\n'

                sg.popup('Архив успешно распакован\nИнформация:\n{}'.format(unzipped_info), title='Информация')
                zip_to_unzip.close()

            except(FileNotFoundError, BaseException):
                sg.popup('Что-то пошло не так')
        elif event == '-3-':
            try:
                os.remove(sg.popup_get_file('Выберите архив для удаления', title='Выбор архива',
                                            file_types=(('ALL Files', '*.zip'),)))
                sg.popup('Архив успешно удален')
            except (FileNotFoundError, BaseException):
                sg.popup('Невозможно удалить архив')

    zip_window.close()
