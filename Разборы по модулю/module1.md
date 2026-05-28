# 📗 Модуль 1 — Настройка сетевой инфраструктуры

> ⏱ **Время:** 1 час | ℹ️ **Применяется:** ПА, ДЭ БУ, ДЭ ПУ | ⭐ **Баллы:** 25–27

[← README](../README.md) | [Модуль 2 →](module2.md)

---

## ⏰ Чек-лист по модулю

- [ ] Зад. 1 — hostname на всех 6 устройствах
- [ ] Зад. 2 — IP-адресация (VLSM) на ISP, HQ-RTR, BR-RTR, HQ-SRV, BR-SRV
- [ ] Зад. 3 — Пользователи sshuser + net_admin
- [ ] Зад. 4 — VLAN 100, 200, 999 на HQ-RTR (транкинг)
- [ ] Зад. 5 — SSH: порт 2026, баннер, MaxAuthTries 2
- [ ] Зад. 6 — GRE-туннель между HQ-RTR и BR-RTR
- [ ] Зад. 7 — OSPF (динамическая маршрутизация) через туннель
- [ ] Зад. 8 — NAT на HQ-RTR и BR-RTR
- [ ] Зад. 9 — DHCP для HQ-CLI
- [ ] Зад. 10 — DNS на HQ-SRV
- [ ] Зад. 11 — Часовой пояс

---

## Задание 1 — Установка hostname

> 📌 **Что делает эта команда:** Задаёт FQDN-имя машины (формат: `узел.домен`). Имя сразу записывается в `/etc/hostname` и применяется до следующей перезагрузки.

### Выполняем на каждой ВМ:

```bash
# ISP
hostnamectl set-hostname isp.au-team.irpo

# HQ-RTR
hostnamectl set-hostname hq-rtr.au-team.irpo

# BR-RTR
hostnamectl set-hostname br-rtr.au-team.irpo

# HQ-SRV
hostnamectl set-hostname hq-srv.au-team.irpo

# BR-SRV
hostnamectl set-hostname br-srv.au-team.irpo

# HQ-CLI
hostnamectl set-hostname hq-cli.au-team.irpo
```

### Проверка (на каждом)

```bash
hostname
# должно вывести: hq-rtr.au-team.irpo

# Дополнительно добавить в /etc/hosts для локального разрешения:
echo "127.0.1.1 hq-rtr.au-team.irpo hq-rtr" >> /etc/hosts
# (вместо hq-rtr — имя вашего узла)
```

---

## Задание 2 — IP-адресация (VLSM)

> 📌 **Что такое VLSM:** Variable Length Subnet Mask — разделение сети на подсети разных размеров. На экзамене вы сами выбираете адреса из RFC1918 и придумываете маски.

### Планировка адресного пространства

| Сегмент | Требуется хостов | Маска | Дост. адреса | Пример сети |
|---|---|---|---|---|
| ISP → HQ-RTR | 2 | /28 (14 хостов) | фикс. | 172.16.1.0/28 |
| ISP → BR-RTR | 2 | /28 | фикс. | 172.16.2.0/28 |
| HQ-SRV (VLAN100) | ≤32 | /27 (30 хостов) | 30 | 192.168.100.0/27 |
| HQ-CLI (VLAN200) | ≥32 | /27 | 30 | 192.168.200.0/27 |
| VLAN999 (mgmt) | ≤8 | /29 (6 хостов) | 6 | 192.168.99.0/29 |
| BR-SRV | ≤16 | /28 (14 хостов) | 14 | 192.168.20.0/28 |
| GRE-туннель | 2 | /30 | 2 | 10.0.0.0/30 |

### Настройка адресов в Альт Linux (через nmcli)

> ⚠️ В Альт Linux сеть настраивается через **nmcli** (не через `/etc/network/interfaces` и не через ip route save).

```bash
# Шаг 1: узнать имена интерфейсов (очень важно!)
ip link show
# Или:
nmcli con show
# Обычно eth0, eth1, eth2... в ALT JeOS
# Шаг 2: присвоить адрес
# (замените "ens18" на ваше имя интерфейса)
nmcli con mod "ens18" \
  ipv4.addresses 192.168.100.2/27 \
  ipv4.gateway 192.168.100.1 \
  ipv4.dns "192.168.100.2" \
  ipv4.method manual
nmcli con up "ens18"
```

