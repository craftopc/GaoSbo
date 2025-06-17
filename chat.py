import requests
import json

OLLAMA_URL = "http://192.168.1.5:11434/api/chat"
MODEL = "qwen2.5-coder:14b"


def chat_with_ollama():
    messages = []
    print("和 Ollama 聊天，输入 exit 退出")
    while True:
        user_input = input("你: ")
        if user_input.strip().lower() == "exit":
            break
        messages.append({"role": "user", "content": user_input})
        payload = {"model": MODEL, "messages": messages}
        try:
            response = requests.post(OLLAMA_URL, json=payload, stream=True, timeout=120)
            reply = ""
            # Ollama 流式返回多行 JSON
            for line in response.iter_lines():
                if line:
                    data = json.loads(line.decode())
                    if "message" in data and "content" in data["message"]:
                        reply += data["message"]["content"]
                    if data.get("done", False):
                        break
            print("Ollama:", reply.strip())
            messages.append({"role": "assistant", "content": reply.strip()})
        except Exception as e:
            print("请求失败:", e)


if __name__ == "__main__":
    chat_with_ollama()
