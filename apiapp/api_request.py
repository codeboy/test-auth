from django.conf import settings
import requests
import json
import logging

logger = logging.getLogger(__name__)

class BaseRequest:
    """
    Base class for making request
    """
    def __init__(self, api_url, logging=True):
        self.api_url = api_url
        self.logging = logging
        self.cert = settings.CERTIFICATE_FILE
        self.key = settings.KEY_FILE
        self.__start_session()

    def __start_session(self):
        """
        start requests session and add auth params and headers
        """
        self.session = requests.Session()
        self.session.cert = self.cert, self.key
        self.session.headers = {'Content-Type': 'application/json'}

    def __del__(self):
        self.session.close()

    def make_request(self, method, rid=0, params={}):
        """
        send request to server and processes the response
        :param method: api method
        :param rid: request id
        :param params: optional parameters
        :return str: final text of result
        """
        ctx = 'No data'
        send_data = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params,
            "id": rid
        }

        try:
            req = self.session.post(self.api_url, data=json.dumps(send_data))
            stat = req.status_code

            # while request we need handle some errors
            # non 200 as 404 or 405
            if stat != 200:
                ctx = 'Request error: {}'.format(req.status_code)
                self.__make_log(ctx)

            # handle response errors after 200 code
            # checking for 'result' existing of not handle errors in 'error' or any others
            else:
                prepared_data = json.loads(req.content)
                if not 'result' in prepared_data.keys():
                    if prepared_data.get('error'):
                        ctx = 'Server error: {}'.format(prepared_data['error']['message'])
                        self.__make_log(ctx)
                    else:
                        ctx = 'Some error acquired'
                # final ready data
                else:
                    ctx = prepared_data

        # error with certificate or key file
        except requests.exceptions.SSLError as e:
            ctx = 'SSL error'
            self.__make_log(ctx)
        # other connection error
        except requests.exceptions.RequestException as e:
            ctx = 'Connection error. {}'.format(e)
            self.__make_log(ctx)
        return  ctx

    def __make_log(self, msg):
        """
        create log entry
        :param msg:
        """
        if self.logging:
            logger.error(msg)