### Настройка ISP — 3 интерфейса

```bash
# ==== На ISP ====
# eth0 (или ens18) — внешний, DHCP от провайдера (или в задании иногда стат. адрес)
nmcli con mod "ens18" ipv4.method auto
nmcli con up "ens18"

# eth1 (ens19) — сеть 172.16.1.0/28 (к HQ-RTR)
nmcli con mod "ens19" \
  ipv4.addresses 172.16.1.1/28 \
  ipv4.method manual
nmcli con up "ens19"

# eth2 (ens20) — сеть 172.16.2.0/28 (к BR-RTR)
nmcli con mod "ens20" \
  ipv4.addresses 172.16.2.1/28 \
  ipv4.method manual
nmcli con up "ens20"

# Проверка
ip a
```

### Настройка HQ-RTR — адрес WAN-интерфейса

```bash
# ==== На HQ-RTR ====
# eth0 (ens18) — в сторону ISP
nmcli con mod "ens18" \
  ipv4.addresses 172.16.1.2/28 \
  ipv4.gateway 172.16.1.1 \
  ipv4.method manual
nmcli con up "ens18"

# Проверка до ISP:
ping -c3 172.16.1.1
```

### Настройка BR-RTR

```bash
# ==== На BR-RTR ====
nmcli con mod "ens18" \
  ipv4.addresses 172.16.2.2/28 \
  ipv4.gateway 172.16.2.1 \
  ipv4.method manual
nmcli con up "ens18"

# eth1 (ens19) — в сторону BR-SRV
nmcli con mod "ens19" \
  ipv4.addresses 192.168.20.1/28 \
  ipv4.method manual
nmcli con up "ens19"

ping -c3 172.16.2.1
```

### Настройка HQ-SRV

```bash
# ==== На HQ-SRV ====
nmcli con mod "ens18" \
  ipv4.addresses 192.168.100.2/27 \
  ipv4.gateway 192.168.100.1 \
  ipv4.dns "127.0.0.1" \
  ipv4.method manual
nmcli con up "ens18"
```

### Настройка BR-SRV

```bash
# ==== На BR-SRV ====
nmcli con mod "ens18" \
  ipv4.addresses 192.168.20.2/28 \
  ipv4.gateway 192.168.20.1 \
  ipv4.method manual
nmcli con up "ens18"
```

---

## Задание 3 — Создание пользователей

> 📌 Пользователь **sshuser** — на серверах (HQ-SRV, BR-SRV). Пользователь **net_admin** — на маршрутизаторах (HQ-RTR, BR-RTR).

### sshuser на HQ-SRV и BR-SRV

```bash
# Создать пользователя с UID=2026 (-u), домашняя директория (-m), shell (-s)
useradd -u 2026 -m -s /bin/bash sshuser

# Установить пароль
echo "sshuser:P@ssw0rd" | chpasswd

# Дать права sudo без пароля через visudo:
visudo
# Добавить в конец файла (до строки #includedir):
# sshuser ALL=(ALL) NOPASSWD: ALL

# Проверка:
id sshuser
# вывод: uid=2026(sshuser) gid=2026(sshuser) groups=2026(sshuser)
```

### net_admin на HQ-RTR и BR-RTR

```bash
useradd -m -s /bin/bash net_admin
echo "net_admin:P@ssw0rd" | chpasswd
visudo
# Добавить:
# net_admin ALL=(ALL) NOPASSWD: ALL
```

---

## Задание 4 — VLAN (router-on-a-stick) на HQ-RTR

> 📌 **Что делаем:** eth1 (ens19) HQ-RTR — транк-порт к HQ-сети. На нём создаём VLAN-подинтерфейсы. В Proxmox на адаптере vmbr3 тэг не ставим — теги проходят через ОС.

