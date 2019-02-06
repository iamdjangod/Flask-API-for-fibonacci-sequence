#!/bin/bash

set -o nounset

readonly SELF_DIR=$(cd $(dirname $0) && pwd)
readonly SERVER_PORT=${SERVER_PORT:-60888}
readonly SERVER_CMD_LINE="$SELF_DIR/fibonacci_server.py --port $SERVER_PORT"
readonly SERVER_URL="http://localhost:${SERVER_PORT}"

# Test functions, name must starts with 'test_'
#
function test_process
{
    pgrep -lf "$SERVER_CMD_LINE"
}


function test_fib_not_a_number
{
    check_call "/fib/0/xxx" 400 "[]"
}

function test_fib_float_number
{
    check_call "/fib/0/1.0" 400 "[]"
}

function test_fib_negative_numer
{
    check_call "/fib/0/-1" 400 "[]"
}

function test_fib_overflowed_number
{
    check_call "/fib/0/99999999999999" 413 "[]"
}

function test_fib_zero
{
    check_call "/fib/0/0" 200 "[]"
}

function test_fib_minimal
{
    check_call "/fib/0/2" 200 "[0, 1]"
}

function test_fib_normal
{
    check_call "/fib/1/5" 200 "[1, 1, 2, 3, 5]"
}


# Helper functions
#
function start
{
    $SERVER_CMD_LINE &
    sleep 0.5  # port might not open if check too early
}

function stop
{
    pkill -f "$SERVER_CMD_LINE" &>/dev/null
}

function check_call
{
    local uri=${1:?}
    local expected_status=${2:?}
    local expected_body=${3:?}
    local rc=0
    local out=""
    local status
    local body

    echo "Requesting ${SERVER_URL}${uri}"
    out=$(curl -is "${SERVER_URL}${uri}")
    rc=$?

    # Output before returning non-zero (error)
    trap 'echo "$out"' RETURN

    (( rc == 0 )) || return 1
    [[ $out =~ ^HTTP/1\.[0-1]\ $expected_status ]] || return 1
    [[ $out == *Content-Type:\ application/json* ]] || return 1
    [[ $out == *${expected_body}* ]] || return 1

    # Clean up on-return handler (and return 0)
    trap '' RETURN
}

function all_tests
{
    declare -f | grep -Eo '^test_[a-z_]+'
}

function run_test
{
    local t=${1:?}
    local out

    printf "%-40s " "* Running $t"
    out=$(eval $t 2>&1)
    if (( $? != 0 )); then
        echo -e "\x1b[31mFAIL\x1b[0m"
        [[ -z $out ]] || echo "$out" | sed 's/^/  | /'
        return 1
    else
        echo -e "\x1b[32mPASS\x1b[0m"
        return 0
    fi
}

function main
{
    local -i total=0
    local -i failed=0
    local -a tests=()
    local t

    start

    if (( $# == 0 )); then
        tests=( $(all_tests) )
    else
        tests=( "$@" )
    fi

    for t in ${tests[@]}; do
        (( total += 1 ))
        run_test $t || {
            (( failed += 1 ))
        }
    done

    stop

    echo "Executed $total tests, $failed failed"
    (( failed == 0 ))  # Test result is return code
}

main "$@"
