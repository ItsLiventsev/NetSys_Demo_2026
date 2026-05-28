# 📘 Модуль 2 — Организация сетевого администрирования

> ⏱ **Время:** 1 час 30 мин | ⭐ **Баллы:** 24 | ℹ️ **Применяется:** ДЭ БУ + ДЭ ПУ

> ⚠️ Модуль 1 должен быть полностью выполнен до начала этого!

[← README](../README.md) | [Модуль 1](module1.md) | [Модуль 3 →](module3.md)

---

## ⏰ Чек-лист

- [ ] Зад. 1 — Samba AD DC на BR-SRV
- [ ] Зад. 2 — RAID0 на HQ-SRV (+2 диска в Proxmox)
- [ ] Зад. 3 — NFS-сервер на HQ-SRV + autofs на HQ-CLI
- [ ] Зад. 4 — NTP chrony ISP аs сервер, остальные — клиенты
- [ ] Зад. 5 — Ansible на BR-SRV
- [ ] Зад. 6 — Docker на BR-SRV
- [ ] Зад. 7 — Apache + MariaDB на HQ-SRV
- [ ] Зад. 8 — Port forwarding на HQ-RTR и BR-RTR
- [ ] Зад. 9-10 — nginx reverse proxy + HTTP auth на ISP
- [ ] Зад. 11 — Яндекс Браузер на HQ-CLI

---

## Задание 1 — Samba AD Domain Controller на BR-SRV

> 📌 **Что делаем:** Настраиваем BR-SRV как контроллер домена Active Directory с внутренним DNS. HQ-CLI потом вводится в этот домен.

### Требуемые пакеты в Альт Linux

```bash
# ==== На BR-SRV ====

# Samba в Альт может содержаться в разных пакетах.
# Проверьте наличие:
apt-cache search samba
# Ожидаем пакеты: task-samba-dc или samba-common samba samba-winbind

# Установить полный набор DC:
apt-get install -y task-samba-dc
# или пораздельно:
apt-get install -y samba samba-dc winbind krb5-workstation
```

### Подготовка системы

```bash
# Остановить службы перед провизионированием:
systemctl stop samba smbd nmbd winbind 2>/dev/null

# Очистить старую конфигурацию Samba:
mv /etc/samba/smb.conf /etc/samba/smb.conf.bak 2>/dev/null
rm -rf /var/lib/samba/private/* 2>/dev/null

# Установить FQDN-имя BR-SRV:
hostnamectl set-hostname br-srv.au-team.irpo

# Установить часовой пояс (важно для Kerberos!):
timedatectl set-timezone Europe/Moscow
```

### Провизионирование AD DC

```bash
samba-tool domain provision \
  --realm=AU-TEAM.IRPO \
  --domain=AU-TEAM \
  --adminpass='P@ssw0rd' \
  --dns-backend=SAMBA_INTERNAL \
  --server-role=dc \
  --use-rfc2307 \
  --interactive
# На вопросы нажмите Enter (оставить по умолчанию)
```

### Настройка DNS для BR-SRV

```bash
# BR-SRV теперь сам DNS-сервер— указываем на себя
cat > /etc/resolv.conf << EOF
domain au-team.irpo
search au-team.irpo
nameserver 127.0.0.1
EOF

# Защитить файл от изменений NetworkManager:
chattr +i /etc/resolv.conf
```

### Запуск Samba AD

```bash
# В Альт служба называется просто samba
systemctl unmask samba
systemctl enable samba
systemctl start samba

# Проверка:
samba-tool domain info 127.0.0.1
# Должно вывести инфо о домене au-team.irpo

# Проверка DNS:
host -t A au-team.irpo 127.0.0.1
# Должен вернуть IP адрес BR-SRV
```

### Создание пользователей и группы

```bash
# Создать 5 пользователей
for i in 1 2 3 4 5; do
  samba-tool user create hquser$i P@ssw0rd \
    --given-name="HQ User $i" \
    --surname="$i"
done

# Создать группу
samba-tool group add hq

# Добавить всех пользователей в группу
for i in 1 2 3 4 5; do
  samba-tool group addmembers hq hquser$i
done

# Проверка:
samba-tool user list
samba-tool group listmembers hq
```

