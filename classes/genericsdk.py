import requests
import json
from classes import exceptions
from urllib.parse import urljoin


class genericSDK(object):
    def __init__(self, url='http://localhost:port', token=None, session=None, engine=None):
        self._url = url
        self.token = token  # TODO Fetch from file if None (not passed in from args)
        self.engine = engine

        if not session:
            session = requests.Session()
        self.session = session

    def abstract_funcname(self, parameter_list):
        raise NotImplementedError

    def funcname(self, parameter_list):
        pass

    # TODO they may want bumpers for time constraints
    def post_sample(self, cert, ca_type='exported'):
        """ POST /v1/pki/root/generate/:ca_type """
        url = '/v1/{0}/root/generate/{1}'.format(self.engine, ca_type)

        params = json.loads(json.dumps(cert.__dict__))
        return self._post(url, json=params).json()

    def get_sample(self, serial):
        """ GET /v1/pki/cert/:serial """
        url = '/v1/{0}/cert/{1}'.format(self.engine, serial)
        return self._get(url).json()

    def close(self):
        self.session.close()

    """ NETWORK HANDLERS """

    def _get(self, url, **kwargs):
        return self.__request('get', url, **kwargs)

    def _post(self, url, **kwargs):
        return self.__request('post', url, **kwargs)

    def _put(self, url, **kwargs):
        return self.__request('put', url, **kwargs)

    def _delete(self, url, **kwargs):
        return self.__request('delete', url, **kwargs)

    def _list(self, url, **kwargs):
        return self.__request('list', url, **kwargs)

    def __request(self, method, url, header=None, **kwargs):
        url = urljoin(self._url, url)

        if not header:
            header = {}

        # if self.token:
        #     #header[X-Thing-Token'] = self.token

        # wrap_ttl = kwargs.pop('wrap_ttl', None)  # TODO Examine if this is required
        # if wrap_ttl:
        #     header['X-Thing-Wrap-TTL'] = str(wrap_ttl)

        response = self.session.request(method, url, headers=header, allow_redirects=False, **kwargs)

        # NOTE CURRENTLY EMPTY RESPONSES DO NOT RETURN JSON, SO I AM GENERATING IT INSTEAD FOR UNIFORMITY
        # if str(response) == '<Response [204]>':
        #     response = requests.Response()
        #     response.status_code = 204

        # if 400 <= response.status_code < 600:
        #     text = errors = None
        #     if response.headers.get('Content-Type') == 'application/json':
        #         errors = response.json().get('errors')
        #     if errors is None:
        #         text = response.text
        #     self.__raise_error(response.status_code, text, errors=errors)

        return response

    def __raise_error(self, status_code, message=None, errors=None):
        if status_code == 400:
            raise exceptions.InvalidRequest(message, errors=errors)
        elif status_code == 401:
            raise exceptions.Unauthorized(message, errors=errors)
        elif status_code == 403:
            raise exceptions.Forbidden(message, errors=errors)
        elif status_code == 404:
            raise exceptions.InvalidPath(message, errors=errors)
        elif status_code == 429:
            raise exceptions.RateLimitExceeded(message, errors=errors)
        elif status_code == 500:
            raise exceptions.InternalServerError(message, errors=errors)
        else:
            raise exceptions.UnexpectedError(message)

    @staticmethod
    def static_funcname(parameter_list):
        pass
