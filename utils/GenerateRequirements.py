import subprocess

# 运行 pip freeze 命令并获取输出
def generate_requirements():
    result = subprocess.run(['pip', 'freeze'], capture_output=True, text=True)

    # 将输出写入 requirements.txt 文件
    with open('requirements.txt', 'w') as file:
        file.write(result.stdout)