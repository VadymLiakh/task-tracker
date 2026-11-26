"""Task Tracker — консольний менеджер задач."""

import argparse

from tracker.storage import load_tasks, save_tasks


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
    for t in tasks:
        mark = "x" if t["done"] else " "
        print(f"[{mark}] #{t['id']} {t['title']}")


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
    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