```bash
# ==== На HQ-RTR ====

# Сначала убедитесь, что eth1 (или ens19) поднят:
ip link show ens19

# Создаём VLAN 100 (для HQ-SRV)
nmcli con add type vlan \
  con-name vlan100 \
  dev ens19 \
  id 100 \
  ipv4.addresses 192.168.100.1/27 \
  ipv4.method manual
nmcli con up vlan100

# Создаём VLAN 200 (для HQ-CLI, DHCP-сервер)
nmcli con add type vlan \
  con-name vlan200 \
  dev ens19 \
  id 200 \
  ipv4.addresses 192.168.200.1/27 \
  ipv4.method manual
nmcli con up vlan200

# Создаём VLAN 999 (управление)
nmcli con add type vlan \
  con-name vlan999 \
  dev ens19 \
  id 999 \
  ipv4.addresses 192.168.99.1/29 \
  ipv4.method manual
nmcli con up vlan999

# Проверка:
ip a show ens19.100
ip a show ens19.200
ip a show ens19.999
```

### Настройка HQ-SRV для работы через VLAN 100

```bash
# ==== На HQ-SRV ====
# HQ-SRV подключён напрямую к vmbr3 в Proxmox
# Никаких VLAN-настроек на нём нет — он заходит в VLAN100 через HQ-RTR
# HQ-SRV видит только разтегированный траффик VLAN100 со стороны HQ-RTR
# В Proxmox: VLAN Tag = 100 на адаптере HQ-SRV -> vmbr3
# Или (если HQ-SRV на vmbr3 без тэга, а HQ-RTR делает разтегирование):
nmcli con mod "ens18" \
  ipv4.addresses 192.168.100.2/27 \
  ipv4.gateway 192.168.100.1 \
  ipv4.method manual
nmcli con up "ens18"
```

---

## Задание 5 — SSH на HQ-SRV и BR-SRV

> 📌 Требуется: порт 2026, баннер "Аутхоризован доступ только для авторизованных", макс. 2 попытки.

```bash
# ==== На HQ-SRV и BR-SRV ====

# Открыть конфиг:
vim /etc/openssh/sshd_config
# (в Альт путь именно /etc/openssh/sshd_config, а не /etc/ssh/)
```

Найти и изменить строки (или добавить, если нет):

```
Port 2026
AllowUsers sshuser
MaxAuthTries 2
Banner /etc/openssh/banner
```

```bash
# Создать файл баннера
echo "Authorized access only" > /etc/openssh/banner

# Перезапустить SSH (в Альт служба называется sshd)
systemctl restart sshd

# Добавить в автозапуск
systemctl enable sshd

# Проверка с другой машины:
ssh -p 2026 sshuser@192.168.100.2
# Должен появиться баннер: Authorized access only
```

---

## Задание 6 — GRE-туннель HQ-RTR ↔ BR-RTR

> 📌 **Что такое GRE:** Generic Routing Encapsulation — пакует IP-пакеты внутрь других IP-пакетов. Создаёт виртуальный канал между двумя роутерами через сеть ISP.

```bash
# ==== На HQ-RTR ====

# Через nmcli (автозапуск заботится сам):
nmcli con add type ip-tunnel \
  con-name gre1 \
  ifname gre1 \
  mode gre \
  remote 172.16.2.2 \
  local 172.16.1.2
nmcli con mod gre1 \
  ipv4.addresses 10.0.0.1/30 \
  ipv4.method manual
nmcli con up gre1

# Проверка:
ip a show gre1
# Должна быть адрес: 10.0.0.1/30
```

```bash
# ==== На BR-RTR ====
nmcli con add type ip-tunnel \
  con-name gre1 \
  ifname gre1 \
  mode gre \
  remote 172.16.1.2 \
  local 172.16.2.2
nmcli con mod gre1 \
  ipv4.addresses 10.0.0.2/30 \
  ipv4.method manual
nmcli con up gre1

# Проверка (с BR-RTR до HQ-RTR):
ping -c3 10.0.0.1
# Должны быть ответы!
```

---

## Задание 7 — OSPF (FRRouting)

> 📌 **Что такое OSPF:** протокол динамической маршрутизации. Через GRE-туннель HQ-RTR и BR-RTR обменяются таблицами маршрутов и знают друг о друге.

```bash
# ==== На HQ-RTR и BR-RTR ====

# Установить FRRouting
apt-get install -y frr

# Включить демон OSPF:
sed -i 's/ospfd=no/ospfd=yes/' /etc/frr/daemons
systemctl restart frr
systemctl enable frr

# Проверка, что FRR запустился:
systemctl status frr
vtysh -c "show version"
```