### Ввод HQ-CLI в домен

```bash
# ==== На HQ-CLI ====

# Добавить DNS-адрес BR-SRV для разрешения домена:
nmcli con mod "ens18" ipv4.dns "192.168.20.2"
# (IP-адрес BR-SRV)
nmcli con up "ens18"

# Проверка разрешения:
nslookup au-team.irpo
# Должен вернуть IP BR-SRV

# Установить необходимые пакеты:
apt-get install -y sssd sssd-ad adcli realmd samba-common-tools

# Ввести в домен (рекомендуется через realm):
realm join --user=Administrator au-team.irpo
# Введите пароль Administrator: P@ssw0rd

# После вхождения:
systemctl enable sssd
systemctl start sssd

# Проверка:
getent passwd hquser1
# Должно вывести запись пользователя
```

### Права sudo для группы hq через visudo

```bash
# На HQ-CLI:
visudo
# Добавить строку в конец:
%hq ALL=(ALL) NOPASSWD:/usr/bin/cat,/usr/bin/grep,/usr/bin/id

# Проверка под доменным пользователем:
su - hquser1
sudo cat /etc/passwd
# Должно выполниться без запроса пароля
```

---

## Задание 2 — RAID0 на HQ-SRV

> 📌 **RAID0 — что это:** данные разбиваются на 2 диска (страйпинг). Максимальная скорость, но нет избыточности. Если один диск сломается — данные теряются.

### Подготовка: добавить диски в Proxmox

1. В интерфейсе Proxmox выберите ВМ HQ-SRV
2. Перейдите в вкладку **Hardware**
3. Нажмите **Add** → **Hard Disk**
4. Добавьте 2 диска по 5 ГБ (можно меньше по условию задания)

### Создание RAID на ALT Linux

```bash
# ==== На HQ-SRV ====

# Убедитесь, что диски видны:
lsblk
# Ожидаем:
# sda - системный диск
# sdb, sdc - новые для RAID

# Установить mdadm:
apt-get install -y mdadm

# Создать RAID0 (вы увидите предупреждение — нажмите y):
mdadm --create /dev/md0 \
  --level=0 \
  --raid-devices=2 \
  /dev/sdb /dev/sdc
# Подтвердить: y

# Сохранить конфиг в файл (чтобы переживало перезагрузку):
mdadm --detail --scan | tee -a /etc/mdadm.conf

# Сформатировать RAID-устройство в ext4:
mkfs.ext4 /dev/md0

# Создать точку монтирования:
mkdir -p /raid

# Добавить автомонтирование:
echo "/dev/md0   /raid   ext4   defaults   0 0" >> /etc/fstab
mount -a

# Проверка:
df -h /raid
# Должно показать размер ~10ГБ (сумма двух дисков)

cat /proc/mdstat
# Должно показать md0 : active raid0 sdb sdc
```

---

## Задание 3 — NFS на HQ-SRV + автомонтирование на HQ-CLI

> 📌 **NFS** (Network File System) — сетевая файловая система. HQ-CLI будет автоматически монтировать папку с HQ-SRV при обращении.

### NFS-сервер на HQ-SRV

```bash
# ==== На HQ-SRV ====
apt-get install -y nfs-utils

# Создать общую папку на RAID:
mkdir -p /raid/nfs
chown nobody:nogroup /raid/nfs
chmod 777 /raid/nfs

# Описать експорт:
vim /etc/exports
```

```
# Формат: <папка> <сеть/хост>(<опции>)
/raid/nfs  192.168.200.0/27(rw,sync,no_subtree_check,no_root_squash)
```

```bash
# Применить экспорты:
exportfs -arv
# Вывод: exporting 192.168.200.0/27:/raid/nfs

systemctl enable nfs-server
systemctl start nfs-server

# Разрешить NFS в firewall (если есть):
iptables -A INPUT -s 192.168.200.0/27 -p tcp -m multiport --dports 111,2049 -j ACCEPT
iptables -A INPUT -s 192.168.200.0/27 -p udp -m multiport --dports 111,2049 -j ACCEPT

# Проверка:
showmount -e localhost
```

### Autofs на HQ-CLI

