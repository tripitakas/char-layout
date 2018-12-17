#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tornado import ioloop, netutil, process
from tornado.httpserver import HTTPServer
from tornado.web import Application
from tornado.options import define, options
import socket
from controller.page import MainHandler, PageHandler

define('port', default=8001, help='run port', type=int)
define('debug', default=True, help='the debug mode', type=bool)
define('num_processes', default=4, help='sub-processes count', type=int)

if __name__ == '__main__':
    options.parse_command_line()
    options.debug = options.debug and options.port != 80
    handlers = [(r'/', MainHandler), (r'/(\w+)', PageHandler)]
    app = Application(handlers,
                      debug=options.debug,
                      cookie_secret='R1sl9JqfQnCOS+aAR0fPVPpw5LzQOkzKudChgWnbhKw=',
                      static_path='static',
                      template_path='views')

    server = HTTPServer(app, xheaders=True)
    sockets = netutil.bind_sockets(options.port, family=socket.AF_INET)
    fork_id = 0 if options.debug else process.fork_processes(options.num_processes)
    server.add_sockets(sockets)

    print('Start http://localhost:%d' % (options.port,))
    ioloop.IOLoop.current().start()
