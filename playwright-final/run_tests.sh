#!/bin/bash
if [ -n "$1" ]; then
    pytest -k "$1"
else
    pytest
fi
allure generate allure-results -o allure-report --clean --single-file
open allure-report/index.html

# ./run_tests.sh                                    # chạy toàn bộ test
# ./run_tests.sh test_login_with_valid_credentials  # chạy đúng 1 test theo tên
# ./run_tests.sh "login"                            # chạy tất cả test có chứa chữ "login"