```bash
# ==== На HQ-CLI ====
apt-get install -y nfs-utils autofs

# Настроить главный конфиг:
vim /etc/auto.master
# Добавить строку:
/mnt/nfs  /etc/auto.nfs  --timeout=60

# Создать карту автомонтирования:
vim /etc/auto.nfs
# Добавить:
# nfs — это подпапка в /mnt/nfs/nfs
shared   -fstype=nfs4,rw   192.168.100.2:/raid/nfs
# (192.168.100.2 = IP HQ-SRV)

# Создать точку монтирования:
mkdir -p /mnt/nfs

systemctl enable autofs
systemctl start autofs

# Проверка — обращение триггерит монтирование:
ls /mnt/nfs/shared
df -h
# Должно показать NFS-монтирование
```

---

## Задание 4 — NTP chrony (ISP — сервер, все остальные — клиенты)

> 📌 NTP синхронизирует время на всех узлах. Важно для Kerberos/AD, логов и сертификатов.

```bash
# ==== На ISP (сервер NTP) ====
apt-get install -y chrony
vim /etc/chrony.conf
```

```
# Внешний NTP-сервер
pool ntp.ru iburst
pool 0.ru.pool.ntp.org iburst

# ISP будет stratum 5 если нет внешнего NTP:
local stratum 5

# Разрешить отвечать всем клиентам:
allow all

# Не слушать самого себя:
bindaddress 0.0.0.0
```

```bash
systemctl enable chronyd
systemctl restart chronyd

# Проверка состояния:
chronyc sources -v
chronyc tracking
# Должно показать Reference ID и Stratum
```

### NTP-клиенты (HQ-RTR, BR-RTR, HQ-SRV, BR-SRV, HQ-CLI)

```bash
# ==== На каждом клиенте ====
apt-get install -y chrony
vim /etc/chrony.conf
# Найти и заскомментировать строку pool ....
# Добавить:
server 172.16.1.1 iburst
# (172.16.1.1 = IP ISP)

systemctl enable chronyd
systemctl restart chronyd

# Проверка (ждите ~30 секунд):
chronyc sources -v
# ^* 172.16.1.1 — значок * = активный источник
```

---

## Задание 5 — Ansible на BR-SRV

> 📌 Ansible позволяет управлять удалёнными узлами через SSH без агентов.

```bash
# ==== На BR-SRV ====
apt-get install -y ansible

# Создать каталог для отчётов:
mkdir -p /etc/ansible/PC-INFO
```

```bash
# Файл конфигурации:
vim /etc/ansible/ansible.cfg
```

```ini
[defaults]
inventory      = /etc/ansible/hosts
host_key_checking = False
remote_user    = sshuser
private_key_file = /root/.ssh/id_rsa
```

```bash
# Файл инвентаря:
vim /etc/ansible/hosts
```

```ini
[all]
hq-rtr.au-team.irpo  ansible_user=net_admin  ansible_port=22
hq-srv.au-team.irpo  ansible_user=sshuser    ansible_port=2026
hq-cli.au-team.irpo  ansible_user=sshuser    ansible_port=2026
br-rtr.au-team.irpo  ansible_user=net_admin  ansible_port=22
```

```bash
# Генерировать SSH-ключ (без passphrase):
ssh-keygen -t rsa -b 4096 -N "" -f /root/.ssh/id_rsa

# Разослать на узлы:
ssh-copy-id -p 2026 sshuser@192.168.100.2   # HQ-SRV
ssh-copy-id -p 2026 sshuser@192.168.200.10  # HQ-CLI
ssh-copy-id net_admin@172.16.1.2            # HQ-RTR
ssh-copy-id net_admin@172.16.2.2            # BR-RTR

# Проверка связи:
ansible all -m ping
# Должно вывести: SUCCESS для всех узлов
```

---

## Задание 6 — Docker на BR-SRV

> 📌 Образы загружаются из Additional.iso (интернет на экзамене есть не всегда).

