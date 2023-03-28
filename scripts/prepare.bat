@echo off
setlocal
cd %~dp0\..
if exist %cd%\algolibraries (
    call :info "It exists!"
)
call :exit
exit /B %errorlevel%

:info
echo [*] %~1
exit /B 0

:exit
call :info "All done!"
exit /B 0