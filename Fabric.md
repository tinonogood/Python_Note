# Install

pip3.5 install fabric

`fab -H {ip_address} host_type`


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
   
