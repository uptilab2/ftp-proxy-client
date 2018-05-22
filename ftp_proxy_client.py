
import requests
from io import BytesIO


class FtpProxyError(Exception):
    pass


class FtpProxy():
    def __init__(self, host, port=2121):
        split_host = host.rsplit(':', 1)
        if len(split_host) > 1 and split_host[1].isdigit():
            host, port = split_host
        protocol = '' if '://' in host else 'http://'
        self.proxy_host = f'{protocol}{host}:{port}'

    def connect(self, host, port=None, login=None, password=None, protocol='ftp'):
        if host.startswith('ftp://'):
            host = host[6:]

        if protocol == 'ftp':
            return FtpClient(self.proxy_host, host, port, login, password)
        elif protocol == 'sftp':
            return SftpClient(self.proxy_host, host, port, login, password)

        raise FtpProxyError(f'Protocol is not (yet) supported: "{protocol}"')


class BaseClient():
    def __init__(self, proxy_host, host, port, login, password):
        self.proxy_host = proxy_host
        self.session = requests.Session()
        headers = self.build_headers(host, port, login, password)
        self.session.headers.update(headers)

    def build_headers(self, host, port, login, password):
        if host is None:
            split_host = host.rsplit(':', 1)
            if len(split_host) > 1 and split_host[1].isdigit():
                host, port = split_host

        headers = {'X-ftpproxy-host': host}
        if port:
            headers['X-ftpproxy-port'] = str(port)
        if login:
            headers['X-ftpproxy-user'] = login
        if password:
            headers['X-ftpproxy-password'] = password
        return headers

    def query(self, url, **kwargs):
        url = f'{self.proxy_host}{self.protocol_prefix}{url}'
        try:
            response = self.session.get(url, **kwargs)
        except requests.RequestException:
            raise FtpProxyError('Failed connecting to proxy server')

        if response.status_code == 400:
            message = response.json()['error']
            raise FtpProxyError(message)

        return response


class FtpClient(BaseClient):
    protocol_prefix = '/ftp'

    def ping(self):
        """Check connection to remote FTP server

        :return: Success status
        :rtype: bool

        Usage::

          >>> from ftp_proxy_client import FtpProxy
          >>> client = FtpProxy(host='my-proxy-server').connect(host='my-ftp-server')
          >>> client.ping()
          True
        """

        try:
            response = self.query('/ping')
            return response.status_code == 200
        except FtpProxyError:
            return False

    def ls(self, path=None, recursive=False, extension=None):
        """List files and repositories on ftp server

        :param path: (optional) path to list
        :type path: str
        :param recursive: (optional) recurse down directories when listing
        :type path: bool
        :param extension: (optional) filter files by extension
        :type path: str

        :return: files, directories
        :rtype: tuple

        Usage::

          >>> from ftp_proxy_client import FtpProxy
          >>> client = FtpProxy(host='my-proxy-server').connect(host='my-ftp-server')
          >>> client.ls()
          (['/foo.py', 'bar/bar.py'], ['/bar'])
        """
        params = {'recursive': 'true' if recursive else 'false'}
        if path:
            params['path'] = path
        if extension:
            params['extension'] = extension
        response = self.query('/ls', params=params)
        return response.json()

    def download(self, path):
        """Retrieve a file from FTP server

        :param path: path of file to download
        :type path: str

        :return: the requested file
        :rtype: BytesIO instance

        Usage::

          >>> from ftp_proxy_client import FtpProxy
          >>> client = FtpProxy(host='my-proxy-server').connect(host='my-ftp-server')
          >>> client.download('foo.py')
          <_io.BytesIO at 0x10b8b8308>
          >>> _.read()
          b'print("foo")'
        """
        response = self.query('/download', params={'path': path}, stream=True)
        buf = BytesIO()
        for chunk in response.iter_content():
            buf.write(chunk)
        return buf


class SftpClient(FtpClient):
    protocol_prefix = '/sftp'

    def ls(self, path=None, extension=None):
        """Override to disable recursive parameter"""
        return super().ls(path=path, extension=extension)
