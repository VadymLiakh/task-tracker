"""Task Tracker — консольний менеджер задач."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "libs" / "console-utils"))

from console_utils import colorize, format_table  # noqa: E402
from tracker.stats import get_stats  # noqa: E402
from tracker.storage import load_tasks, save_tasks  # noqa: E402


def cmd_add(args):
    tasks = load_tasks()
    new_id = max((t["id"] for t in tasks), default=0) + 1
    tasks.append({"id": new_id, "title": args.title, "done": False})
    save_tasks(tasks)
    print(f"Додано задачу #{new_id}: {args.title}")


def cmd_list(args):
    tasks = load_tasks()
    if not tasks:
        print("Список задач порожній.")
        return
    rows = [(t["id"], t["title"], "так" if t["done"] else "ні") for t in tasks]
    print(format_table(["ID", "Задача", "Виконано"], rows))


def cmd_done(args):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == args.id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Задачу #{args.id} виконано.")
            return
    print(f"Задачу #{args.id} не знайдено.")


def cmd_remove(args):
    tasks = load_tasks()
    left = [t for t in tasks if t["id"] != args.id]
    if len(left) == len(tasks):
        print(f"Задачу #{args.id} не знайдено.")
        return
    save_tasks(left)
    print(f"Задачу #{args.id} видалено.")


def cmd_stats(args):
    s = get_stats(load_tasks())
    print(f"Усього задач: {s['total']}")
    print(colorize(f"Виконано: {s['done']} ({s['percent']}%)", "green"))
    print(colorize(f"Залишилось: {s['left']}", "yellow"))


def build_parser():
    parser = argparse.ArgumentParser(description="Консольний менеджер задач")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="додати задачу")
    p.add_argument("title")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="показати всі задачі")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="позначити задачу виконаною")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("remove", help="видалити задачу")
    p.add_argument("id", type=int)
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("stats", help="показати статистику")
    p.set_defaults(func=cmd_stats)
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
