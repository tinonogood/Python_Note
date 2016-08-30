# Install

安裝完python-setuptools, pip2.6後

pip2.6 install fabric

安裝後fab指令位於/usr/local/bin

`fab -f {file_name} -H {ip_address} host_type`

file_name: fabfile.py


# 錯誤

- ImportError: cannot import name 'isMappingType'

  輸入: `fab -H {ip_address} host_type`
  
  Traceback (most recent call last):
  File "/usr/local/python3/bin/fab", line 9, in <module>
    load_entry_point('Fabric==1.12.0', 'console_scripts', 'fab')()
  File "/usr/local/python3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 542, in load_entry_point
    return get_distribution(dist).load_entry_point(group, name)
  File "/usr/local/python3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 2569, in load_entry_point
    return ep.load()
  File "/usr/local/python3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 2229, in load
    return self.resolve()
  File "/usr/local/python3/lib/python3.5/site-packages/pkg_resources/__init__.py", line 2235, in resolve
    module = __import__(self.module_name, fromlist=['__name__'], level=0)
  File "/usr/local/python3/lib/python3.5/site-packages/fabric/main.py", line 13, in <module>
    from operator import isMappingType
  ImportError: cannot import name 'isMappingType'
  
  解:
  
   因'operator.isMappingType'為 standard library for Python 2.x, 不存在於python3
   
   改以python2安裝
   
   `#zypper se setuptools `        #安裝python-setuptools, 然後easy_install pip2.6
   
   `#zypper in python-setuptools`
   
   `#easy_install-2.6 pip`
   
   `#pip2.6 install fabric`
   
   Successfully installed ecdsa-0.13 fabric-1.12.0 paramiko-1.17.2 pycrypto-2.6.1
/usr/local/lib64/python2.6/site-packages/pip-8.1.2-py2.6.egg/pip/_vendor/requests/packages/urllib3/util/ssl_.py:122: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. You can upgrade to a newer version of Python to solve this. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
  InsecurePlatformWarning
  
- SyntaxError: Non-ASCII character '\xe5' in file

  因註解有中文,於code中加入` -*- coding: UTF-8 -*- ‵
   
