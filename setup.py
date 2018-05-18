#!/usr/bin/env python

from distutils.core import setup

setup(name='ftp-proxy-client',
      version='1.0',
      description='Client for FtpProxy',
      author='Giovanni Dallava',
      author_email='giovanni.dallava@uptilab.com',
      url='https://github.com/uptilab2/ftp-proxy-client',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
      ],
      keywords='ftp proxy client',
      install_requires=['requests']
      extras_require={  # Optional
        'dev': ['pytest', 'flake8'],
      },
      project_urls={
        'Source': 'https://github.com/uptilab2/ftp_proxy',
      },
     )
