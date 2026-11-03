#!/usr/bin/env python3
"""Проверка относительных ссылок в markdown-документах репозитория.

Скрипт не ходит в сеть: проверяются только ссылки на файлы внутри репозитория.
Внешние URL (http/https), якоря (#...) и mailto игнорируются.

Примеры:

    python3 scripts/check-links.py                      # только ссылки на документы
    python3 scripts/check-links.py --assets             # ещё и изображения
    python3 scripts/check-links.py --section docs/04-services
    python3 scripts/check-links.py --include-archive    # вместе с архивом

Код возврата: 0 — битых ссылок на документы нет (отсутствующие изображения не
считаются ошибкой, они перечисляются отдельно), 1 — найдены битые ссылки на документы.
"""

from __future__ import annotations

import argparse
import os
import re
import sys
from collections import defaultdict
from urllib.parse import unquote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LINK_RE = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)")
SKIP_DIRS = {".git", "node_modules", ".venv", "__pycache__"}
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".gif", ".svg", ".webp", ".bmp")


def iter_markdown(base: str, include_archive: bool):
    for dirpath, dirnames, filenames in os.walk(base):
        dirnames[:] = sorted(d for d in dirnames if d not in SKIP_DIRS)
        rel_dir = os.path.relpath(dirpath, base)
        if rel_dir.split(os.sep)[0] == "archive" and not include_archive:
            dirnames[:] = []
            continue
        for name in sorted(filenames):
            if name.lower().endswith(".md"):
                yield os.path.join(dirpath, name)


def iter_links(path: str):
    """Возвращает (строка, is_image, цель) для ссылок вне блоков кода."""
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, start=1):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            if in_fence:
                continue
            # инлайн-код (`...`) не считаем ссылками: там бывают примеры разметки
            line = re.sub(r"`[^`]*`", "", line)
            for match in LINK_RE.finditer(line):
                bang, _text, target = match.groups()
                yield lineno, bang == "!", target


def is_external(target: str) -> bool:
    return (
        not target
        or target.startswith(("#", "mailto:", "tel:", "data:"))
        or re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", target) is not None
    )


def resolve(doc: str, target: str) -> str:
    path = unquote(target.split("#", 1)[0].split("?", 1)[0])
    return os.path.normpath(os.path.join(os.path.dirname(doc), path))


def main() -> int:
    parser = argparse.ArgumentParser(description="Проверка относительных ссылок в markdown")
    parser.add_argument("--assets", action="store_true", help="проверять и ссылки на изображения")
    parser.add_argument("--section", metavar="PATH", help="проверять только указанный каталог/файл")
    parser.add_argument("--include-archive", action="store_true", help="включить каталог archive/")
    parser.add_argument("--quiet", action="store_true", help="не печатать список файлов, только сводку")
    args = parser.parse_args()

    base = os.path.join(ROOT, args.section) if args.section else ROOT
    base = os.path.abspath(base)
    if not os.path.exists(base):
        print(f"Нет такого пути: {args.section}", file=sys.stderr)
        return 2
    if os.path.isfile(base):
        docs = [base]
        search_root = os.path.dirname(base)
    else:
        docs = list(iter_markdown(base, args.include_archive))
        search_root = base

    broken_docs: dict[str, list[tuple[int, str]]] = defaultdict(list)
    broken_assets: dict[str, list[tuple[int, str]]] = defaultdict(list)
    missing_assets: dict[str, list[tuple[int, str]]] = defaultdict(list)
    checked = 0

    for doc in docs:
        for lineno, is_image, target in iter_links(doc):
            if is_external(target):
                continue
            checked += 1
            resolved = resolve(doc, target)
            rel = os.path.relpath(doc, search_root)
            if os.path.exists(resolved):
                continue
            looks_like_image = is_image or target.lower().split("#")[0].endswith(IMAGE_EXT)
            if looks_like_image:
                if args.assets:
                    missing_assets[rel].append((lineno, target))
            else:
                broken_docs[rel].append((lineno, target))
            _ = broken_assets  # изображения считаются отдельно, «битыми ссылками» не считаются

    def report(title: str, data: dict[str, list[tuple[int, str]]]) -> None:
        if not data:
            return
        print(f"\n{title}")
        for doc in sorted(data):
            items = data[doc]
            print(f"  {doc}  ({len(items)})")
            if not args.quiet:
                for lineno, target in items[:20]:
                    print(f"    строка {lineno}: {target}")
                if len(items) > 20:
                    print(f"    … и ещё {len(items) - 20}")

    print(f"Проверено markdown-файлов: {len(docs)}; относительных ссылок: {checked}")
    report("Битые ссылки на документы:", broken_docs)
    if args.assets:
        report("Отсутствующие изображения:", missing_assets)

    if not broken_docs and not (args.assets and missing_assets):
        print("\nПроблем не найдено.")
        return 0

    if broken_docs:
        print(f"\nИтого битых ссылок: {sum(len(v) for v in broken_docs.values())}")
        return 1
    print(f"\nИтого отсутствующих изображений: {sum(len(v) for v in missing_assets.values())} "
          f"(разметка готова, файлы ещё не загружены — см. docs/images/README.md)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
