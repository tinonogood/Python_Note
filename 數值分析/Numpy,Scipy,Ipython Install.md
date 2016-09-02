## Get Numpy

[Numpy's Github](https://github.com/numpy/numpy "https://github.com/numpy/numpy")

develop repo.

`git clone git://github.com/numpy/numpy.git numpy`

or 以pip安裝

`/usr/local/python3/bin/pip3.5 install numpy`

## Get Scipy

[Scipy's Github](https://github.com/scipy/scipy)

以pip安裝

`/usr/local/python3/bin/pip3.5 install scipy`

## Ipython

以pip安裝

`#pip3.5 ipython`


安裝套件在 /usr/local/python3/lib/python3.5/site-packages/

### 錯誤

- Error Message: ImportError: No module named 'Cython'

以python setup.py build安裝失敗

改用pip3.5 install numpy

- `"ImportError: Need nose >= 1.0.0 for tests - see http://somethingaboutorange.com/mrl/projects/nose" `

安裝nose

- `“ImportError: No module named scipy” `

因用pip3.5 Install, 需改以用python3.5執行即可import

- 執行Ipython3出錯: `importerror no module named 'readline'`

  檢查ncurses-devel, 安裝readline:`pip3 install readline`
  
- 執行Ipython3 --pylab 出錯:`ImportError: No module named '_tkinter'`

- `ERROR: test_common.test_face`

  `File "/usr/local/python3/lib/python3.5/site-packages/nose/case.py", line 198, in runTest self.test(*self.arg)`
  `File "/usr/local/python3/lib/python3.5/site-packages/scipy/misc/tests/test_common.py", line 168, in test_face assert_equal(face().shape, (768, 1024, 3))`
  `File "/usr/local/python3/lib/python3.5/site-packages/scipy/misc/common.py", line 410, in face import bz2`
  `File "/usr/local/python3/lib/python3.5/bz2.py", line 22, in <module> from _bz2 import BZ2Compressor, BZ2Decompressor`
  `ImportError: No module named '_bz2'`


