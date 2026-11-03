# MIGRATION — карта переносов

Реструктуризация от **2026-11-03**. Если на материалы репозитория ссылались извне (Yonote, чаты, закладки), прежние пути нужно заменить по таблице ниже.

Git-история файлов сохранена: переносы выполнены через `git mv`, поэтому в `git log --follow` видна история до переезда.

## Нормативные документы

| Было | Стало | Примечание |
| :-- | :-- | :-- |
| `КОД 09.02.06-1-2026 Том 1 (Общес.pdf` | [`docs/01-normative/kod-09.02.06-1-2026-tom1.pdf`](docs/01-normative/kod-09.02.06-1-2026-tom1.pdf) | имя файла было обрезано и содержало пробелы |
| `Система оценивания.pdf` | [`docs/01-normative/grading-system-2026.pdf`](docs/01-normative/grading-system-2026.pdf) | латинский slug вместо кириллицы |
| `Пример отчета на ДЭ.odt` | [`docs/01-normative/report-sample-2026.odt`](docs/01-normative/report-sample-2026.odt) | содержимое не менялось |

## Корневой README (разделён на части)

Прежний `README.md` был одним файлом на 75 КБ, в котором смешивались описание экзамена, разбор модуля 1 и пошаговые разборы модуля 2. Содержимое распределено без потерь:

| Фрагмент прежнего `README.md` | Куда перенесён |
| :-- | :-- |
| Строки 1–12: титул, ссылки на стенд, Yonote, задание | [`docs/00-overview.md`](docs/00-overview.md) (расширено) |
| Строки 13–695: «Модуль 1. Настройка сетевой инфраструктуры» | [`docs/03-walkthrough/module-1.md`](docs/03-walkthrough/module-1.md) (текст без изменений) |
| Строки 700–1112: «Модуль 2. Задание 1» | [`docs/03-walkthrough/module-2-task-1-samba-dc.md`](docs/03-walkthrough/module-2-task-1-samba-dc.md) |
| Строки 1113–1329: «Модуль 2. Задание 2» | [`docs/03-walkthrough/module-2-task-2-raid.md`](docs/03-walkthrough/module-2-task-2-raid.md) |
| Строки 1330–1564: «Модуль 2. Задание 3» | [`docs/03-walkthrough/module-2-task-3-nfs.md`](docs/03-walkthrough/module-2-task-3-nfs.md) |
| Строки 1565–1832: «Модуль 2. Задание 4» | [`docs/03-walkthrough/module-2-task-4-chrony.md`](docs/03-walkthrough/module-2-task-4-chrony.md) |
| Строка 698: «Дальше идёт немного в разнобой…» | не переносилась (служебная пометка) |

Новый корневой [`README.md`](README.md) — навигационный хаб: структура репозитория, быстрые ссылки, архив.

## Разборы по модулям

| Было | Стало |
| :-- | :-- |
| `Разборы по модулю/module1.md` | [`docs/02-modules/module-1-network-infrastructure.md`](docs/02-modules/module-1-network-infrastructure.md) |
| `Разборы по модулю/module2.md` | [`docs/02-modules/module-2-system-administration.md`](docs/02-modules/module-2-system-administration.md) |
| `Разборы по модулю/module3.md` | [`docs/02-modules/module-3-network-operations.md`](docs/02-modules/module-3-network-operations.md) |

## Разборы по заданиям модуля 2

Файлы `taskN-*.md` были побайтовыми копиями разделов корневого README (проверено сравнением). Оставлены как самостоятельные документы, имена без суффикса ` (1)`:

| Было | Стало |
| :-- | :-- |
| `Разборы по заданию/task1-samba-dc (1).md` | [`docs/03-walkthrough/module-2-task-1-samba-dc.md`](docs/03-walkthrough/module-2-task-1-samba-dc.md) |
| `Разборы по заданию/task2-raid (1).md` | [`docs/03-walkthrough/module-2-task-2-raid.md`](docs/03-walkthrough/module-2-task-2-raid.md) |
| `Разборы по заданию/task3-nfs (1).md` | [`docs/03-walkthrough/module-2-task-3-nfs.md`](docs/03-walkthrough/module-2-task-3-nfs.md) |
| `Разборы по заданию/task4-ntp (1).md` | [`docs/03-walkthrough/module-2-task-4-chrony.md`](docs/03-walkthrough/module-2-task-4-chrony.md) |

## Разборы по сервисам

Каталог `Разборы по заданию/` переименован в `docs/04-services/`; имена файлов сохранены, поэтому замена в ссылках — только префикс каталога:

