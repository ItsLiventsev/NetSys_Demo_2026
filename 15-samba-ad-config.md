# Модуль 15. Развёртывание контроллера домена на базе Samba AD

## Описание

Данный модуль описывает развёртывание контроллера домена Active Directory на базе Samba на dc-a, ввод рабочих станций в домен, создание организационной структуры и настройку групповых политик.

## Задачи

- Установка и настройка Samba AD на dc-a
- Интеграция с BIND DNS (BIND9_DLZ)
- Ввод рабочих станций cli1-a и cli2-a в домен
- Создание организационных подразделений (OU)
- Создание групп и пользователей
- Настройка групповых политик (GPO)

---

## 1. Подготовка dc-a (ALT Server)

### 1.1 Временная настройка DNS

```bash
echo "nameserver 77.88.8.8" > /etc/resolv.conf
```

### 1.2 Установка пакетов

```bash
apt-get update && apt-get install -y task-samba-dc bind bind-utils
```

### 1.3 Предотвращение конфликта зон

Если при установке системы было указано полное имя домена, система может создать зону `office.ssa2026.region`, что приведёт к конфликту с Samba.

Закомментировать все строки в файле `/etc/bind/local.conf`:

```bash
vim /etc/bind/local.conf
```

![local.conf](../images/samba_local_conf.png)

### 1.4 Отключение chroot

```bash
control bind-chroot disabled
```

### 1.5 Отключение KRB5RCACHETYPE

```bash
echo 'KRB5RCACHETYPE="none"' >> /etc/sysconfig/bind
```

### 1.6 Подключение плагина BIND_DLZ

```bash
echo 'include "/var/lib/samba/bind-dns/named.conf";' >> /etc/bind/named.conf
```

### 1.7 Настройка options.conf

Редактируем файл `/etc/bind/options.conf`:

```bash
vim /etc/bind/options.conf
```

Добавить в раздел `options`:

- **tkey-gssapi-keytab** — путь к ключевой таблице для GSS-API (интеграция с Kerberos)
- **minimal-responses yes** — уменьшает объём ответов
- **listen-on { any; }** — IP-адреса, на которых принимаются запросы
- **allow-query { any; }** — разрешённые подсети для DNS-запросов
- **allow-query-cache { any; }** — кэширование для всех
- **allow-recursion { any; }** — рекурсивные запросы для всех
- **forwarders { 100.100.100.100; }** — внешние DNS-серверы
- **forward first** — сначала пересылать, затем кешировать

![options.conf](../images/samba_options_conf.png)

В раздел `logging` добавить:

```
category lame-servers { null; };
```

![logging](../images/samba_logging.png)

---

## 2. Создание домена Samba AD

### 2.1 Очистка предыдущих конфигураций

```bash
rm -f /etc/samba/smb.conf
rm -rf /var/lib/samba/*
rm -rf /var/cache/samba
mkdir -p /var/lib/samba/sysvol
```

### 2.2 Интерактивное создание домена

```bash
samba-tool domain provision
```

При выполнении команды указать:

- **Realm:** OFFICE.SSA2026.REGION
- **Domain:** OFFICE
- **Server Role:** dc
- **DNS backend:** BIND9_DLZ
- **Administrator password:** P@ssw0rd

![samba-tool domain provision](../images/samba_provision.png)

### 2.3 Результат создания домена

![Результат provision](../images/samba_provision_result.png)

### 2.4 Запуск служб

```bash
systemctl enable --now samba
systemctl enable --now bind
```

### 2.5 Настройка Kerberos

При создании домена Samba автоматически генерирует файл `krb5.conf`:

```bash
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
```

### 2.6 Перезапуск Samba

```bash
systemctl restart samba
```

---

## 3. Проверка работы домена

### 3.1 Информация о домене

```bash
samba-tool domain info 127.0.0.1
```

![domain info](../images/samba_domain_info.png)

### 3.2 Проверка служб

```bash
smbclient -L localhost -U administrator
```

![smbclient](../images/samba_smbclient.png)

> **Примечание:** `netlogon` и `sysvol` создаются автоматически и необходимы для работы контроллера домена.

### 3.3 Проверка DNS

Проверка `/etc/resolv.conf`:

```bash
cat /etc/resolv.conf
```

