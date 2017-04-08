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
        for crit_task in filter(lambda task: task.is_failed or
                                (
                                    task.state == 'in_progress' and
                                    task.remaining.days < 3
                                ),
                                tasks_gen(self.data_file)):
            yield str(crit_task).encode('utf8')
            yield '<br>'.encode('utf8')


if __name__ == '__main__':
    http_server = make_server('127.0.0.1', 9090, WSGIApplication)
    http_server.handle_request()
