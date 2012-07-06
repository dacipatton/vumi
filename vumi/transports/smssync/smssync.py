# -*- test-case-name: vumi.transports.httprpc.tests.test_httprpc -*-

import json

from twisted.internet.defer import inlineCallbacks
from twisted.python import log
from twisted.web import http
from twisted.web.resource import Resource

from vumi.transports.base import Transport


class SmsSyncHealthResource(Resource):
    isLeaf = True

    def render(self, request):
        request.setResponseCode(http.OK)
        request.do_not_log = True
        return 'OK'


class SmsSyncResource(Resource):
    isLeaf = True

    def __init__(self, transport):
        self.transport = transport
        Resource.__init__(self)

    def render(self, request):
        return 'pew'


class SmsSyncTransport(Transport):

    def validate_config(self):
        self.web_path = self.config['web_path']
        self.web_port = int(self.config['web_port'])
        self.secret = self.config.get('secret', '')

    @inlineCallbacks
    def setup_transport(self):
        self.web_resource = yield self.start_web_resources(
            [
                (SmsSyncResource(self), self.web_path),
                (SmsSyncHealthResource(), 'health')
            ], self.web_port
        )
