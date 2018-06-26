import requests
import re
import os
from time import sleep
from os.path import join as p_join, normpath
import sys
import lxml.html as html
import itertools
from config import *
from logger_module import logger

nagios_local_page = normpath(nagios_local_page)
metric_source = normpath(metric_source)
sounds_dir = normpath(sounds_dir)
log_file = normpath(log_file)


def main():

    logger.info('Nagios sound notifier started')

    def _list_from_indexes_and_period(in_list, *indexes, period=2):
        """Функция выделяет из набора данных значения по индексу в заданном порядке, в рамках определенного периода
        in_list -- входящий лист данных
        indexes -- индексы через запятую (с 1) в требуемом порядке
        period -- длина периода обработки (по умолчанию period=2)
        Результатом функции является набор вида [[2,3],[5,6],...]
        """
        in_list = list(in_list)
        in_list_len = len(in_list)
        if not in_list_len % period == 0:
            raise Exception('Недопустимый период %s для листа длиной %s' % (period, in_list_len))
        for index in indexes:
            if index > period:
                raise Exception('Индекс=%s выходит за пределы периода %s' % (index, period))

        out_list = []
        while in_list:
            period_list = map(lambda index: in_list[index - 1], indexes)
            out_list.append(list(period_list))
            in_list = in_list[period:]

        return out_list

    # переход в домашнюю директорию
    os.chdir(os.path.realpath(os.path.dirname(sys.argv[0])))

    # получаем сведения о метриках, которые нам интересны
    with open(metric_source, encoding='utf8') as metric_file:
        metric_list = metric_file.readlines()
    metric_list = [metric.replace('\n', '').split(';') for metric in metric_list
                   if not metric.startswith('#')
                   and metric.replace('\n', '')]
    last_error_strings = []

    while True:

        # Скачиваем страницу и кладем ее в файл nagios_local_page
        nagios_web_page_file = requests.get(nagios_web_page, auth=(nagios_login, nagios_password))
        with open(nagios_local_page, mode='wb') as web_str:
            web_str.write(nagios_web_page_file.content)

        # разбираем страницы нагиос на лист со словарем данных
        # парсим странички
        out_data = []
        page = html.parse(nagios_local_page)
        for nagios_page_class in nagios_page_classes:
            class_root = page.getroot().find_class(nagios_page_class)

            # отбор строк с нужным классом из всех строк
            separated_class_lists = _list_from_indexes_and_period(class_root, 2, period=7)
            # лист для записи всех проблемных _list_from_indexes_and_period
            for critical_list in separated_class_lists:
                # лист для метрики
                class_metric_list = []
                for class_data in critical_list:
                    # находим и добавляем название сервера в лист
                    for iterData in class_data.iterlinks():
                        class_metric_list.append(re.search('host=(.*)&', iterData[2]).group(1))
                    class_metric_list.append(class_data.text_content())
                    class_metric_list.append(nagios_page_class.replace('statusBG', ''))
                # добавляем список по метрике в class_out_list
                    out_data.append(class_metric_list)

        # настало время проверить, надо ли по каким то оповестить
        error_strings = []
        sound_files = []
        for element in itertools.product(out_data, metric_list):
            for test in range(3):
                if not element[0][test] == element[1][test] and element[1][test]:
                    break
            else:
                error_string = ' / '.join(element[0])
                error_strings.append(error_string)

                # а вдруг по нему ранее оповещали?
                if error_string not in last_error_strings:
                    # давай запишем в лог
                    logger.info(error_string)

                    # и найдем нужный звуковой файл
                    sound_file = element[1][3]
                    if not sound_file:
                        sound_file = default_sound
                    sound_files.append(sound_file)

        # обновляем сведения об обработанных ошибках
        last_error_strings = error_strings
        # настало время воспроизвести то, что мы нашли
        # создаем строку для воспроизведения с полными путями
        sound_files = ' '.join([p_join(sounds_dir, file) for file in set(sound_files)])
        if sound_files:
            sound_files = ' '.join([prefix_sound, sound_files])
            notify_command = play_command % sound_files
            os.system(notify_command)
            logger.info('Exec "%s"' % notify_command)
        sleep(sleep_time)

if __name__ == '__main__':
    logger = logger()
    try:
        main()
    # если при исполнении будут исключения - кратко выводим на терминал, остальное - в лог
    except Exception as e:
        logger.fatal('Fatal error! Exit', exc_info=True)
        print('Critical error: %s' % e)
        print('More information in log file')
        exit(1)
