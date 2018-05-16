# ftp-proxy-client
This module allows you to explore and download a file from a FTP via a proxy.

The ftp-proxy module is a great addition to this one.

## Setup
- run ``pip install ftp-proxy-client``
- on your python script, ``import FtpProxy``

## Usage
Here is an example of usage that covers all the methods available:
``
if __name__ == '__main__':
    ftp_proxy = FtpProxy(host='foo', port=8080)
    ftp_client = ftp_proxy.connect('192.168.0.1', port=8080, login='foobar')

    assert ftp_client.ping() is True
    files, directories = ftp_client.ls()
    assert files and directories

    files2, directories = ftp_client.ls(recursive=True)
    assert len(files2) > len(files)

    files3, directories = ftp_client.ls(recursive=True, extension='.txt')
    assert not directories
    assert files3[0].endswith('.txt')

    fp = ftp_client.download(path='/foo.txt')
    with open('/tmp/foo.txt', 'wb') as ff:
        ff.write(fp.read())
    assert fp.tell() > 0
``
