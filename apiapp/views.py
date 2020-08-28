from django.http import HttpResponse
from django.views import View
from django.conf import settings
import requests
import json


api_url = "https://slb.medv.ru/api/v2/"

def print_request(req):
    """
    just log the result of request
    :param req: request object
    """
    print(dir(req))
    for i in ['headers', 'content', 'reason', 'links']:
        print(getattr(req, i))
    print(req.request.body)


class AuthCheckView(View):
    def get(self, request, **kwargs):
        ctx = 'Nothing to show.' # context will be show in html markup
        rid = int(kwargs['rid']) if kwargs.get('rid') else 0 # request id for an additional request param
        url = api_url
        cert = settings.CERTIFICATE_FILE
        key = settings.KEY_FILE

        session = requests.Session()
        session.cert = cert, key
        session.headers = {'Content-Type': 'application/json'}
        send_data = {
            "jsonrpc": "2.0",
            "method": "auth.check",
            "params": {},
            "id": rid
        }

        try:
            req = session.post(url, data=json.dumps(send_data))
            # print_request(req) # just print result of request
            stat = req.status_code

            # while request we need handle some errors
            # non 200 as 404 or 405
            if stat != 200:
                ctx = 'Request error: {}'.format(req.status_code)

            # handle response errors after 200 code
            # checking for 'result' existing of not handle errors in 'error' or any others
            else:
                prepared_data = json.loads(req.content)
                if not 'result' in prepared_data.keys():
                    if prepared_data.get('error'):
                        ctx = 'Server error: {}'.format(prepared_data['error']['message'])
                    else:
                        ctx = 'Some error acquired'
                else:
                    ctx = prepared_data

        # error with certificate or key file
        except requests.exceptions.SSLError as e:
            ctx = 'SSL error'
        # other connection error
        except requests.exceptions.RequestException as e:
            ctx = 'Connection error. {}'.format(e)

        session.close()
        return HttpResponse('<html><body><div><pre style="white-space: break-spaces">{}</pre></div></body></html>'.format(ctx))
