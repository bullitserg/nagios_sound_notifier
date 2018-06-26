nagios_web_page = 'http://nagios-m1.etp-micex.ru/nagios/cgi-bin/status.cgi?hostgroup=all&style=detail&servicestatustypes=28&hoststatustypes=15'
nagios_local_page = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/nagios.html'
nagios_login = '****'
nagios_password = '****'
nagios_page_classes = ['statusBGCRITICAL', 'statusBGWARNING']

metric_source = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/metrics.source'

prefix_sound = 'prefix.mp3'
default_sound = 'default.mp3'
play_command = 'nohup /usr/bin/mplayer %s > /dev/null 2> /dev/null &'
sounds_dir = 'C:/Users/belim/PycharmProjects/Nagios sound notifier/sounds'

sleep_time = 5

log_format = '[%(asctime)s]# > %(message)s'