### Настройка OSPF на HQ-RTR

```bash
# Входим в интерактивный режим vtysh:
vtysh
```

```
! Далее вводите в режиме vtysh (# = символ комментария):
configure terminal
!
! Router-ID = IP-адрес loopback (уникальный номер для процесса)
router ospf
  ospf router-id 1.1.1.1
  !
  ! Анонсируем только сеть туннеля в area 0:
  network 10.0.0.0/30 area 0
  !
  ! Рассылаем подключённые сети (включая VLAN100/200/999 и BR-сеть):
  redistribute connected
  !
  ! Отключаем passive для всех кроме туннеля:
  passive-interface default
  no passive-interface gre1
!
! Пароль на OSPF на туннельном интерфейсе:
interface gre1
  ip ospf authentication message-digest
  ip ospf message-digest-key 1 md5 P@ssw0rd
end
write memory
```

### Настройка OSPF на BR-RTR

```bash
vtysh
```

```
configure terminal
router ospf
  ospf router-id 2.2.2.2
  network 10.0.0.0/30 area 0
  redistribute connected
  passive-interface default
  no passive-interface gre1
!
interface gre1
  ip ospf authentication message-digest
  ip ospf message-digest-key 1 md5 P@ssw0rd
end
write memory
```

```bash
# Проверка (дождитесь ~30 секунд и проверьте):
vtysh -c "show ip ospf neighbor"
# Должен быть сосед со статусом Full

vtysh -c "show ip route ospf"
# Должны быть видны сети другой стороны

# Пинг сети другого роутера (с HQ-RTR до BR):
ping -c3 192.168.20.2
```

---

## Задание 8 — NAT (выход в интернет) на ISP, HQ-RTR, BR-RTR

> 📌 Включить IP-форвардинг и NAT MASQUERADE.

```bash
# ==== На ISP, HQ-RTR, BR-RTR ====

# Шаг 1: включить форвардинг (передача пакетов)
echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p
# Проверка:
cat /proc/sys/net/ipv4/ip_forward
# Должно вывести: 1

# Шаг 2: правило NAT
# Замените ens18 на имя WAN-интерфейса (к ISP)
iptables -t nat -A POSTROUTING -o ens18 -j MASQUERADE

# Проверка правила:
iptables -t nat -L POSTROUTING -n -v

# Шаг 3: сохранить правила навсегда
apt-get install -y iptables-service
service iptables save
systemctl enable iptables
```

---

## Задание 9 — DHCP-сервер для HQ-CLI

> 📌 DHCP-сервер настраивается на HQ-RTR. Он выдаёт IP клиентам из VLAN200 (в нашем случае HQ-CLI).

```bash
# ==== На HQ-RTR ====
apt-get install -y dhcp-server

# Основной конфиг:
vim /etc/dhcp/dhcpd.conf
```

```
# Объявляем подсеть VLAN200
subnet 192.168.200.0 netmask 255.255.255.224 {
    range 192.168.200.10 192.168.200.30;  # диапазон выдачи
    option routers 192.168.200.1;         # шлюз = VLAN200 HQ-RTR
    option domain-name-servers 192.168.100.2;  # DNS = HQ-SRV
    option domain-name "au-team.irpo";
    default-lease-time 600;
    max-lease-time 7200;
}
```

```bash
# Указать, на каком интерфейсе слушать DHCP:
vim /etc/sysconfig/dhcpd
# Найти строку DHCPDv4_ARGS и изменить:
# DHCPDv4_ARGS="ens19.200"
# (где ens19.200 = VLAN200 на trunk-интерфейсе)

systemctl enable dhcpd
systemctl start dhcpd

# Проверка на HQ-CLI (DHCP-клиент):
# Убедитесь, что HQ-CLI в настройках Proxmox подключён к vmbr3 с VLAN Tag = 200
nmcli con mod "ens18" ipv4.method auto
nmcli con up "ens18"
ip a
# Должен получить адрес из диапазона 192.168.200.10-30
```

---

## Задание 10 — DNS-сервер (BIND9) на HQ-SRV

