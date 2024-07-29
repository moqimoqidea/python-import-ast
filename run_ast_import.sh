#!/bin/bash

# 检查是否传递了文件路径参数
if [ $# -ne 1 ]; then
  echo "Usage: $0 <path-to-python-file>"
  exit 1
fi

# 获取传递的文件路径
PYTHON_FILE_PATH=$1

# 获取文件名（不包括路径和扩展名）
BASENAME=$(basename -- "$PYTHON_FILE_PATH")
FILENAME="${BASENAME%.*}.txt"

# 运行 Python 脚本并将输出写入文件
python ast-import.py \
  --ignore-local \
  --ignore-relative \
  --path "$PYTHON_FILE_PATH" > "$FILENAME"

# 输出生成的文件名
echo "Output written to $FILENAME"
