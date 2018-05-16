import requests
from io import BytesIO

class FtpProxyError(Exception):
    def __init__(self, message, errors):
        super().__init__(message)
        self.errors = errors


class FtpProxy():
    def __init__(self, host, port):
        self.proxy_host = host
        self.proxy_port = port

    def connect(self, host, port=None, login=None, password=None):
        if not host:
            raise FtpProxyError('A host is required')
        elif host.startswith('ftp://'):
            host = host[6:]
        if not self.proxy_host.startswith('http://'):
            self.proxy_host = f'http://{self.proxy_host}'
        if self.proxy_port:
            self.proxy_host += f":{self.proxy_port}"
        client = Client(self.proxy_host, host, port, login, password)
        client.ping()
        return client


class Client():
    def __init__(self, proxy_host, host, port, login, password):
        self.proxy_host = proxy_host
        self.session = requests.Session()
        self.session.headers['X-ftpproxy-host'] = host
        if port:
            self.session.headers['X-ftpproxy-port'] = str(port)
        if login:
            self.session.headers['X-ftpproxy-user'] = login
        if password:
            self.session.headers['X-ftpproxy-password'] = password

    def query(self, url, params=None):
        try:
            url = self.proxy_host + url
            response = self.session.get(url, params=params)
            if response.status_code == 400:
                raise FtpProxyError(response.json()['error'])
            return response
        except ConnectionError:
            raise FtpProxyError('Error connecting to the proxy')

    def ping(self):
        try:
            self.query('/ftp/ping')
            return True
        except FtpProxyError:
            return False

    def ls(self, path=None, recursive=False, extension=None):
        params={'recursive': 'false'}
        if recursive:
            params={'recursive': 'true'}
        if path:
            params['path'] = path
        if extension:
            params['extension'] = extension
        try:
            result = self.query('/ftp/ls', params).json()
            return result.get('files', []), result.get('directories', [])
        except:
            raise FtpProxyError('Bad response from proxy')


    def download(self, path=None):
        params=None
        if path:
            params = {'path': path}
        try:
            return BytesIO(self.query('/ftp/download', params).content)
        except:
            raise FtpProxyError('Bad response from proxy')

