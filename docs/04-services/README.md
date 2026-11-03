# 04. Справочник по сервисам и этапам

24 разбора «как настраивается конкретная технология»: команды, конфигурационные файлы, проверка и диагностика. Материал не привязан к одному заданию — по нему удобно восстанавливать забытые команды и разбираться со службой, которая «не работает».

## Про какой стенд эти разборы

Разборы написаны под сценарий из двух площадок — **COD** (`cod.ssa2026.region`) и **офис A** (`office.ssa2026.region`):

- маршрутизаторы `rtr-cod`, `rtr-a` — EcoRouter;
- межсетевой экран `fw-cod` — Ideco NGFW;
- коммутаторы `sw1-a`, `sw2-a`, `sw1-cod`, `sw2-cod` — ALT Linux + openvswitch;
- серверы `srv1-cod`, `srv2-cod`, `dc-a`, рабочие станции `cli1-a`, `cli2-a`, `admin-cod`;
- провайдер `ISP`.

Это **другой стенд**, чем в [`../03-walkthrough`](../03-walkthrough/README.md) (там HQ/BR на стенде ПК № 8). Поэтому:

- используйте эти файлы как справочник по технологиям, а не как готовый сценарий экзамена;
- имена интерфейсов, адреса и названия устройств подставляйте свои;
- последовательность этапов (01 → 23) отражает логику построения сети «снизу вверх» и годится как маршрут изучения.

## Оглавление

| № | Файл | Тема | Ключевые технологии |
| :-: | :-- | :-- | :-- |
| 0 | [`00-isp-config.md`](00-isp-config.md) | Настройка ВМ ISP | имена, IPv4, forwarding, NAT (iptables), BIND, Chrony, BGP (FRR) |
| 1 | [`01-rtr-ip-config.md`](01-rtr-ip-config.md) | Имена и IP-адресация на `rtr-cod` и `rtr-a` | EcoRouter: hostname, domain, интерфейсы, статические маршруты, VLAN |
| 2 | [`02-fw-cod-config.md`](02-fw-cod-config.md) | Первичная настройка `fw-cod` | Ideco NGFW: вход администратора, интерфейсы, сверка MAC, LAN-роль |
| 3 | [`03-bgp-config.md`](03-bgp-config.md) | BGP на `rtr-cod` | FRR: соседство с ISP, анонсы, проверка атрибутов и маршрутов |
| 4 | [`04-tunnel-config.md`](04-tunnel-config.md) | Туннель между площадками | GRE-туннель `rtr-cod` ↔ `rtr-a`, маршрутизация поверх туннеля |
| 5 | [`05-nat-config.md`](05-nat-config.md) | Доступ в Интернет | NAT на маршрутизаторах (EcoRouter) и на межсетевом экране |
| 6 | [`06-ospf-config.md`](06-ospf-config.md) | Динамическая маршрутизация между офисами | OSPF, соседство через туннель, таблицы маршрутов |
| 7 | [`07-switching-config.md`](07-switching-config.md) | Коммутация `sw1-a` / `sw2-a` | openvswitch, bridge, RSTP, management-VLAN |
| 8 | [`08-fwcod-web-config.md`](08-fwcod-web-config.md) | Доступ к веб-интерфейсу `fw-cod` | настройка через консоль, лицензирование |
| 9 | [`09-fwcod-vlan-config.md`](09-fwcod-vlan-config.md) | VLAN-интерфейсы на `fw-cod` | Ethernet + VLAN subinterfaces, маршрутизация между VLAN |
| 10 | [`10-switching-cod-config.md`](10-switching-cod-config.md) | Коммутация `sw1-cod` / `sw2-cod` | openvswitch, RSTP, авторизация через `fw-cod` |
| 11 | [`11-hosts-ip-config.md`](11-hosts-ip-config.md) | Имена и адреса остальных устройств | ALT Linux: hostname, статические адреса серверов и рабочих станций |
| 12 | [`12-radius-config.md`](12-radius-config.md) | Административный доступ через RADIUS | FreeRADIUS на `srv1-cod`, клиенты, пользователи, EcoRouter |
| 13 | [`13-ntp-config.md`](13-ntp-config.md) | Синхронизация времени | NTP на EcoRouter, Chrony на ALT Linux, NTP на Ideco NGFW |
| 14 | [`14-dns-cod-config.md`](14-dns-cod-config.md) | DNS в COD | BIND: прямая зона `cod.ssa2026.region`, обратная `168.192.in-addr.arpa`, форвардинг |
| 15 | [`15-samba-ad-config.md`](15-samba-ad-config.md) | Контроллер домена | Samba AD на `dc-a`, BIND9_DLZ, ввод `cli1-a`/`cli2-a`, OU, группы, GPO |
| 16 | [`16-dns-office-config.md`](16-dns-office-config.md) | DNS в офисе A | A-записи офиса, обратная зона `20.172.in-addr.arpa`, пересылка запросов в COD |
| 17 | [`17-ca-config.md`](17-ca-config.md) | Центр сертификации | OpenSSL: корневой CA, выпуск сертификатов, распространение корневого сертификата |
| 18 | [`18-postgresql-config.md`](18-postgresql-config.md) | Сервер баз данных | PostgreSQL, `pg_hba.conf`, удалённый доступ, DBeaver |
| 19 | [`19-iscsi-config.md`](19-iscsi-config.md) | СХД по iSCSI | target (`tgtadm`/`targets.conf`) и initiator, LVM поверх iSCSI, Proxmox |
| 20 | [`20-lvm-config.md`](20-lvm-config.md) | Управление дисками (LVM) | PV → VG → LV, XFS, `/etc/fstab` |
| 21 | [`21-nfs-config.md`](21-nfs-config.md) | Сетевой файловый сервис | экспорт NFS, клиентское монтирование, права доступа |
| 22 | [`22-zabbix-config.md`](22-zabbix-config.md) | Мониторинг | MariaDB + Zabbix server/frontend + агенты, веб-настройка, уведомления |
| 23 | [`23-freepbx-config.md`](23-freepbx-config.md) | IP-телефония | FreePBX/SangomaOS, SIP-транк, добавочные номера, softphone, проверка вызовов |

## Как читать

- **Учебный маршрут.** Идти по номерам 00 → 23: сначала ISP и адресация, потом коммутация и маршрутизация, затем сервисы.
- **Точечно.** Открыть нужный файл через оглавление выше; в каждом документе есть «Содержание», «Описание», «Задачи», пошаговые части и раздел проверки.
- **Перед экзаменом.** Сверять последовательность с чек-листом модуля в [`../02-modules`](../02-modules/README.md): задания модулей идут в другом порядке, чем этот справочник.

## Про скриншоты

В текстах есть ссылки на изображения вида `../images/<имя>.png`. Каталог [`../images`](../images/README.md) пока не заполнен — ссылки заранее размечены под имена файлов, которые нужно положить при добавлении скриншотов. Проверить, каких файлов не хватает:

```bash
python3 scripts/check-links.py --assets --section docs/04-services
```

---

[← Документация](../README.md) | [Обзор](../00-overview.md) | [Пошаговые разборы ←](../03-walkthrough/README.md)