> 📌 DNS разрешает имена в IP-адреса и наоборот. Требуется зона au-team.irpo + обратная зона + forwarder на внешний DNS.

```bash
# ==== На HQ-SRV ====
apt-get install -y bind
systemctl enable named
```

```bash
# Главный конфиг:
vim /etc/bind/named.conf
```

```
options {
    directory "/var/bind";
    listen-on { any; };         // слушать на всех интерфейсах
    allow-query { any; };       // отвечать всем
    recursion yes;
    forwarders { 77.88.8.7; 77.88.8.3; };  // внешние DNS (Яндекс)
    forward first;
};

zone "au-team.irpo" IN {
    type master;
    file "/etc/bind/au-team.irpo.zone";
};

zone "100.168.192.in-addr.arpa" IN {
    type master;
    file "/etc/bind/100.168.192.rev";
};
```

```bash
# Файл прямой зоны:
vim /etc/bind/au-team.irpo.zone
```

```
$TTL 86400
@   IN SOA hq-srv.au-team.irpo. admin.au-team.irpo. (
        2026042201 ; Serial (YYYYMMDDNN)
        3600       ; Refresh
        1800       ; Retry
        604800     ; Expire
        86400 )    ; Minimum TTL

; Сервер имён
@       IN  NS  hq-srv.au-team.irpo.

; A-записи (необходимо указывать IP вашего HQ-SRV)
hq-rtr  IN  A   192.168.100.1
br-rtr  IN  A   192.168.20.1
hq-srv  IN  A   192.168.100.2
hq-cli  IN  A   192.168.200.10  ; или IP полученный по DHCP
br-srv  IN  A   192.168.20.2

; ISP-адреса (для веб-сервисов на nginx)
docker  IN  A   172.16.1.1
web     IN  A   172.16.2.1
```

```bash
# Обратная зона:
vim /etc/bind/100.168.192.rev
```

```
$TTL 86400
@   IN SOA hq-srv.au-team.irpo. admin.au-team.irpo. (
        2026042201 3600 1800 604800 86400 )

@   IN  NS   hq-srv.au-team.irpo.
1   IN  PTR  hq-rtr.au-team.irpo.    ; 192.168.100.1
2   IN  PTR  hq-srv.au-team.irpo.    ; 192.168.100.2
```

```bash
# Проверить конфиг на ошибки:
named-checkconf /etc/bind/named.conf
named-checkzone au-team.irpo /etc/bind/au-team.irpo.zone

systemctl restart named

# Тестовые запросы:
nslookup hq-srv.au-team.irpo 127.0.0.1
nslookup 192.168.100.2 127.0.0.1
dig hq-rtr.au-team.irpo @127.0.0.1
```

---

## Задание 11 — Часовой пояс

```bash
# Выбор зоны зависит от города проведения экзамена!
# Спросите эксперта заранее.

# Примеры:
timedatectl set-timezone Europe/Moscow       # UTC+3 Москва
timedatectl set-timezone Asia/Yekaterinburg  # UTC+5 Екатеринбург
timedatectl set-timezone Asia/Novosibirsk    # UTC+7 Новосибирск
timedatectl set-timezone Asia/Irkutsk        # UTC+8 Иркутск
timedatectl set-timezone Asia/Vladivostok    # UTC+10 Владивосток

# Проверка:
timedatectl status
# Должна быть строка Time zone: Asia/Vladivostok (VLAT, +1000)
```

---

## ✅ Конечная проверка модуля 1

```bash
# С HQ-CLI проверяем всё:
# 1. Получен ли IP по DHCP
ip a

# 2. Доступность шлюзов и серверов:
ping -c2 192.168.100.1   # HQ-RTR VLAN100
ping -c2 192.168.100.2   # HQ-SRV
ping -c2 192.168.20.2    # BR-SRV (через OSPF)
ping -c2 8.8.8.8          # Интернет (через NAT)

# 3. Разрешение имён:
nslookup hq-srv.au-team.irpo
nslookup br-srv.au-team.irpo

# 4. SSH на сервера:
ssh -p 2026 sshuser@192.168.100.2
# Должен вывести баннер "Authorized access only"
```

---

[← README](../README.md) | [Далее: Модуль 2 →](module2.md)
