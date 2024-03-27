@echo off

setlocal enabledelayedexpansion

REM Default values
set "flavor=release"
set "commit=5"
set "app=customer"

REM Parse command line arguments
:parse_args
if "%~1" == "" goto end

if "%~1" == "--flavor" (
    set "flavor=%~2"
    shift
) else if "%~1" == "-f" (
    set "flavor=%~2"
    shift
) else if "%~1" == "--commit" (
    set "commit=%~2"
    shift
) else if "%~1" == "-c" (
    set "commit=%~2"
    shift
) else if "%~1" == "--app" (
    set "app=%~2"
    shift
) else (
    echo Unknown option: %~1
)

shift
goto parse_args

:end

@REM REM Print parsed arguments
@REM echo Flavor: %flavor%
@REM echo Commit: %commit%
@REM echo App: %app%

rem Set the first command with or without flavor
if "%flavor%"=="release" (
    set "command1=fvm flutter build apk --release"
) else (
    set "command1=fvm flutter build apk --release --flavor %flavor% -t "lib/main_%flavor%.dart""
)

rem Set the second command with or without flavor
if "%flavor%"=="release" (
    set "command2=python %APK2DISCORD% -n app-release -c %commit% --app %app%"
) else (
    set "command2=python %APK2DISCORD% -n app-%flavor%-release -c %commit% --app %app%"
)

call %command1%
call %command2%

endlocal
