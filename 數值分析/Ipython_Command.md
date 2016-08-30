- `#ipython --pylab`

啟動IPython於pylab模式(自動導入Scipy,Numpy,Matplotlib)

- `%run` 執行python code

  `-i`: 指定當前資料夾之 python code
  
  `-d`: debug
  
  `-p`: 性能分析
  
- `%hist` 命令歷史紀錄


## 錯誤

  `In [3]: a = arange(5)`
  `---------------------------------------------------------------------------`
  `NameError                                 Traceback (most recent call last)`
  `<ipython-input-3-1dd9434971cc> in <module>()`
  `----> 1 a = arange(5)`

  `NameError: name 'arange' is not defined`