```bash
# ==== На BR-SRV ====

# Установить Docker:
apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose
systemctl enable docker
systemctl start docker

# Подключить ISO в Proxmox:
# Hardware -> Add -> CD/DVD Drive -> ISO image
# (ISO должно быть загружено в хранилище Proxmox)

# Смонтировать ISO:
mkdir -p /media/cdrom
mount /dev/sr0 /media/cdrom

# Проверить содержимое:
ls /media/cdrom/

# Загрузить образы в Docker:
docker load -i /media/cdrom/docker/site.tar
docker load -i /media/cdrom/docker/mariadb.tar
# Или если имена другие:
ls /media/cdrom/docker/
# загружаем все файлы типа *.tar:
for f in /media/cdrom/docker/*.tar; do docker load -i "$f"; done

# Проверить загруженные образы:
docker images
# Запомните точные имена для docker-compose.yml!
```

```bash
mkdir -p /opt/docker
vim /opt/docker/docker-compose.yml
```

```yaml
version: '3'
services:
  site:
    image: site:latest    # имя узнайте из docker images
    container_name: site
    restart: always
    ports:
      - "8080:8080"
    environment:
      DB_HOST: db
      DB_NAME: testdb
      DB_USER: test
      DB_PASSWORD: P@ssw0rd
    depends_on:
      - db

  db:
    image: mariadb:latest  # имя узнайте из docker images
    container_name: db
    restart: always
    environment:
      MYSQL_ROOT_PASSWORD: P@ssw0rd
      MYSQL_DATABASE: testdb
      MYSQL_USER: test
      MYSQL_PASSWORD: P@ssw0rd
```

```bash
cd /opt/docker
docker-compose up -d

# Проверка:
docker ps
curl http://localhost:8080
# Должна ответить HTTP 200 или страница сайта
```

---

## Задание 7 — Apache + MariaDB на HQ-SRV

```bash
# ==== На HQ-SRV ====

# Установить Apache (в Альт — httpd), PHP, MariaDB:
apt-get install -y apache2 php8.1 php8.1-mysqli mariadb-server
# или если php8.1 не найдён:
apt-get install -y apache2 php php-mysqli mariadb-server

systemctl enable httpd
systemctl enable mariadb
systemctl start mariadb
systemctl start httpd

# Подключить ISO к HQ-SRV (аналогично Docker):
mkdir -p /media/cdrom
mount /dev/sr0 /media/cdrom
ls /media/cdrom/web/

# Скопировать файлы веб-приложения:
cp -r /media/cdrom/web/* /var/www/html/

# Создать БД и пользователя:
mysql -u root << 'EOF'
CREATE DATABASE IF NOT EXISTS webdb;
CREATE USER IF NOT EXISTS 'web'@'localhost' IDENTIFIED BY 'P@ssw0rd';
GRANT ALL PRIVILEGES ON webdb.* TO 'web'@'localhost';
FLUSH PRIVILEGES;
EOF

# Импорт дампа (если есть):
mysql webdb < /media/cdrom/web/dump.sql

# Отредактировать config.php или index.php:
# Убедитесь, что подключение с правильными данными:
grep -r "db_host\|database\|DB_" /var/www/html/ | head -20
vim /var/www/html/config.php  # или index.php

systemctl restart httpd

# Проверка:
curl http://localhost/
```

---

## Задание 8 — Port forwarding на роутерах

> 📌 Пробрасываем порты через NAT так, чтобы nginx на ISP мог обращаться к веб-серверам.

```bash
# ==== На HQ-RTR ====
# Замените ens18 = имя WAN-интерфейса (172.16.1.2)
# Замените  192.168.100.2 = IP HQ-SRV

# Форвардинг должен быть включён (из зад. 8 Модуля 1)!

# Проброс TCP 8080 -> HQ-SRV:80
iptables -t nat -A PREROUTING -i ens18 -p tcp --dport 8080 -j DNAT \
  --to-destination 192.168.100.2:80
iptables -A FORWARD -d 192.168.100.2 -p tcp --dport 80 -j ACCEPT

# Проброс SSH-порта 2026 -> HQ-SRV:2026
iptables -t nat -A PREROUTING -i ens18 -p tcp --dport 2026 -j DNAT \
  --to-destination 192.168.100.2:2026
iptables -A FORWARD -d 192.168.100.2 -p tcp --dport 2026 -j ACCEPT

# Сохранить:
service iptables save
```

