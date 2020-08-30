from django.http import HttpResponse
from django.views import View
from django.views.generic.base import TemplateView
from django.conf import settings
import requests
import json
import logging
from .api_request import BaseRequest


logger = logging.getLogger(__name__)
api_url = "https://slb.medv.ru/api/v2/"


class AuthCheckTplView(TemplateView):
    """
    This class use template as output
    and BaseRequest as request engine
    """
    template_name = 'api.html'

    def get(self, request, **kwargs):
        ctx = self.get_context_data()
        api_method = "auth.check"
        api_req = BaseRequest(api_url)
        result = api_req.make_request(method=api_method)

        ctx['data'] = result
        return self.render_to_response(ctx)


def print_request(req):
    """
    just log the result of request
    :param req: requests object
    """
    print(req)
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
            stat = req.status_code

            # while request we need handle some errors
            # non 200 as 404 or 405
            if stat != 200:
                ctx = 'Request error: {}'.format(req.status_code)
                logger.error(ctx)

            # handle response errors after 200 code
            # checking for 'result' existing of not handle errors in 'error' or any others
            else:
                prepared_data = json.loads(req.content)
                if not 'result' in prepared_data.keys():
                    if prepared_data.get('error'):
                        ctx = 'Server error: {}'.format(prepared_data['error']['message'])
                        logger.error(ctx)
                    else:
                        ctx = 'Some error acquired'
                # final ready data
                else:
                    ctx = prepared_data

        # error with certificate or key file
        except requests.exceptions.SSLError as e:
            ctx = 'SSL error'
            logger.error(ctx)
        # other connection error
        except requests.exceptions.RequestException as e:
            ctx = 'Connection error. {}'.format(e)
            logger.error(ctx)

        session.close()
        return HttpResponse('<html><body><div><pre style="white-space: break-spaces">{}</pre></div></body></html>'.format(ctx))
