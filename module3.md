# 📙 Модуль 3 — Эксплуатация сетевой инфраструктуры

> ⏱ **Время:** 1 час 30 мин | ⭐ **Баллы:** 24 | ℹ️ **Применяется:** только ДЭ ПУ

> ⚠️ Модули 1 и 2 должны быть выполнены!

[← README](../README.md) | [Модуль 2](module2.md)

---

## ⏰ Чек-лист

- [ ] Зад. 1 — IPSec/WireGuard VPN между HQ-RTR и BR-RTR
- [ ] Зад. 2 — Межсетевой экран iptables на роутерах
- [ ] Зад. 3 — Zabbix (мониторинг) на HQ-SRV
- [ ] Зад. 4 — rsyslog (централизованные логи) + logrotate
- [ ] Зад. 5 — CUPS (печать) на HQ-SRV
- [ ] Зад. 6 — Ansible playbook инвентаризации
- [ ] Зад. 7 — fail2ban на HQ-SRV
- [ ] Зад. 8 — Резервное копирование (Кибер Бэкап)

---

## Задание 1 — VPN: WireGuard site-to-site

> 📌 **Что делаем:** GRE-туннель уже настроен в Модуле 1. В Модуле 3 может быть задание настроить WireGuard VPN с шифрованием поверх GRE.

### На HQ-RTR

```bash
# Установить WireGuard:
apt-get install -y wireguard wireguard-tools

# Создать папку для ключей:
mkdir -p /etc/wireguard
chmod 700 /etc/wireguard

# Генерировать пару ключей:
wg genkey | tee /etc/wireguard/hq-private.key | wg pubkey > /etc/wireguard/hq-public.key
chmod 600 /etc/wireguard/hq-private.key

# Узнать ключи:
HQ_PRIVATE=$(cat /etc/wireguard/hq-private.key)
HQ_PUBLIC=$(cat /etc/wireguard/hq-public.key)
echo "HQ пуб. ключ = $HQ_PUBLIC"
# Скопируйте HQ_PUBLIC, он понадобится на BR-RTR
```

```bash
# Создать конфиг (ПОСЛЕ того, как узнаете BR_PUBLIC):
vim /etc/wireguard/wg0.conf
```

```ini
[Interface]
PrivateKey = <содержимое-файла-hq-private.key>
Address = 10.10.0.1/30
ListenPort = 51820
# Запуск/стоп интерфейса
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT

[Peer]
PublicKey = <BR_PUBLIC ключ>
AllowedIPs = 192.168.20.0/28, 10.10.0.2/32
Endpoint = 172.16.2.2:51820
PersistentKeepalive = 25
```

```bash
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

# Проверка:
wg show
```

### На BR-RTR

```bash
apt-get install -y wireguard wireguard-tools
mkdir -p /etc/wireguard
chmod 700 /etc/wireguard

wg genkey | tee /etc/wireguard/br-private.key | wg pubkey > /etc/wireguard/br-public.key
chmod 600 /etc/wireguard/br-private.key

BR_PUBLIC=$(cat /etc/wireguard/br-public.key)
echo "BR пуб. ключ = $BR_PUBLIC"
# Скопируйте BR_PUBLIC для HQ-RTR

vim /etc/wireguard/wg0.conf
```

```ini
[Interface]
PrivateKey = <содержимое-файла-br-private.key>
Address = 10.10.0.2/30
ListenPort = 51820
PostUp = iptables -A FORWARD -i wg0 -j ACCEPT; iptables -A FORWARD -o wg0 -j ACCEPT
PostDown = iptables -D FORWARD -i wg0 -j ACCEPT; iptables -D FORWARD -o wg0 -j ACCEPT

[Peer]
PublicKey = <HQ_PUBLIC ключ>
AllowedIPs = 192.168.100.0/27, 192.168.200.0/27, 10.10.0.1/32
Endpoint = 172.16.1.2:51820
PersistentKeepalive = 25
```

```bash
systemctl enable wg-quick@wg0
systemctl start wg-quick@wg0

# Проверка (с BR-RTR):
ping -c3 10.10.0.1  # пинг через WireGuard
ping -c3 192.168.100.2  # пинг HQ-SRV
```

---

## Задание 2 — Межсетевой экран (Firewall)

> 📌 **Что делаем:** Настраиваем iptables на роутерах по принципу "по умолчанию запрещать, нужное — разрешать".

> ⚠️ Важно! Не заблокируйте себе SSH до сохранения правил! Настраивайте в безопасном порядке.

