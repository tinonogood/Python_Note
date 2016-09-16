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
