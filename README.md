# ftp-proxy-client ![travis](https://travis-ci.com/uptilab2/ftp-proxy-client.svg?branch=master)
An FTP client for [ftp-proxy](https://github.com/uptilab2/ftp-proxy)

## Current features:
- Test successful connection to FTP server through proxy
- List files and directories
- Download a file

## Installation
`pip install ftp-proxy-client`

## Usage
```
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
```
