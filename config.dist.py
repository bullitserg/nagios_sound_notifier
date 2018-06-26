nagios_web_page = 'http://nagios-m1.etp-micex.ru/nagios/cgi-bin/status.cgi?hostgroup=all&style=detail&servicestatustypes=28&hoststatustypes=15'
nagios_local_page = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/nagios.html'
nagios_login = '****'
nagios_password = '****'
nagios_page_classes = ['statusBGCRITICAL', 'statusBGWARNING']

metric_source = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/metrics.source'

prefix_text = 'Внимание!'
default_text = 'Найдена новая ошибка.'

play_command = 'nohup echo "%s" | festival --tts --language russian > /dev/null 2> /dev/null &'


sleep_time = 5

log_file = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/notifier.log'
