# Introduction
## What is mgithub
Mgithub is a CLI tool to update batch Github repositories and meta data.<br>
Mgithub is suitable for:
1. An organization which has multiple repositories.
2. There is a need for consistent batch maintenance appears during the iteration of the project.

## Help make this documentation better...
if you find this documentation lacking in any way or missing documentation for a feature, then the best things to do
is learn about it and then write the documentation yourself ! 
Sources of this manual are available at [Mgithub](https://github.com/Websoft9/mgithub). Fork the repository, update them
and send a pull request.

## Three main steps of project development
**Step 1**: Finish CLI framework and two command example.<br>
**Step 2**: Finish all planned command. <br>
**Step 3**: Improve the user experience and optimization, build Alpha version.<br>

# Quickstart
### Pre-request
You need to have python3 and pip3 installed on your own device.
### Install
1. Fork/Download the repository from [Mgithub](https://github.com/Websoft9/mgithub).
2. Install mgithub command through pip3.
    ```
    $ pip3 install --editable .
    ```
3. Run mgithub command then you should find the help information in your terminal window.
    ```
    $ mgithub
    ```
4. Use mgithub config to set your Github's url
    ```buildoutcfg
    $ mgithub configre
    input URL: https://github.com/XXXX
    Set new URL successfully
    ```
5. Manipulate the checklist to decide the repositories you are going to make operation on it.
    ```buildoutcfg
    $ vim data/XXXX_repositories.txt
    Custom the list of repositories by manipulating this checklist file
    ```
6. Use command to make operation on your repositories
    ```buildoutcfg
    $ mgithub copy copysrc/text.txt /test/
    ```
### Uninstall
1. Use pip3 to uninstall the mgithub package.
    ```
    $ pip3 uninstall mgithub
    ```

# User Guide
## mgithub
#### Help information
You can find the help information by either typing mgithub or mgithub -h.
```
$ mgithub
$ mgithub -h
```
#### Check the version
You can check the version of mgithub by -v option.
```
$ mgithub -v
```
#### Check the log
You can find the latest 10 logs by -l or --logs options.
```
$ mgithub -l
$ mgithub --logs
```

## Main command option
#### --skip-get-repositories
User can use this option to skip the step of cloning repositories from Github. 
However, the repositories in user's checklist are still going to be re-checked or pulled before you make any operation with it.
```buildoutcfg
mgithub --skip-get-repositories copy copysrc/test.txt /test/
```
#### --skip-broken
User can use this option to skip the broken operation with certain repository and jump to the next repository automatically.
Without this option, any exception appears during the process of operation will stop the mgithub command.
```buildoutcfg
mgithub --skip-broken copy copysrc/test.txt /test/
```
#### -f, --force
Force the operation without the prompt. <br>
e.g. If there is already a test.txt file under /test/, this copy will overwrite this file without asking user.
```buildoutcfg
mgithub -f copy copysrc/test.txt /test/
```

## System command
#### configure
User should use this command to configure the user/organization's Github url before running any command at the first time.
```buildoutcfg
$ mgithub configre
input URL: https://github.com/XXXX
Set new URL successfully
```
#### repocache
User can use this command to pull the list of repositories under user/organization which has been configured before.
```buildoutcfg
$ mgithub repocache
开始更新XXXX Github仓库列表...

projA
projB
projC
```

## Product command
#### copy
Copy files or folder from source path to destination path.<br>
1. Command usage: mgithub copy [OPTIONS] SOURCE_PATH DESTINATION_PATH<br>
2. SOURCE_PATH: the path of source file on your local computer, you can put the file into mgithub/copysrc folder or just use the absolue path of file.<br>
3. DESTINATION_PATH: the destination location of repository where you want paste the file.<br>

e.g. copy test.txt file under mgithub/copysrc to /test/ path of repository.
```buildoutcfg
$ mgithub copy copysrc/test.txt /test/
```
e.g. copy test.txt file with absolute path of your computer to /test/ path of repository.
```buildoutcfg
$ mgithub copy ~/desktop/test.txt /test/
```
e.g. copy test.txt file with force overwriting
```buildoutcfg
$ mgithub -f copy copysrc/test.txt /test/
```

#### githubcli
Execute official Github's CLI command.<br>
1. Command usage: mgithub githubcli [OPTIONS] 'CLISTRING'<br>
2. CLISTRING: some of the available official gh command<br>

**e.g. create new secret**<br>
The official command to create new secret with gh command is:
```buildoutcfg
gh secret set -R"XXXX/projectA" SECRET_1 -b"abcdefg"
```
With mgithub githubcli, there is no need to use -R option to confirm the name of repository:
```buildoutcfg
mgithub githubcli 'gh secret set SECRET_1 -b"abcdefg"'
```
This mgithub script will create a secret named SECRET_1 whose value is abcdefg to every repositories under the checklist.<br>
If there is -f option, mgithub will forced overwrite the same name secret, and vice versa.

**e.g. delete existed secret**<br>
The official command to delete existed secret with gh command is:
```buildoutcfg
gh secret remove -R"XXXX/projectA" SECRET_1
```
With mgithub githubcli, there is no need to use -R option to confirm the name of repository:
```buildoutcfg
mgithub githubcli 'gh secret remove SECRET_1'
```
This mgithub script will delete every secret called SECRET_1 of every repositories under the checklist.<br>
If not found, mgithub will throw a exception and stop the command. User can use --skip-broken option to skip the 
abnormal repository.
