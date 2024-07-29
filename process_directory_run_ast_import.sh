#!/bin/bash

# 检查是否传递了目录路径参数
if [ $# -ne 1 ]; then
  echo "Usage: $0 <path-to-python-directory>"
  exit 1
fi

# 获取传递的目录路径，并去除末尾的斜杠
DIRECTORY_PATH=$1
DIRECTORY_PATH="${DIRECTORY_PATH%/}"

# 检查传递的参数是否是一个有效的目录
if [ ! -d "$DIRECTORY_PATH" ]; then
  echo "Error: $DIRECTORY_PATH is not a directory"
  exit 1
fi

# 遍历目录下的所有 Python 文件（不递归）
for PYTHON_FILE in "$DIRECTORY_PATH"/*.py;
do
  if [ -f "$PYTHON_FILE" ]; then
    bash "$(dirname "$0")/run_ast_import.sh" "$PYTHON_FILE"
  fi
done
