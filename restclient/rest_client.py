import json
import curlify
import requests
import structlog
import uuid


class RestClient:
    def __init__(self, host, headers):
        self.host = host
        self.session = requests.session()
        self.session.headers = headers
        self.log = structlog.get_logger(self.__class__.__name__).bind(service='api')

    def post(self, path, **kwargs):
        """
        Create data
        :param path:
        :param kwargs:
        :return:
        """
        response = self._send_request('POST', path, **kwargs)
        return response

    def get(self, path, params=None, **kwargs):
        """
        Get data
        :param path:
        :param kwargs:
        :return:
        """
        response = self._send_request(method='GET', path=path, params=params, **kwargs)
        return response

    def put(self, path, **kwargs):
        """
        Update data
        :param path:
        :param kwargs:
        :return:
        """
        response = self._send_request(method='PUT', path=path, **kwargs)
        return response

    def delete(self, path, **kwargs):
        """
        Remove data
        :param path:
        :param kwargs:
        :return:
        """
        response = self._send_request(method='DELETE', path=path, **kwargs)
        return response

    def patch(self, path, **kwargs):
        """
        Patch data
        :param path:
        :param kwargs:
        :return:
        """
        response = self._send_request(method='PATCH', path=path, **kwargs)
        return response

    def _send_request(self, method, path, **kwargs):
        """
        Sends request and logs data
        :param method:
        :param path:
        :param kwargs:
        :return:
        """
        full_url = self.host + path
        log = self.log.bind(event_id=str(uuid.uuid4()))
        log.msg(
            event='request',
            method=full_url,
            params=kwargs.get('params'),
            headers=kwargs.get('headers', self.session.headers),
            json=kwargs.get('json'),
            data=kwargs.get('data'),
        )
        response = self.session.request(
            method=method,
            url=full_url,
            **kwargs
        )
        curl = curlify.to_curl(response.request)
        print(curl)
        log.msg(
            event='response',
            status_code=response.status_code,
            headers=response.headers,
            json=self._get_json(response),
            text=response.text,
            content=response.content,
            curl=curlify.to_curl(response.request),
        )
        return response

    @staticmethod
    def _get_json(response):
        """
        Get json from request
        :param response:
        :return:
        """
        try:
            return response.json()
        except json.JSONDecodeError:
            return
