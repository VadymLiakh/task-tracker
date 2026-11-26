"""Статистика виконання задач."""


def get_stats(tasks):
    total = len(tasks)
    done = len([t for t in tasks if t["done"]])
    percent = round(done / total * 100) if total else 0
    return {"total": total, "done": done, "left": total - done, "percent": percent}
