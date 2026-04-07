import json, os, sys
from datetime import datetime

DATA_FILE = "tasks.json"

def load():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

def add(title):
    tasks = load()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    tasks.append(task)
    save(tasks)
    print(f"[+] Task ditambahkan: {title}")

def list_tasks():
    tasks = load()
    if not tasks:
        print("Belum ada task.")
        return
    print(f"\n{'ID':<5} {'STATUS':<8} {'TASK':<30} {'DIBUAT'}")
    print("-" * 60)
    for t in tasks:
        status = "[x]" if t["done"] else "[ ]"
        print(f"{t['id']:<5} {status:<8} {t['title']:<30} {t['created']}")

def done(task_id):
    tasks = load()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save(tasks)
            print(f"[v] Task #{task_id} selesai!")
            return
    print(f"Task #{task_id} tidak ditemukan.")

def delete(task_id):
    tasks = load()
    new = [t for t in tasks if t["id"] != task_id]
    if len(new) == len(tasks):
        print(f"Task #{task_id} tidak ditemukan.")
        return
    save(new)
    print(f"[-] Task #{task_id} dihapus.")

def help_text():
    print("""
Todo CLI - Sistem Operasi Kelompok
===================================
python main.py add "nama task"
python main.py list
python main.py done 
python main.py delete 
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_text(); sys.exit()
    cmd = sys.argv[1]
    if cmd == "add" and len(sys.argv) >= 3:
        add(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(sys.argv) == 3:
        done(int(sys.argv[2]))
    elif cmd == "delete" and len(sys.argv) == 3:
        delete(int(sys.argv[2]))
    else:
        help_text()
