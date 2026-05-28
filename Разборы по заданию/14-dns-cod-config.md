# Модуль 14. Настройка службы доменных имен в COD

## Описание

Данный модуль описывает настройку DNS-сервера BIND на srv1-cod для зоны `cod.ssa2026.region` с поддержкой прямого и обратного разрешения имён, а также настройку DNS-клиентов на остальных устройствах COD.

## Задачи

- Установка и настройка BIND на srv1-cod
- Создание зоны прямого просмотра `cod.ssa2026.region`
- Создание зоны обратного просмотра `168.192.in-addr.arpa`
- Настройка пересылки запросов к ISP и офису A
- Настройка DNS-клиентов на устройствах COD

---

## 1. Настройка DNS-сервера (srv1-cod)

### 1.1 Установка BIND

```bash
apt-get install -y bind bind-utils
```

### 1.2 Настройка options.conf

Редактируем конфигурационный файл `/etc/bind/options.conf`:

```bash
vim /etc/bind/options.conf
```

Основные параметры:

- **listen-on { any; }** — слушать на всех интерфейсах
- **listen-on-v6 { none; }** — отключить IPv6
- **forward first** — сначала пытаться переслать запрос
- **forwarders { 100.100.100.100; }** — пересылка на ISP
- **allow-query { any; }** — разрешить запросы от всех
- **allow-query-cache { any; }** — разрешить кэширование для всех
- **allow-recursion { any; }** — разрешить рекурсию для всех

![Настройка options.conf](../images/dns_cod_options.png)

### 1.3 Настройка зон в rfc1912.local

Добавить в конфигурационный файл `/etc/bind/rfc1912.local` информацию о файлах зон прямого и обратного просмотра:

```bash
vim /etc/bind/rfc1912.local
```

```
zone "cod.ssa2026.region" {
    type master;
    file "cod.ssa2026.region";
    allow-transfer { 172.20.10.10; };
};

zone "168.192.in-addr.arpa" {
    type master;
    file "168.192.in-addr.arpa";
    allow-transfer { 172.20.10.10; };
};

zone "office.ssa2026.region" {
    type forward;
    forward only;
    forwarders { 172.20.10.10; };
};

zone "20.172.in-addr.arpa" {
    type forward;
    forward only;
    forwarders { 172.20.10.10; };
};
```

![Настройка зон](../images/dns_cod_zones.png)

> ⚠️ **Примечание:** 
> - `allow-transfer { 172.20.10.10; }` — разрешает трансфер зоны на dc-a
> - Зоны `office.ssa2026.region` и `20.172.in-addr.arpa` настроены как forward для пересылки запросов к офису A

### 1.4 Создание зоны прямого просмотра

Скопировать файл шаблона:

```bash
cp /etc/bind/zone/localhost /etc/bind/zone/cod.ssa2026.region
```

Выдать права:

```bash
chown root:named /etc/bind/zone/cod.ssa2026.region
```

Редактируем файл `/etc/bind/zone/cod.ssa2026.region`:

```bash
vim /etc/bind/zone/cod.ssa2026.region
```

Содержимое файла зоны прямого просмотра:

```
$TTL    1D
@       IN      SOA     cod.ssa2026.region. root.cod.ssa2026.region. (
                        2025110500      ; serial
                        12H             ; refresh
                        1H              ; retry
                        1W              ; expire
                        1H              ; ncache
                        )

        IN      NS      cod.ssa2026.region.

fw-cod          IN      A       192.168.10.254
sw1-cod         IN      A       192.168.30.1
sw2-cod         IN      A       192.168.30.2
cli-cod         IN      A       192.168.40.40
srv1-cod        IN      A       192.168.10.1
srv2-cod        IN      A       192.168.10.2
sip-cod         IN      A       192.168.50.50
admin-cod       IN      A       192.168.30.30
```

### 1.5 Создание зоны обратного просмотра

Скопировать файл шаблона:

```bash
cp /etc/bind/zone/localhost /etc/bind/zone/168.192.in-addr.arpa
```

Выдать права:

```bash
chown root:named /etc/bind/zone/168.192.in-addr.arpa
```

Редактируем файл `/etc/bind/zone/168.192.in-addr.arpa`:

```bash
vim /etc/bind/zone/168.192.in-addr.arpa
```

Содержимое файла зоны обратного просмотра:

