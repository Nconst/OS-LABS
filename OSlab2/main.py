import PySimpleGUI as sg
import hashlib
import itertools
import multiprocessing
import string
import binascii
from functools import partial
from itertools import product

alphabet = string.ascii_lowercase.encode()
alphabet_with_digits = string.ascii_letters + string.digits
sg.theme('Reddit')


def sha256(data):
    return hashlib.sha256(data).digest()


def check_sha256(repls_parent, bytes_format, n, target_sha256):
    for repls in itertools.product(alphabet, repeat=n):
        data = bytes_format % (repls_parent + repls)
        if sha256(data) == target_sha256:
            return data


def brute_force_shredded(mask, target_sha256, n_cutoff=5):
    bytes_format = mask.replace(b'%', b'%%').replace(b'*', b'%c')
    mp_check = partial(check_sha256, bytes_format=bytes_format, n=min(n_cutoff, mask.count(b'*')),
                       target_sha256=target_sha256)
    n = max(0, mask.count(b'*') - n_cutoff)
    all_repls_parent = itertools.product(alphabet, repeat=n)
    with multiprocessing.Pool() as pool:
        for data in pool.imap_unordered(mp_check, all_repls_parent):
            if data is not None:
                return data
    sg.popup('Декодирование не удалось')
    return


def brute_force_mono(mask, hsh, verbose=False):
    pwd_pat = mask.replace('{', '{{').replace('}', '}}').replace('*', '{}')
    n = mask.count('*')
    i = 0
    for chars in product(alphabet_with_digits, repeat=n):
        if verbose:
            i += 1
            if i % 10000 == 0:
                print('Iterations: {}'.format(i))
        if hsh == hashlib.sha256(pwd_pat.format(*chars).encode()).hexdigest():
            return pwd_pat.format(*chars)
    sg.popup('Декодирование не удалось')
    return


def hash_keys_layout(hash_to_choose):
    create_buttons = [
        [sg.Button(hash_to_choose[hashes], key=hashes)] for hashes in
        range(len(hash_to_choose))
    ]

    key_window = sg.Window('Выберите хэш', create_buttons)
    while True:
        event, values = key_window.read()
        if event == sg.WIN_CLOSED:
            break
        else:
            key_window.close()
            return hash_to_choose[event]

    key_window.close()


def win_init():
    layout_buttons = [
        [sg.Button('Выбрать файл, хранящий хэш значения', key='-0-', size=(20, 4))],
        [sg.Button('Начать подбор', key='-1-', size=(20, 4))]
    ]

    image_layout = [
        [sg.Image(filename='kbsp.png')],
        [sg.Text('Операционные системы. Практика 2')],
        [sg.Text('Выполнил студент группы БББО-11-20 Эберзин М.А')]
    ]
    layout = [
        [
            sg.Column(layout_buttons, vertical_alignment='top'),
            sg.VSeparator(),
            sg.Column(image_layout, element_justification='c')
        ]
    ]
    window = sg.Window('OS lab №1', layout, size=(580, 290), icon='iConvert.ico')
    explored_hash = None

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == '-0-':
            try:
                get_hash = open(sg.popup_get_file('Выберите файл с хэш значениями', title='Выбрать хэш',
                                                  file_types=(('ALL Files', '*.txt'),)), 'r')
                hash_info = [line.rstrip() for line in get_hash]
                print(hash_info)
                get_hash.close()
                explored_hash = hash_keys_layout(hash_info)
                print(type(explored_hash))
            except (FileNotFoundError, BaseException):
                sg.popup('Невозможно открыть файл')

        if event == '-1-' and explored_hash is not None:
            get_mode = sg.popup_yes_no('Запустить подбор в многопоточном режиме?', title='Выбор режима')
            if get_mode == 'Yes':
                shredded_value = brute_force_shredded(b'*****', binascii.unhexlify(explored_hash.encode()))
                sg.popup(shredded_value.decode())
            elif get_mode == 'No':
                sg.popup(brute_force_mono('*****', explored_hash, verbose=False))

    window.close()


if __name__ == '__main__':
    win_init()
