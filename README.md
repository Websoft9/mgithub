# 说明

本项目是用于批量更新Github项目以及项目元数据的CLI程序，适用于一个组织下有多个项目，且项目在不断迭代过程中可能产生一致性**批量**维护的需求。  

本项目处于详细设计和开发中，计划使用 Python 开发。

项目计划分为三个阶段：

**第一阶段**： 完成CLI框架以及两个Command范例  
**第二阶段**： 完成所有计划的Command  
**第三阶段**： 完成体验优化，形成 Alpha 版本  

对于参与本项目第一阶段的贡献者，将以核心成员身份承担本开源项目的战略规划和发展。

希望有兴趣的伙伴多多参与。

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

# Quickstart
###Pre-request
You need to have python3 and pip3 installed on your own device.
###Install
1. Fork/Download the repository from [Mgithub](https://github.com/Websoft9/mgithub).
2. Install mgithub command through pip3.
```
    $ pip3 install --editable .
```
3. Run mgithub command then you should find the help information in your terminal window.
```buildoutcfg
    $ mgithub
```
###Uninstall
1. Use pip3 to uninstall the mgithub package.
```buildoutcfg
    $ pip3 uninstall mgithub
```

# User Guide
##mgithub
####Help information
You can find the help information by either typing mgithub or mgithub -h.
```buildoutcfg
    $ mgithub
    $ mgithub -h
```
####Check the version
You can check the version of mgithub by -v option.
```buildoutcfg
    $ mgithub -v
```
####Check the log
You can find the latest 10 logs by -l or --logs options.
```buildoutcfg
    $ mgithub -l
    $ mgithub --logs
```


