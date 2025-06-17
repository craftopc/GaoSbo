import re

with open("decompiled_functions.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

clean_lines = []
for line in lines:
    s = line.strip()
    # 去除空行和全=分隔符
    if not s or set(s) == {"="}:
        continue
    # 去除整行的注释
    if s.startswith("/*") or s.startswith("//"):
        continue
    # 去除行内 /* ... */ 注释
    s = re.sub(r"/\*.*?\*/", "", s)
    # 去除行内 // 注释
    s = re.sub(r"//.*", "", s)
    if s.strip():
        clean_lines.append(s)

with open("output.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(clean_lines))
