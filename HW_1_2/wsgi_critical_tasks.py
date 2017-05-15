from wsgiref.simple_server import make_server
from load_tasks import tasks_gen


class WSGIApplication(object):
    data_file = 'dataset.yml'
    default_headers = [
        ('Content-Type', 'text/html; charset=utf8'),
        ('Server', 'WSGICriticalTasks/1.0'),
    ]

    def __init__(self, environment, start_response_callback):
        self.environment = environment
        self.start_response = start_response_callback

    def __iter__(self):
        self.start_response('200 OK', self.default_headers)
        crit_tasks = (
            task for task in tasks_gen(self.data_file)
            if task.is_critical
        )
        for crit_task in crit_tasks:
            yield str(crit_task).encode('utf8')
            yield '<br>'.encode('utf8')


if __name__ == '__main__':
    http_server = make_server('127.0.0.1', 9090, WSGIApplication)
    http_server.handle_request()
