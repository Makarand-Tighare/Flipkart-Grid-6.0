@echo off
for /f "tokens=*" %%i in ('findstr /v "^#" ..\.env') do set %%i
npx nodemon --watch pages --watch components --exec "npx next dev"
