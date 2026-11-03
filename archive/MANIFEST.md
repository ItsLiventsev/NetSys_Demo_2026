# MANIFEST — метаданные импорта архива

Дата импорта: **2026-11-03**. Метод: слияние дерева исходного репозитория в подкаталог `archive/<год>/` с сохранением второго родителя (subtree-подобный merge, без переписывания истории).

## Сводка

| Год | Исходный репозиторий | HEAD исходника | Коммитов | Файлов | Объём | Коммит-импорт |
| :-: | :-- | :-- | :-: | :-: | :-: | :-- |
| 2022 | `ItsLiventsev/NetSys_Demo_2022` | `b5825d10dcb8c597fc465c0980b7172c3f8a7737` | 1 | 46 | 744 КБ | `16c6e2171b61990ac228d67e88d0ae5d2cf270cc` |
| 2023 | `ItsLiventsev/NetSys_Demo_2023` | `0378265347b82fa9a10ba8df351ae0049d895801` | 5 | 1 | 72 КБ | `2f761c8e993a1c789421e37ce7cbc3d25f520a77` |
| 2024 | `ItsLiventsev/NetSys_Demo_2024` | `62e20cd1acab7875d2ca963786a55b43050a5822` | 69 | 3 | 1,4 МБ | `97717c951c4d2c2ddd937ed4ecea8a01d0b2f6ba` |
| 2025 | `ItsLiventsev/NetSys_Demo_2025` | `40635e11c67a0c87880e4a1591a41ee309997b4f` | 63 | 98 | 8,2 МБ | `18b9bc2ff1d8db8f807256e24518c0a5a50c36c4` |

Итого: **148 файлов**, ~11 МБ рабочего дерева, **138 коммитов** исходной истории (1 + 5 + 69 + 63).

Проверка целостности на момент импорта: `diff -r` рабочего дерева исходного клона и каталога `archive/<год>/` — расхождений нет.

## 2022 — NetSys_Demo_2022

- URL: <https://github.com/ItsLiventsev/NetSys_Demo_2022> (ветка `main`)
- Создан: 2022-07-09, последний коммит: 2022-07-09 («Add files via upload»)
- В форках не состоит, лицензия не указана
- Структура:

```
archive/2022/
├── README.md                 полный разбор ДЭ 2022
├── azure/autodeploy/         Terraform для Azure: 12 файлов (11 .tf + README)
├── docs/autodeploy/          Terraform/PowerCLI для vSphere: 11 файлов
├── docs/autoassess/          Terraform/PowerCLI для оценки: 11 файлов
├── docs/autochecker/         PowerShell/YAML авточекер: 7 файлов
├── docs/marks/               demoassess.xlsx, demoassessauto.xlsx
└── iso/README.MD
```

- Примечание: README ссылается на внешние репозитории (`storm39mad/DEMO2022`, `2c9/demoex2022`) — это исторические источники материалов, ссылки внутри архива не переписывались.

## 2023 — NetSys_Demo_2023

- URL: <https://github.com/ItsLiventsev/NetSys_Demo_2023> (ветка `main`)
- Создан: 2022-11-09, последний коммит: 2023-01-28
- Содержимое: единственный `README.md` (72 КБ) — конспект linux-only варианта «DEMO2022-2023-linux-only»
- Изображения не хранятся в репозитории: README ссылается на `user-images.githubusercontent.com`

## 2024 — NetSys_Demo_2024

- URL: <https://github.com/ItsLiventsev/NetSys_Demo_2024> (ветка `main`)
- Создан: 2023-12-06, последний коммит: 2024-05-14
- Содержимое:

```
archive/2024/
├── README.md                       стенд ПК № 8, 2023–2024
├── Common version (version 0.1).md конспект по ALT Linux
└── KOD_09.02.06-1-2024_TOM _1.pdf  КОД 2024
```

- Примечание: имя файла `KOD_09.02.06-1-2024_TOM _1.pdf` содержит пробел перед `_1` — оставлено как в исходнике.

## 2025 — NetSys_Demo_2025

- URL: <https://github.com/ItsLiventsev/NetSys_Demo_2025> (ветка `main`)
- Создан: 2024-08-25, последний коммит: 2025-05-17
- Содержимое:

```
archive/2025/
├── README.md                        стенд @pk8.mskobr, 2024–2025 (модули 1–4)
├── ASDaC_default_ALT.conf_v2.txt    конфиг PVE-скрипта авторазвёртывания
├── screens/                         91 скриншот (image.png, image-1…image-90.png)
├── КОД 09.02.06-1-2025 Том 1.pdf    КОД 2025
└── screens/.placeholder              служебный файл
```

- Примечание: раздел «Данные для авторизации в виртуальных машинах стенда» содержит учебные пароли (`P@ssw0rd`) — они относятся к демонстрационному стенду и не являются секретами.

## Как воспроизвести импорт

```bash
git remote add src2025 https://github.com/ItsLiventsev/NetSys_Demo_2025.git
git fetch --no-tags src2025 main
git merge -s ours --no-commit --allow-unrelated-histories src2025/main
git read-tree --prefix=archive/2025/ -u src2025/main
git commit -m "archive: полный слепок репозитория NetSys_Demo_2025 (история сохранена)"
```

Аналогично для остальных лет (подставить год). Команда `git read-tree --prefix` раскладывает корень исходного репозитория в `archive/<год>/`, а `git merge -s ours` сохраняет исходную ветку вторым родителем — история остаётся достижимой через `<импорт>^2`.

---

[← Архив](README.md) | [Корневой README](../README.md)
