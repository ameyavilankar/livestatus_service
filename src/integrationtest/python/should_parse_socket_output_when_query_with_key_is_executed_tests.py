'''
The MIT License (MIT)

Copyright (c) 2013 ImmobilienScout24

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import unittest

try:
    from urllib2 import urlopen
except:
    from urllib.request import urlopen

from mock import patch, PropertyMock
import simplejson as json

from liveserver import LiveServer
from livesocket import LiveSocket

expected_api_call_response = {
    u'devica01': {
        u'notifications_enabled': 1,
        u'host_name': 'devica01'
    },
    u'tuvdbs06': {
        u'notifications_enabled': 1,
        u'host_name': 'tuvdbs06'
    },
    u'tuvdbs05': {
        u'notifications_enabled': 1,
        u'host_name': 'tuvdbs05'
    }
}


class Test(unittest.TestCase):
    @patch('livestatus_service.dispatcher.get_current_configuration')
    def test(self, get_config):
        mock_configuration = PropertyMock()
        mock_configuration.livestatus_socket = './livestatus_socket'
        get_config.return_value = mock_configuration
        with LiveServer() as liveserver:
            socket_response = '[["host_name","notifications_enabled"],["devica01", 1], ["tuvdbs05",1], ["tuvdbs06",1]]'
            with LiveSocket('./livestatus_socket', socket_response) as livesocket:
                api_call_result = urlopen('{0}query?q=GET%20hosts&key=host_name'.format(liveserver.url))
                actual_api_response = json.loads(api_call_result.read().decode('utf-8'))
                self.assertEqual(expected_api_call_response, actual_api_response)
                written_to_socket = livesocket.incoming.get()
                self.assertTrue('GET hosts' in written_to_socket and 'OutputFormat: json' in written_to_socket)


if __name__ == '__main__':
    unittest.main()
