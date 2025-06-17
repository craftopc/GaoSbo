import requests
import json
import os
import subprocess
import time
from urllib.parse import urlparse

ip = "10.50.100.10"
token = "f793c5576a4e857883d4cc0a0cfaa736"
race_id = "32c9cee6c67f7dda6d93712461071abd"

# AI配置
OLLAMA_URL = "http://192.168.1.5:11434/api/chat"
MODEL = "qwen2.5-coder:14b"


def get_questions():
    url = f"http://{ip}/api/ct/web/ai_race/race/checkpoints/robot/"
    params = {"token": token, "race_id": race_id}
    res = requests.get(url=url, params=params)
    return json.loads(res.text)


def post_flag(checkpoint_id):
    url = f"http://{ip}/api/ct/web/ai_race/race/flag/robot/"
    data = {
        "token": token,
        "checkpoint_id": checkpoint_id,
        "race_id": race_id,
        "flag": "flag{YFGlUEZ1HYAuAJTDK7Vhlh3HCMw6NDjX}",
    }
    res = requests.post(url=url, json=data)
    return res


def download_file(url, filename):
    """下载附件文件"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"已下载附件: {filename}")
        return True
    except Exception as e:
        print(f"下载附件失败: {e}")
        return False


def run_ghidra_decompile(binary_path):
    """运行Ghidra反编译脚本"""
    try:
        # 这里需要根据实际的Ghidra安装路径和脚本路径调整
        # 示例命令，实际使用时需要配置正确的Ghidra路径
        print("开始反编译二进制文件...")
        print("注意: 请确保已正确配置Ghidra环境并手动运行DecompileFunction.py")
        os.system("rm -rf /tmp/ghidra_proj")
        os.system("mkdir -p /tmp/ghidra_proj")
        os.system(
            f"/opt/ghidra/support/analyzeHeadless /tmp/ghidra_proj myproj -import {binary_path} -scriptPath ./ -postScript DecompileFunction.py"
        )
        return True
    except Exception as e:
        print(f"反编译失败: {e}")
        return False


def clean_decompiled_code():
    """清理反编译代码"""
    try:
        subprocess.run(["python", "clean.py"], check=True)
        print("反编译代码清理完成")
        return True
    except Exception as e:
        print(f"清理代码失败: {e}")
        return False


def send_to_ai(content, task_description=""):
    """发送内容给AI进行分析"""
    prompt = f"""请分析以下反编译的C代码，找出其中的安全漏洞（如缓冲区溢出、格式化字符串漏洞等），并生成相应的exploit代码。

任务描述: {task_description}

反编译代码:
{content}

请提供:
1. 漏洞分析
2. 利用思路
3. 完整的exploit代码（Python）
"""

    messages = [{"role": "user", "content": prompt}]
    payload = {"model": MODEL, "messages": messages}

    try:
        response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=300)
        reply = ""
        for line in response.iter_lines():
            if line:
                data = json.loads(line.decode())
                if "message" in data and "content" in data["message"]:
                    reply += data["message"]["content"]
                if data.get("done", False):
                    break
        return reply.strip()
    except Exception as e:
        print(f"AI分析失败: {e}")
        return None


def save_exploit(exploit_code):
    """保存生成的exploit代码"""
    try:
        with open("exp.py", "w", encoding="utf-8") as f:
            f.write(exploit_code)
        print("Exploit代码已保存为 exp.py")
        return True
    except Exception as e:
        print(f"保存exploit代码失败: {e}")
        return False


class Data:
    def __init__(self) -> None:
        self.res: dict = get_questions()

    def get_total(self) -> int:
        return self.res["data"]["total"]

    def get_list(self) -> list:
        return self.res["data"]["list"]

    def get_list_info(self, idx):
        list = self.get_list()
        l = []
        l.append(list[idx]["resource_id"])
        l.append(list[idx]["name"])
        l.append(list[idx]["attachment"][0]["name"])  # 修复索引错误
        l.append(list[idx]["attachment"][0]["url"])
        l.append(list[idx]["scene_addresses"][0]["access_ip"])  # 修复索引错误
        l.append(list[idx]["scene_addresses"][0]["access_port"])
        return l


def process_challenge(idx=0):
    """处理挑战题目的完整流程"""
    # data = Data()
    # resource_id, name, attachment_name, attachment_url, target_ip, target_port = (
    #    data.get_list_info(idx)
    # )

    name = "pie"
    resource_id = "c1b2d3e4f5g6h7i8j9k0l1m2n3o4p5q6"
    attachment_name = "pie"
    target_ip = "127.0.0.1"
    target_port = "12345"

    print(f"处理题目: {name}")
    print(f"资源ID: {resource_id}")
    print(f"附件: {attachment_name}")
    print(f"目标: {target_ip}:{target_port}")

    # 1. 下载附件
    # if not download_file(attachment_url, attachment_name):
    #    return False

    # 2. 反编译二进制文件
    print("\n=== 反编译阶段 ===")
    run_ghidra_decompile(attachment_name)

    # 3. 清理反编译代码
    print("\n=== 清理代码 ===")
    if not clean_decompiled_code():
        return False

    # 4. 读取清理后的代码
    try:
        with open("output.txt", "r", encoding="utf-8") as f:
            cleaned_code = f.read()
    except Exception as e:
        print(f"读取清理后的代码失败: {e}")
        return False

    # 5. 发送给AI分析
    print("\n=== AI分析阶段 ===")
    task_desc = f"题目名称: {name}, 目标: {target_ip}:{target_port}, 二进制文件: {attachment_name}"
    ai_response = send_to_ai(cleaned_code, task_desc)

    if not ai_response:
        return False

    print("AI分析结果:")
    print("=" * 50)
    print(ai_response)
    print("=" * 50)

    # 6. 尝试提取并保存exploit代码
    if "```python" in ai_response:
        try:
            start_idx = ai_response.find("```python") + len("```python")
            end_idx = ai_response.find("```", start_idx)
            exploit_code = ai_response[start_idx:end_idx].strip()
            save_exploit(exploit_code)
        except Exception as e:
            print(f"提取exploit代码失败: {e}")

    return True


if __name__ == "__main__":
    print("CTF自动化分析工具")
    print("=" * 30)

    # 获取题目列表
    # data = Data()
    # total = data.get_total()
    total = 1
    print(f"共有 {total} 道题目")

    process_challenge(0)

    # 选择要处理的题目
#  try:
#      idx = int(input(f"请选择要处理的题目索引 (0-{total-1}): "))
#      if 0 <= idx < total:
#          process_challenge(idx)
#      else:
#          print("无效的题目索引")
#  except ValueError:
#      print("请输入有效的数字")
#  except KeyboardInterrupt:
#      print("\n程序被用户中断")
