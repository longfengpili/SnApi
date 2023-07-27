# @Author: longfengpili
# @Date:   2023-07-27 10:36:03
# @Last Modified by:   longfengpili
# @Last Modified time: 2023-07-27 11:01:21

getos=`uname -s`
# 判断那系统和python地址
if [[ $getos =~ 'Darwin' ]];then
    # Mac系统
    sysOS='Mac'
    pyVer='python'
elif [[ $getos =~ 'Linux' ]];then
    cd /workspace
    sysOS='Linux'
    pyVer='/usr/bin/python3'
else
    sysOS='Windows'
    pyVer='python'
fi

logInfo() {
    lineno=$1
    message=$2
    now=`date '+%s'`
    logbase="$(date '+%Y-%m-%d %H:%M:%S').$(date "+%N") - main - bash - INFO - $FILENAME - $lineno - $APPNAME"
    echo "$logbase-all-bash, 【$now】$message !!!"
}


logInfo $LINENO "Current system is $sysOS【$getos】【$PWD】"
$pyVer main.py
logInfo $LINENO "Job stop"