![resolv.conf](../images/samba_resolv_conf.png)

Проверка SRV-записи Kerberos:

```bash
host -t SRV _kerberos._udp.office.ssa2026.region.
```

![check kerberos](../images/samba_check_kerberos.png)

Проверка SRV-записи LDAP:

```bash
host -t SRV _ldap._tcp.office.ssa2026.region.
```

![check ldap](../images/samba_check_ldap.png)

Проверка A-записи контроллера домена:

```bash
host -t A dc-a.office.ssa2026.region.
```

![check host](../images/samba_check_host.png)

### 3.4 Проверка Kerberos-аутентификации

```bash
kinit administrator@OFFICE.SSA2026.REGION
```

> ⚠️ **Важно:** Имя домена должно быть в ВЕРХНЕМ регистре!

![kinit](../images/samba_kinit.png)

Просмотр билета:

```bash
klist
```

![klist](../images/samba_klist.png)

---

## 4. Ввод рабочих станций в домен

### 4.1 Установка пакетов (cli1-a и cli2-a)

```bash
apt-get update && apt-get install -y task-auth-ad-sssd
```

### 4.2 Ввод в домен через ЦУС

Открыть: **Пользователи** → **Аутентификация**

Выбрать:
- **Домен Active Directory**
- Домен: `office.ssa2026.region`
- Имя компьютера: `cli1-a` (или `cli2-a`)
- **SSSD (в единственном домене)**

Нажать **Применить**.

![Настройки AD](../images/ad_join_settings.png)

### 4.3 Ввод учётных данных

Ввести имя пользователя `Administrator` и пароль, нажать **ОК**:

![Ввод пароля](../images/ad_join_password.png)

### 4.4 Результат

![Успешное присоединение](../images/ad_join_success.png)

### 4.5 Перезагрузка

Перезагрузить рабочую станцию для применения всех настроек.

---

## 5. Управление Active Directory (ADMC)

### 5.1 Установка ADMC (cli1-a)

```bash
apt-get install -y admc
```

### 5.2 Получение билета Kerberos

```bash
kinit administrator@OFFICE.SSA2026.REGION
```

![kinit на cli1-a](../images/ad_kinit_cli.png)

### 5.3 Запуск ADMC

Меню: **Системные** → **ADMC** или команда `admc`

![ADMC - Computers](../images/admc_computers.png)

---

## 6. Создание организационной структуры

### 6.1 Создание OU ofadmins

ПКМ на `office.ssa2026.region` → **Создать подразделение**

Имя: `ofadmins`

![Создание OU](../images/admc_create_ou.png)

### 6.2 Создание OU ofusers

Аналогично создать подразделение `ofusers`:

![OU созданы](../images/admc_ou_created.png)

### 6.3 Создание группы ofadmins

ПКМ на OU `ofadmins` → **Создать группу**

- Имя: `ofadmins`
- Область группы: Глобальная
- Тип группы: Безопасность

![Создание группы](../images/admc_create_group.png)

### 6.4 Создание группы ofusers

Аналогично создать группу `ofusers` в OU `ofusers`:

![Группа ofusers](../images/admc_group_ofusers.png)

---

## 7. Создание пользователей

### 7.1 Создание пользователя ofadmin1

ПКМ на OU `ofadmins` → **Создать пользователя**

- Имя: `ofadmin1`
- Имя для входа: `ofadmin1`
- Пароль: `P@ssw0rd`
- ☑ Пользователь не может изменить пароль
- ☑ Пароль не истекает

![Создание ofadmin1](../images/admc_create_user_ofadmin1.png)

### 7.2 Добавление в группу ofadmins

Свойства группы `ofadmins` → **Участники** → **Добавить** → `ofadmin1`

![Участники ofadmins](../images/admc_ofadmins_members.png)

### 7.3 Создание пользователя ofuser1

Аналогично создать пользователя `ofuser1` в OU `ofusers` и добавить в группу `ofusers`:

![Участники ofusers](../images/admc_ofusers_members.png)

### 7.4 Создание пользователя user1

Создать пользователя `user1` в стандартном контейнере `Users`:

![Создание user1](../images/admc_create_user1.png)

---

## 8. Проверка входа пользователей

### 8.1 Вход под ofadmin1 (cli2-a)