| Было | Стало |
| :-- | :-- |
| `Разборы по заданию/00-isp-config.md` | [`docs/04-services/00-isp-config.md`](docs/04-services/00-isp-config.md) |
| `Разборы по заданию/01-rtr-ip-config.md` | [`docs/04-services/01-rtr-ip-config.md`](docs/04-services/01-rtr-ip-config.md) |
| `Разборы по заданию/02-fw-cod-config.md` | [`docs/04-services/02-fw-cod-config.md`](docs/04-services/02-fw-cod-config.md) |
| `Разборы по заданию/03-bgp-config.md` | [`docs/04-services/03-bgp-config.md`](docs/04-services/03-bgp-config.md) |
| `Разборы по заданию/04-tunnel-config.md` | [`docs/04-services/04-tunnel-config.md`](docs/04-services/04-tunnel-config.md) |
| `Разборы по заданию/05-nat-config.md` | [`docs/04-services/05-nat-config.md`](docs/04-services/05-nat-config.md) |
| `Разборы по заданию/06-ospf-config.md` | [`docs/04-services/06-ospf-config.md`](docs/04-services/06-ospf-config.md) |
| `Разборы по заданию/07-switching-config.md` | [`docs/04-services/07-switching-config.md`](docs/04-services/07-switching-config.md) |
| `Разборы по заданию/08-fwcod-web-config.md` | [`docs/04-services/08-fwcod-web-config.md`](docs/04-services/08-fwcod-web-config.md) |
| `Разборы по заданию/09-fwcod-vlan-config.md` | [`docs/04-services/09-fwcod-vlan-config.md`](docs/04-services/09-fwcod-vlan-config.md) |
| `Разборы по заданию/10-switching-cod-config.md` | [`docs/04-services/10-switching-cod-config.md`](docs/04-services/10-switching-cod-config.md) |
| `Разборы по заданию/11-hosts-ip-config.md` | [`docs/04-services/11-hosts-ip-config.md`](docs/04-services/11-hosts-ip-config.md) |
| `Разборы по заданию/12-radius-config.md` | [`docs/04-services/12-radius-config.md`](docs/04-services/12-radius-config.md) |
| `Разборы по заданию/13-ntp-config.md` | [`docs/04-services/13-ntp-config.md`](docs/04-services/13-ntp-config.md) |
| `Разборы по заданию/14-dns-cod-config.md` | [`docs/04-services/14-dns-cod-config.md`](docs/04-services/14-dns-cod-config.md) |
| `Разборы по заданию/15-samba-ad-config.md` | [`docs/04-services/15-samba-ad-config.md`](docs/04-services/15-samba-ad-config.md) |
| `Разборы по заданию/16-dns-office-config.md` | [`docs/04-services/16-dns-office-config.md`](docs/04-services/16-dns-office-config.md) |
| `Разборы по заданию/17-ca-config.md` | [`docs/04-services/17-ca-config.md`](docs/04-services/17-ca-config.md) |
| `Разборы по заданию/18-postgresql-config.md` | [`docs/04-services/18-postgresql-config.md`](docs/04-services/18-postgresql-config.md) |
| `Разборы по заданию/19-iscsi-config.md` | [`docs/04-services/19-iscsi-config.md`](docs/04-services/19-iscsi-config.md) |
| `Разборы по заданию/20-lvm-config.md` | [`docs/04-services/20-lvm-config.md`](docs/04-services/20-lvm-config.md) |
| `Разборы по заданию/21-nfs-config.md` | [`docs/04-services/21-nfs-config.md`](docs/04-services/21-nfs-config.md) |
| `Разборы по заданию/22-zabbix-config.md` | [`docs/04-services/22-zabbix-config.md`](docs/04-services/22-zabbix-config.md) |
| `Разборы по заданию/23-freepbx-config.md` | [`docs/04-services/23-freepbx-config.md`](docs/04-services/23-freepbx-config.md) |

## Изображения

| Было | Стало |
| :-- | :-- |
| `Images/<имя>.png` (от корня) | `docs/images/<имя>.png` |
| `images/<имя>.png` (из `Разборы по заданию/`) | `docs/images/<имя>.png` |

Сами файлы в репозитории отсутствовали и до реструктуризации; см. [`docs/images/README.md`](docs/images/README.md).

## Удалённые дубликаты

| Файл | Причина |
| :-- | :-- |
| `report_2026 (1).odt` | побайтовый дубликат `Пример отчета на ДЭ.odt` (одинаковый MD5) |
| `Пример отчета на ДЭ (1).odt` | побайтовый дубликат `Пример отчета на ДЭ.odt` |
| Разделы модуля 2 в корневом `README.md` | полные копии файлов `task1…task4*.md` |

Все удалённые файлы остаются в истории git (`git log --diff-filter=D --summary`).

## Архив

Новые каталоги, ранее жившие в отдельных репозиториях:

| Было | Стало |
| :-- | :-- |
| `ItsLiventsev/NetSys_Demo_2022` (корень репозитория) | [`archive/2022/`](archive/2022/) |
| `ItsLiventsev/NetSys_Demo_2023` (корень репозитория) | [`archive/2023/`](archive/2023/) |
| `ItsLiventsev/NetSys_Demo_2024` (корень репозитория) | [`archive/2024/`](archive/2024/) |
| `ItsLiventsev/NetSys_Demo_2025` (корень репозитория) | [`archive/2025/`](archive/2025/) |

Соответствие «год → коммит-импорт → исходный SHA» — в [`archive/MANIFEST.md`](archive/MANIFEST.md).

---

[← Корневой README](README.md) | [Документация](docs/README.md) | [CHANGELOG](CHANGELOG.md)