```bash
# ==== На HQ-RTR (ПОСЛЕ настройки NAT!) ====

# 1. Сначала разрешить всё (на время настройки):
iptables -P INPUT ACCEPT
iptables -P FORWARD ACCEPT
iptables -P OUTPUT ACCEPT
iptables -F
iptables -t nat -F

# 2. Добавить правила разрешения:
# Разрешить established соединения
iptables -A INPUT -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT
iptables -A FORWARD -m conntrack --ctstate ESTABLISHED,RELATED -j ACCEPT

# Разрешить loopback
iptables -A INPUT -i lo -j ACCEPT

# Разрешить SSH через WAN
iptables -A INPUT -p tcp --dport 22 -j ACCEPT
iptables -A INPUT -p tcp --dport 2026 -j ACCEPT

# Разрешить OSPF через GRE-туннель
iptables -A INPUT -p gre -j ACCEPT

# Разрешить WireGuard:
iptables -A INPUT -p udp --dport 51820 -j ACCEPT

# Разрешить пересылку из локалки в WAN:
iptables -A FORWARD -i ens19 -o ens18 -j ACCEPT
iptables -A FORWARD -i ens19.100 -o ens18 -j ACCEPT
iptables -A FORWARD -i ens19.200 -o ens18 -j ACCEPT

# 3. После проверки запретить остальное:
iptables -P INPUT DROP
iptables -P FORWARD DROP

# 4. Вернуть NAT правила:
iptables -t nat -A POSTROUTING -o ens18 -j MASQUERADE

# Сохранить:
service iptables save

# Проверка — пинг с HQ-SRV должен работать:
# С HQ-SRV:
ping -c3 8.8.8.8
```

---

## Задание 3 — Zabbix мониторинг на HQ-SRV

> 📌 Используем Zabbix 6.x (в репозитории Альт есть заготовленный пакет). Обеспечивает наглядный мониторинг всех узлов.

```bash
# ==== На HQ-SRV ====

# Установить Zabbix-сервер + агент + веб-интерфейс:
apt-get install -y zabbix-server-mysql zabbix-agent
apt-get install -y zabbix-web-mysql
# Если названия отличаются:
apt-cache search zabbix

# Создать БД и пользователя
# (предполагаем что MariaDB установлен из Модуля 2):
mysql -u root << 'EOF'
CREATE DATABASE IF NOT EXISTS zabbix CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
CREATE USER IF NOT EXISTS 'zabbix'@'localhost' IDENTIFIED BY 'P@ssw0rd';
GRANT ALL PRIVILEGES ON zabbix.* TO 'zabbix'@'localhost';
FLUSH PRIVILEGES;
EOF

# Импорт схемы БД (найдите SQL файл):
find /usr/share -name "*.sql.gz" 2>/dev/null | grep zabbix
# Обычно: /usr/share/zabbix-sql-scripts/mysql/server.sql.gz
zcat /usr/share/zabbix-sql-scripts/mysql/server.sql.gz | mysql -uzabbix -pP@ssw0rd zabbix
```

```bash
# Настроить сервер:
vim /etc/zabbix/zabbix_server.conf
```

```
# Найдите и измените строки:
DBHost=localhost
DBName=zabbix
DBUser=zabbix
DBPassword=P@ssw0rd
```

```bash
systemctl enable zabbix-server
systemctl start zabbix-server
systemctl enable zabbix-agent
systemctl start zabbix-agent
systemctl restart httpd

# Проверка статуса:
systemctl status zabbix-server
tail -20 /var/log/zabbix/zabbix_server.log
```

### Настройка DNS-записи mon.au-team.irpo

```bash
# На HQ-SRV - добавить в /etc/bind/au-team.irpo.zone:
vim /etc/bind/au-team.irpo.zone
# Добавить строку:
# mon  IN  A  192.168.100.2

# Изменить serial (YYYYMMDDNN):
# 2026042202 -> 2026042203

systemctl restart named

# Проверка:
nslookup mon.au-team.irpo
```

### Установка агентов на всех узлах

```bash
# На каждом узле (HQ-CLI, BR-SRV, роутерах):
apt-get install -y zabbix-agent
vim /etc/zabbix/zabbix_agentd.conf
# Изменить:
# Server=192.168.100.2       <- IP HQ-SRV
# ServerActive=192.168.100.2
# Hostname=<имя узла>

systemctl enable zabbix-agent
systemctl start zabbix-agent
```

```
Доступ к веб-интерфейсу:
http://mon.au-team.irpo/zabbix
Логин: Admin
Пароль: zabbix
Добавьте узлы вручную через веб-интерфейс!
```

---

## Задание 4 — rsyslog + logrotate

> 📌 Централизованные логи: HQ-SRV принимает логи от всех узлов сети по UDP/TCP:514.

### Сервер логов на HQ-SRV

```bash
# ==== На HQ-SRV ====
apt-get install -y rsyslog

vim /etc/rsyslog.conf
```