![Вход ofadmin1](../images/ad_login_ofadmin1.png)

### 8.2 Вход под ofuser1 (cli2-a)

![Вход ofuser1](../images/ad_login_ofuser1.png)

---

## 9. Настройка групповых политик (GPO)

### 9.1 Установка gpupdate (cli1-a и cli2-a)

```bash
apt-get install -y gpupdate
```

### 9.2 Включение модуля групповых политик

```bash
gpupdate-setup enable
```

### 9.3 Установка GPUI (cli1-a)

```bash
apt-get install -y gpui
```

### 9.4 Создание GPO

В ADMC: **Объекты групповой политики** → ПКМ на `office.ssa2026.region` → **Создать политику и связать с этим подразделением**

![Создание GPO](../images/gpo_create_menu.png)

Задать имя: `my-gpo`

![Имя GPO](../images/gpo_create_name.png)

### 9.5 Редактирование GPO

ПКМ на созданной политике → **Изменить**

![Редактирование GPO](../images/gpo_edit_menu.png)

---

## 10. Настройка политик

### 10.1 Политика фона рабочего стола

Путь: **Компьютер** → **Административные шаблоны** → **Система ALT** → **Настройки GNOME** → **Внешний вид** → **Фон рабочего стола**

- Путь до изображения: `file:///home/user/Изображения/picture.png`
- ☑ Блокировать настройку изображения

![Фон рабочего стола](../images/gpui_wallpaper.png)

### 10.2 Политика подгонки изображения

Путь: **Внешний вид** → **Подгонка изображения**

- Состояние: Включено
- Способ подгонки: Wallpaper

![Подгонка изображения](../images/gpui_wallpaper_fit.png)

### 10.3 Политика сетевых настроек

Путь: **Компьютер** → **Административные шаблоны** → **Система ALT** → **Правила Polkit** → **Ограничения NetworkManager**

Для всех параметров выставить:
- Состояние: Включено
- Опция: No
- ☑ Блокировать

![Политика NetworkManager](../images/gpui_network_policy.png)

---

## 11. Проверка применения политик

### 11.1 Перезагрузка рабочих станций

Перезагрузить cli1-a и cli2-a для применения политик.

### 11.2 Проверка фона рабочего стола

Фон рабочего стола должен быть установлен согласно политике:

![Результат - фон](../images/gpo_result_wallpaper.png)

### 11.3 Проверка сетевых ограничений

При попытке отключить сетевой интерфейс, данная возможность отсутствует:

![Результат - сеть](../images/gpo_result_network.png)

---

## Итоги

После выполнения данного модуля настроено:

| Компонент | Устройство | Статус |
|-----------|------------|--------|
| Samba AD DC | dc-a | ✅ |
| BIND DNS (BIND9_DLZ) | dc-a | ✅ |
| Kerberos | dc-a | ✅ |
| Ввод в домен | cli1-a | ✅ |
| Ввод в домен | cli2-a | ✅ |
| ADMC | cli1-a | ✅ |
| GPUI | cli1-a | ✅ |
| GPO | office.ssa2026.region | ✅ |

### Параметры домена

| Параметр | Значение |
|----------|----------|
| Realm | OFFICE.SSA2026.REGION |
| NetBIOS Domain | OFFICE |
| DNS Domain | office.ssa2026.region |
| DC Hostname | dc-a.office.ssa2026.region |
| DC IP | 172.20.10.10 |

### Организационная структура

```
office.ssa2026.region
├── Builtin
├── Computers
│   ├── CLI1-A
│   └── CLI2-A
├── Domain Controllers
├── ofadmins
│   ├── ofadmins (группа)
│   └── ofadmin1 (пользователь)
├── ofusers
│   ├── ofusers (группа)
│   └── ofuser1 (пользователь)
└── Users
    └── user1 (пользователь)
```

### Учётные записи

| Пользователь | Пароль | Группа | OU |
|--------------|--------|--------|-----|
| Administrator | P@ssw0rd | Domain Admins | Users |
| ofadmin1 | P@ssw0rd | ofadmins | ofadmins |
| ofuser1 | P@ssw0rd | ofusers | ofusers |
| user1 | P@ssw0rd | Domain Users | Users |

---

## Следующий модуль

➡️ [Модуль 16. ...](16-....md)
