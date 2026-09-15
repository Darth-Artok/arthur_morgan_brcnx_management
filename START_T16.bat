@echo off
cd /d "%~dp0"
where py >nul 2>&1 && py ambm_t16.py init || python ambm_t16.py init
pause
