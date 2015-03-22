#!/bin/bash

function check_process {
    mode=$1
    if [ "$mode" = "pname" ]; then
        process=`pgrep -f $2`
        echo $process
        if [ -z "$process" ]; then
            return 1
        else
            return 0
        fi
    elif [ -f $2 ]; then
        pid=`cat $2`
        pid_exist=`ps --no-heading -p $pid`
        echo $pid_exist
        if [ -z "$pid_exist" ]; then
            return 1
        else
            return 0
        fi
    else
        return 1
    fi
}

function check_dep_tcp {
    host=$1
    port=$2
    nc -z -w3 $host $port
    return $?
}

function check_dep_http {
    url=$1
    ret_code=`curl -L -s -o /dev/null -w "%{http_code}" $url`
    if [ $ret_code -gt 299 ] || [ $ret_code -lt 200 ]; then
        return 1
    else
        return 0
    fi
}