Найдите и разкомментируйте (или добавьте в начало):

```
# Принимать по UDP:
module(load="imudp")
input(type="imudp" port="514")

# Принимать по TCP:
module(load="imtcp")
input(type="imtcp" port="514")

# Сохранять входящие логи по имени хоста:
$template RemoteLogs,"/opt/logs/%HOSTNAME%/%PROGRAMNAME%.log"
*.warn ?RemoteLogs
& stop
```

```bash
mkdir -p /opt/logs
chmod 755 /opt/logs

# Разрешить порт 514 в firewall:
iptables -A INPUT -p udp --dport 514 -j ACCEPT
iptables -A INPUT -p tcp --dport 514 -j ACCEPT

systemctl enable rsyslog
systemctl restart rsyslog

# Проверка (слушает ли 514 порт):
ss -ulnp | grep 514
ss -tlnp | grep 514
```

### Клиенты rsyslog

```bash
# ==== На HQ-RTR, BR-RTR, BR-SRV, HQ-CLI ====
apt-get install -y rsyslog

vim /etc/rsyslog.conf
# Добавить в конец файла:
*.warn   @192.168.100.2:514    # UDP (один @)
# Или TCP:
*.warn   @@192.168.100.2:514   # TCP (два @@)

systemctl restart rsyslog

# Проверка (слать тестовое сообщение):
logger -p user.warn "Тест rsyslog с $(hostname)"
# На HQ-SRV проверьте:
ls /opt/logs/
cat /opt/logs/hq-rtr.au-team.irpo/*.log
```

### logrotate на HQ-SRV

```bash
vim /etc/logrotate.d/remote-logs
```

```
/opt/logs/*/*.log {
    weekly          # поворачивать раз в неделю
    rotate 4        # хранить 4 архива
    compress        # сжать в gzip
    missingok       # не ошибка если файл не найден
    notifempty      # пропускать пустые файлы
    create 644 root root
    postrotate
        systemctl reload rsyslog 2>/dev/null || true
    endscript
}
```

```bash
# Тестовый запуск (debug режим):
logrotate -d /etc/logrotate.d/remote-logs
# Если всё ок, запустить:
logrotate -f /etc/logrotate.d/remote-logs
```

---

## Задание 5 — CUPS (сетевая печать)

> 📌 CUPS — сервер печати Linux. Настраиваем виртуальный PDF-принтер на HQ-SRV и подключаем HQ-CLI.

```bash
# ==== На HQ-SRV ====
apt-get install -y cups cups-pdf

# Настроить доступ к CUPS:
vim /etc/cups/cupsd.conf
```

Найдите и измените строки:

```
# Изменить:
Listen localhost:631
# На:
Port 631
Listen 0.0.0.0:631

# Добавить/изменить в блоках <Location>:
<Location />
  Order allow,deny
  Allow from 192.168.100.0/27
  Allow from 192.168.200.0/27
</Location>

<Location /admin>
  Order allow,deny
  Allow all
</Location>
```

```bash
systemctl enable cups
systemctl restart cups

# Разрешить порт 631:
iptables -A INPUT -s 192.168.100.0/27 -p tcp --dport 631 -j ACCEPT
iptables -A INPUT -s 192.168.200.0/27 -p tcp --dport 631 -j ACCEPT

# Добавить PDF-принтер через CLI:
lpadmin -p PDF -v cups-pdf:/ -m CUPS-PDF.ppd -E
lpadmin -d PDF  # сделать по умолчанию

# Проверка:
lpstat -p -d
```

```bash
# ==== На HQ-CLI ====
apt-get install -y cups cups-client

# Добавить принтер через CLI:
lpadmin -p HQ-PDF -v ipp://192.168.100.2:631/printers/PDF -m everywhere -E
# или через графический интерфейс GNOME/KDE:
# Устройства -> Принтеры -> Добавить -> Сетевой -> IPP

lpstat -p -d
```

---

## Задание 6 — Ansible Playbook (инвентаризация VC)

> 📌 Получаем информацию о узлах и сохраняем в YAML-файлы.

```bash
# ==== На BR-SRV ====

# Положить playbook.yml из Additional.iso:
mount /dev/sr0 /media/cdrom
cp /media/cdrom/ansible/playbook.yml /etc/ansible/

# Если нет — создайте ручно:
vim /etc/ansible/playbook.yml
```

