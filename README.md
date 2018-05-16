# ftp-proxy-client
This module allows you to explore and download a file from a FTP via a proxy.

The ftp-proxy module is a great addition to this one.

## Usage
- Create a FtpProxy instance : ``ftp_proxy = FtpProxy(host='foo', port=0)``
- Connect to your ftp (only host is mandatory) ``ftp_client = ftp_proxy.connect(host='foo', port=0, login='foo', password='bar')``
- To explore the ftp, use the ls method (usable without params) : ``files, directories = ftp_client.ls(path='foo', recursive=False, extension='.bar')``
- To download a file, use the download method : ``fp = ftp_client.download(path='foo.bar')``
