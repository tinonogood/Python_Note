## Get Numpy

[Numpy's Github](https://github.com/numpy/numpy "https://github.com/numpy/numpy")

`git clone git://github.com/numpy/numpy.git numpy`

至numpy資料夾

`/usr/local/python3/bin/pip3.5 install numpy`

## Get Scipy

[Scipy's Github](https://github.com/scipy/scipy)

`/usr/local/python3/bin/pip3.5 install scipy`


安裝套件在 /usr/local/python3/lib/python3.5/site-packages/

### 錯誤

- Error Message: ImportError: No module named 'Cython'

以python setup.py build安裝失敗

改用pip3.5 install numpy

- `"ImportError: Need nose >= 1.0.0 for tests - see http://somethingaboutorange.com/mrl/projects/nose" `

安裝nose

- `“ImportError: No module named scipy” `

因用pip3.5 Install, 需改以用python3.5執行即可import

- `ERROR: test_common.test_face`

  `File "/usr/local/python3/lib/python3.5/site-packages/nose/case.py", line 198, in runTest self.test(*self.arg)`
  `File "/usr/local/python3/lib/python3.5/site-packages/scipy/misc/tests/test_common.py", line 168, in test_face assert_equal(face().shape, (768, 1024, 3))`
  `File "/usr/local/python3/lib/python3.5/site-packages/scipy/misc/common.py", line 410, in face import bz2`
  `File "/usr/local/python3/lib/python3.5/bz2.py", line 22, in <module> from _bz2 import BZ2Compressor, BZ2Decompressor`
  `ImportError: No module named '_bz2'`


