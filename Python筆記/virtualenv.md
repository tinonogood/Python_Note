# virtualenv

創造虛擬python環境工具,隔離各專案,使其可用不同套件不互衝突。

### Install

pip3 install virtualenv

### Usage

`virtualenv venv`: 創造venv目錄,其下有bin,include,lib資料夾並安裝好python,pip

`cd venv`

`source bin/activate`: 啟動當前virtualenv

`deactivate`: 關閉

‵virtualenv -p /usr/local/bin/python3.5 venv`: 指定版本"-p python"

`virtualenv -h`: help文件


# conda 

`conda -V`: 檢查conda版號,並確認是否安裝

`conda update conda`

`conda search "^python$"`:python版號


`conda create -n yourenvname python=x.x anaconda`:創新環境具備python ＆ anaconda

`source activate yourenvname`

`conda info -e`:列出所有虛擬環境

`conda install -n yourenvname [package]`:新增package至環境

`source deactivate`

`conda remove -n yourenvname --all`:刪除環境