```
$TTL    1D
@       IN      SOA     cod.ssa2026.region. root.cod.ssa2026.region. (
                        2025110500      ; serial
                        12H             ; refresh
                        1H              ; retry
                        1W              ; expire
                        1H              ; ncache
                        )

        IN      NS      cod.ssa2026.region.

254.10  IN      PTR     fw-cod.cod.ssa2026.region.
1.30    IN      PTR     sw1-cod.cod.ssa2026.region.
2.30    IN      PTR     sw2-cod.cod.ssa2026.region.
40.40   IN      PTR     cli-cod.cod.ssa2026.region.
1.10    IN      PTR     srv1-cod.cod.ssa2026.region.
2.10    IN      PTR     srv2-cod.cod.ssa2026.region.
50.50   IN      PTR     sip-cod.cod.ssa2026.region.
30.30   IN      PTR     admin-cod.cod.ssa2026.region.
```

![Зона обратного просмотра](../images/dns_cod_reverse_zone.png)

### 1.6 Запуск службы BIND

```bash
systemctl enable --now bind
```

### 1.7 Настройка DNS-клиента на srv1-cod

```bash
cat <<EOF > /etc/net/ifaces/ens19/resolv.conf
search cod.ssa2026.region
nameserver 127.0.0.1
EOF
```

### 1.8 Перезагрузка

```bash
reboot
```

### 1.9 Проверка записей типа A

```bash
host fw-cod
host sw1-cod
host sw2-cod
host cli-cod
host srv1-cod
host srv2-cod
host sip-cod
host admin-cod
```

![Проверка записей A](../images/dns_cod_check_a.png)

### 1.10 Проверка записей типа PTR

```bash
host 192.168.10.254
host 192.168.30.1
host 192.168.30.2
host 192.168.40.40
host 192.168.10.1
host 192.168.10.2
host 192.168.50.50
host 192.168.30.30
```

![Проверка записей PTR](../images/dns_cod_check_ptr.png)

---

## 2. Настройка DNS-клиентов

### 2.1 sw1-cod и sw2-cod (ALT Server)

Задаём в качестве DNS-сервера srv1-cod:

```bash
cat <<EOF > /etc/net/ifaces/mgmt-cod/resolv.conf
search cod.ssa2026.region
nameserver 192.168.10.1
EOF
```

Перезагружаем службу network:

```bash
systemctl restart network
```

Проверка:

```bash
cat /etc/resolv.conf
ping -c3 cod.ssa2026.region
ping -c3 ya.ru
```

![Проверка DNS на sw1-cod](../images/dns_cod_sw1_check.png)

### 2.2 srv2-cod (ALT Server)

Задаём в качестве DNS-сервера srv1-cod:

```bash
cat <<EOF > /etc/net/ifaces/ens20/resolv.conf
search cod.ssa2026.region
nameserver 192.168.10.1
EOF
```

Перезагружаем службу network:

```bash
systemctl restart network
```

Проверка:

```bash
cat /etc/resolv.conf
ping -c3 cod.ssa2026.region
ping -c3 ya.ru
```

![Проверка DNS на srv2-cod](../images/dns_cod_srv2_check.png)

### 2.3 Остальные устройства COD

Аналогичным образом настраиваются DNS-клиенты на:

| Устройство | Интерфейс | DNS-сервер |
|------------|-----------|------------|
| cli-cod | ens19 (или соответствующий) | 192.168.10.1 |
| admin-cod | ens19 (или соответствующий) | 192.168.10.1 |
| sip-cod | eth0 | 192.168.10.1 |

---

## Итоги

После выполнения данного модуля настроено:

| Компонент | Устройство | Статус |
|-----------|------------|--------|
| DNS-сервер BIND | srv1-cod | ✅ |
| Зона прямого просмотра | cod.ssa2026.region | ✅ |
| Зона обратного просмотра | 168.192.in-addr.arpa | ✅ |
| Пересылка на ISP | 100.100.100.100 | ✅ |
| Пересылка на офис A | 172.20.10.10 | ✅ |
| DNS-клиент | srv1-cod | ✅ |
| DNS-клиент | srv2-cod | ✅ |
| DNS-клиент | sw1-cod | ✅ |
| DNS-клиент | sw2-cod | ✅ |

### DNS-записи зоны cod.ssa2026.region

| Имя | Тип | Значение |
|-----|-----|----------|
| fw-cod | A | 192.168.10.254 |
| sw1-cod | A | 192.168.30.1 |
| sw2-cod | A | 192.168.30.2 |
| cli-cod | A | 192.168.40.40 |
| srv1-cod | A | 192.168.10.1 |
| srv2-cod | A | 192.168.10.2 |
| sip-cod | A | 192.168.50.50 |
| admin-cod | A | 192.168.30.30 |

### Пересылка DNS-запросов

| Зона | Направление | Сервер |
|------|-------------|--------|
| Интернет (по умолчанию) | → | 100.100.100.100 (ISP) |
| office.ssa2026.region | → | 172.20.10.10 (dc-a) |
| 20.172.in-addr.arpa | → | 172.20.10.10 (dc-a) |

---

## Следующий модуль

➡️ [Модуль 15. ...](15-....md)