```bash
# ==== На BR-RTR ====
# Замените ens18 = имя WAN-интерфейса (172.16.2.2)
# Замените 192.168.20.2 = IP BR-SRV

# Проброс TCP 8080 -> BR-SRV:8080
iptables -t nat -A PREROUTING -i ens18 -p tcp --dport 8080 -j DNAT \
  --to-destination 192.168.20.2:8080
iptables -A FORWARD -d 192.168.20.2 -p tcp --dport 8080 -j ACCEPT

# Проброс SSH 2026 -> BR-SRV:2026
iptables -t nat -A PREROUTING -i ens18 -p tcp --dport 2026 -j DNAT \
  --to-destination 192.168.20.2:2026
iptables -A FORWARD -d 192.168.20.2 -p tcp --dport 2026 -j ACCEPT

service iptables save
```

---

## Задания 9 + 10 — nginx + HTTP аутентификация на ISP

> 📌 ISP выступает обратным прокси: запросы к web.au-team.irpo перенаправляются на HQ-SRV, к docker.au-team.irpo — на BR-SRV.

```bash
# ==== На ISP ====
apt-get install -y nginx

vim /etc/nginx/nginx.conf
```

Найдите секцию `http { }` и внутри добавьте `server`-блоки (или положите в `/etc/nginx/conf.d/proxy.conf`):

```nginx
# Обратный прокси для web.au-team.irpo -> HQ-SRV
server {
    listen 80;
    server_name web.au-team.irpo;

    # HTTP Базовая аутентификация
    auth_basic           "Access restricted";
    auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass         http://172.16.1.2:8080;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Обратный прокси для docker.au-team.irpo -> BR-SRV
server {
    listen 80;
    server_name docker.au-team.irpo;

    location / {
        proxy_pass         http://172.16.2.2:8080;
        proxy_http_version 1.1;
        proxy_set_header   Host $host;
        proxy_set_header   X-Real-IP $remote_addr;
        proxy_set_header   X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

```bash
# Создать файл паролей для nginx:
apt-get install -y apache2-utils
htpasswd -c /etc/nginx/.htpasswd WEB
# введите: P@ssw0rd

# Или без интеракции:
apt-get install -y openssl
echo "WEB:$(openssl passwd -apr1 'P@ssw0rd')" > /etc/nginx/.htpasswd

# Проверить конфиг:
nginx -t
# Должно: syntax is ok

systemctl enable nginx
systemctl restart nginx

# Проверка:
# С HQ-CLI (если DNS знает web.au-team.irpo):
curl -u WEB:P@ssw0rd http://web.au-team.irpo/
curl http://docker.au-team.irpo/
```

---

## Задание 11 — Яндекс Браузер на HQ-CLI

```bash
# ==== На HQ-CLI ====

# Проверить наличие в репозитории:
apt-cache search yandex
apt-get install -y yandex-browser-stable

# Если нет в репо — скачать с офиц. сайта:
cd /tmp
curl -LO 'https://repo.yandex.ru/yandex-browser/rpm/stable/x86_64/yandex-browser-stable.x86_64.rpm'
rpm -ivh yandex-browser-stable.x86_64.rpm

# Проверка:
yandex-browser --version 2>/dev/null || echo "Установлен"
```

---

## ✅ Конечная проверка модуля 2

```bash
# 1. AD работает:
samba-tool domain info 127.0.0.1            # на BR-SRV
samba-tool user list                         # есть hquser1..5
getent passwd hquser1                        # на HQ-CLI

# 2. RAID работает:
cat /proc/mdstat                             # на HQ-SRV
df -h /raid                                  # /raid смонтирован

# 3. NFS монтируется:
df -h | grep nfs                             # на HQ-CLI

# 4. NTP синхронизирован:
chronyc sources -v                           # значок * = OK

# 5. Docker работает:
docker ps                                    # на BR-SRV
curl http://localhost:8080                   # есть ответ

# 6. Apache/MariaDB:
curl http://localhost/                       # на HQ-SRV

# 7. nginx proxy:
curl -u WEB:P@ssw0rd http://web.au-team.irpo/ # через ISP
```

---

[← Модуль 1](module1.md) | [Далее: Модуль 3 →](module3.md)
