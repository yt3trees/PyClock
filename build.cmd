rem upx --upx-dir C:\upx-3.96-win64
rem --icon=icon/copytool.ico
pyinstaller PyClock.py --name PyClock --noconsole
rem --icon=icon/PyClock_LightIcon.ico

if exist .\app\PyClock\PyClock.exe (
    echo 上書きします。
    echo A | xcopy .\dist .\app /S
) else (
    echo 新規でコピーします。
    echo D | xcopy .\dist .\app /S
)
pause