```yaml
---
- name: Inventory nodes
  hosts: all
  gather_facts: yes
  tasks:
    - name: Collect system info
      shell: |
        echo "hostname: $(hostname -f)"
        echo "ip: $(hostname -I | tr -s ' ')"
        echo "os: $(cat /etc/altlinux-release 2>/dev/null || cat /etc/os-release | head -1)"
        echo "cpu_count: $(nproc)"
        echo "ram_mb: $(free -m | awk '/^Mem/{print $2}')"
      register: info

    - name: Save to PC-INFO directory
      copy:
        content: "{{ info.stdout }}\n"
        dest: "/etc/ansible/PC-INFO/{{ inventory_hostname }}.yml"
      delegate_to: localhost
```

```bash
mkdir -p /etc/ansible/PC-INFO

# Запустить:
ansible-playbook /etc/ansible/playbook.yml

# Проверка:
ls -la /etc/ansible/PC-INFO/
cat /etc/ansible/PC-INFO/hq-srv.au-team.irpo.yml
```

---

## Задание 7 — fail2ban на HQ-SRV

> 📌 fail2ban автоматически блокирует IP-адреса после N неудачных попыток входа.

```bash
# ==== На HQ-SRV ====
apt-get install -y fail2ban

# Создать локальный конфиг (jail.local переопределяет jail.conf):
vim /etc/fail2ban/jail.local
```

```ini
[DEFAULT]
# Время блокировки в секундах
bantime  = 60
# Временной окно для подсчёта попыток
findtime = 60
# Макс. попыток до блокировки
maxretry = 3

[sshd]
enabled  = true
port     = 2026
logpath  = /var/log/auth.log
# в Альт может быть:
# logpath = /var/log/secure
maxretry = 3
bantime  = 60
```

```bash
systemctl enable fail2ban
systemctl start fail2ban

# Проверка:
fail2ban-client status
fail2ban-client status sshd

# Тест: ввести 3 раза неверный пароль с другой машины:
ssh -p 2026 wronguser@192.168.100.2
# После 3 попыток IP должен быть заблокирован!

# Разблокировать IP:
fail2ban-client set sshd unbanip <IP>
```

---

## Задание 8 — Резервное копирование (Кибер Бэкап)

> 📌 Используем Kибер Бэкап. ISO-образ должен быть на Additional.iso или загружен заранее в Proxmox.

### HQ-SRV — сервер управления

```bash
# Подключить ISO с Кибер Бэкапом:
mkdir -p /media/kib
mount /dev/sr1 /media/kib    # или sr0 если адрес ISO другой
ls /media/kib/

# Установить пакет:
rpm -ivh /media/kib/kiberbackup-management-server-*.rpm
# или:
apt-get install -y kiberbackup-management-server

# Запустить сервер:
systemctl enable kiberbackup-management
systemctl start kiberbackup-management

# Доступ к веб-интерфейсу:
# http://192.168.100.2:9877
```

### Настройка через веб-интерфейс

```
1. Указать лицензию (если требуется)
2. Создать организацию: irpo
3. Создать администратора: irpoadmin / P@ssw0rd
```

### HQ-CLI — узел хранилища

```bash
# ==== На HQ-CLI ====

# Установить агент хранилища:
rpm -ivh /media/kib/kiberbackup-storage-node-*.rpm
# или:
apt-get install -y kiberbackup-storage-node

# Создать директорию хранения:
mkdir -p /backup
chown kiberbackup:kiberbackup /backup 2>/dev/null || chmod 777 /backup

# Добавить узел через веб-интерфейс HQ-SRV:
# http://192.168.100.2:9877
# Storage -> Add Node -> Указать IP HQ-CLI -> /backup
```

### Планы резервного копирования на HQ-SRV

```
Через веб-интерфейс:
1. Backup Plans -> Create
   - Объект: Files/Folders -> Добавить /etc
   - Storage: HQ-CLI -> /backup
   - Расписание: Дежурное (или вручное)
   -> Сохранить

2. Backup Plans -> Create
   - Объект: Databases -> MySQL/MariaDB -> webdb
   - Storage: HQ-CLI -> /backup
   - Расписание: Дежурное
   -> Сохранить

3. Для каждого плана: Actions -> Run Now
4. Проверить Activities -> статус Completed
```

---

## ✅ Конечная проверка модуля 3

```bash
# WireGuard:
wg show                       # на HQ-RTR / BR-RTR — peer connected
ping -c2 10.10.0.2            # пинг через VPN

# Firewall:
iptables -L -n -v             # политика DROP INPUT

# Zabbix:
http://mon.au-team.irpo/zabbix  # веб-интерфейс

# rsyslog:
logger -p user.warn "Тест"
ls /opt/logs/                 # папка с именем узла появилась

# fail2ban:
fail2ban-client status sshd   # активно

# Резервное копирование:
ls /backup/                   # на HQ-CLI — видны копии
```

---

[← Модуль 2](module2.md) | [Начало: README →](../README.md)
