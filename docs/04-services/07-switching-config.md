# 7. Настройка коммутации между sw1-a и sw2-a

[← Документация](../README.md) | [Оглавление раздела](README.md) | [← Предыдущий](06-ospf-config.md) | [Следующий →](08-fwcod-web-config.md)

---

## Содержание

- [Обзор](#обзор)
- [sw1-a (Alt Server)](#sw1-a-alt-server)
  - [Назначение имени](#назначение-имени)
  - [Установка Open vSwitch](#установка-open-vswitch)
  - [Настройка коммутации](#настройка-коммутации)
  - [Настройка RSTP](#настройка-rstp)
  - [Настройка Management интерфейса](#настройка-management-интерфейса)
- [sw2-a (Alt Server)](#sw2-a-alt-server)
  - [Назначение имени](#назначение-имени-1)
  - [Установка Open vSwitch](#установка-open-vswitch-1)
  - [Настройка коммутации](#настройка-коммутации-1)
  - [Настройка RSTP](#настройка-rstp-1)
  - [Настройка Management интерфейса](#настройка-management-интерфейса-1)

---

## Обзор

Для организации коммутации в офисе «a» используется Open vSwitch на серверах Alt Linux.

| Коммутатор | Интерфейсы | Назначение |
|------------|------------|------------|
| sw1-a | ens19 | В сторону rtr-a (trunk) |
| sw1-a | ens20 | В сторону dc-a (access VLAN 100) |
| sw1-a | ens21, ens22 | В сторону sw2-a (trunk) |
| sw2-a | ens19, ens20 | В сторону sw1-a (trunk) |
| sw2-a | ens21 | В сторону cli2-a (access VLAN 200) |
| sw2-a | ens22 | В сторону cli1-a (access VLAN 200) |

---

## sw1-a (Alt Server)

### Назначение имени

Назначаем имя устройства согласно топологии:

```bash
hostnamectl set-hostname sw1-a.office.ssa2026.region; exec bash
```

Также рекомендуется указать имя в файле `/etc/sysconfig/network`:

```bash
vim /etc/sysconfig/network
```

![Hostname file](../images/sw1-a_hostname_file.png)

Проверка имени:

```bash
hostname -f
```

![Hostname check](../images/sw1-a_hostname_check.png)

---

### Установка Open vSwitch

#### Временная настройка сети для установки пакетов

Для установки пакета openvswitch необходим доступ в Интернет:

```bash
ip link add link ens19 name ens19.300 type vlan id 300
ip link set dev ens19.300 up
ip addr add 172.20.30.1/24 dev ens19.300
ip route add 0.0.0.0/0 via 172.20.30.254
echo "nameserver 77.88.8.8" > /etc/resolv.conf
```

#### Установка и настройка Open vSwitch

Обновляем список пакетов и устанавливаем openvswitch:

```bash
apt-get update && apt-get install -y openvswitch
```

Включаем и добавляем в автозагрузку:

```bash
systemctl enable --now openvswitch
```

Отключаем автоудаление настроек OVS:

```bash
sed -i "s/OVS_REMOVE=yes/OVS_REMOVE=no/g" /etc/net/ifaces/default/options
```

Перезагружаем сервер:

```bash
reboot
```

#### Настройка физических интерфейсов

Проверяем интерфейсы:

![Interfaces down](../images/sw1-a_interfaces_down.png)

Поднимаем физические интерфейсы через etcnet:

```bash
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens20
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens21
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens22
```

Перезагружаем службу network:

```bash
systemctl restart network
```

Проверяем, что интерфейсы в статусе UP:

![Interfaces up](../images/sw1-a_interfaces_up.png)

#### Временный коммутатор для sw2-a

Создаём временный коммутатор для установки OVS на sw2-a:

```bash
ovs-vsctl add-br br0
ovs-vsctl add-port br0 ens19
ovs-vsctl add-port br0 ens21
```

---

### Настройка коммутации

#### Удаление временного коммутатора

```bash
ovs-vsctl del-br br0
```

#### Создание основного коммутатора

```bash
ovs-vsctl add-br sw1-a
```

Проверка создания:

![OVS bridge](../images/sw1-a_ovs_bridge.png)

#### Настройка портов

**Access порт в сторону dc-a (VLAN 100):**

```bash
ovs-vsctl add-port sw1-a ens20 tag=100
```

**Trunk порт в сторону rtr-a:**

```bash
ovs-vsctl add-port sw1-a ens19 trunk=100,200,300
```

**Trunk порты в сторону sw2-a:**

```bash
ovs-vsctl add-port sw1-a ens21 trunk=100,200,300
ovs-vsctl add-port sw1-a ens22 trunk=100,200,300
```

Проверка портов:

![OVS ports](../images/sw1-a_ovs_ports.png)

#### Включение модуля 802.1Q

```bash
modprobe 8021q
echo "8021q" | tee -a /etc/modules
```

---

### Настройка RSTP

Включаем RSTP на коммутаторе:

```bash
ovs-vsctl set bridge sw1-a rstp_enable=true
ovs-vsctl set bridge sw1-a other_config:stp-protocol=rstp
```

Задаём наименьший приоритет (Root Bridge):

```bash
ovs-vsctl set bridge sw1-a other_config:rstp-priority=0
```

Проверка RSTP:

```bash
ovs-appctl rstp/show
```

![RSTP show](../images/sw1-a_rstp_show.png)

Проверка настроек bridge:

```bash
ovs-vsctl list bridge
```

![RSTP list](../images/sw1-a_rstp_list.png)

---

### Настройка Management интерфейса

#### Создание каталога и файла options

```bash
mkdir /etc/net/ifaces/mgmt
nano /etc/net/ifaces/mgmt/options
```

Содержимое файла options:

![mgmt options](../images/sw1-a_mgmt_options.png)

```
TYPE=ovsport
BOOTPROTO=static
CONFIG_IPV4=yes
BRIDGE=sw1-a
VID=300
```

| Параметр | Значение | Описание |
|----------|----------|----------|
| TYPE | ovsport | Тип интерфейса (internal) |
| BOOTPROTO | static | Статическая настройка |
| CONFIG_IPV4 | yes | Использовать IPv4 |
| BRIDGE | sw1-a | К какому мосту добавить |
| VID | 300 | Принадлежность к VLAN |

#### Назначение IP-адреса и маршрута

```bash
echo "172.20.30.1/24" > /etc/net/ifaces/mgmt/ipv4address
echo "default via 172.20.30.254" > /etc/net/ifaces/mgmt/ipv4route
```

Применяем настройки:

```bash
systemctl restart network
```

#### Проверка настроек

Проверка IP-адреса:

![mgmt IP](../images/sw1-a_mgmt_ip.png)

Проверка маршрута:

![mgmt route](../images/sw1-a_mgmt_route.png)

Проверка в OVS:

![OVS mgmt](../images/sw1-a_ovs_mgmt.png)

#### Настройка Native VLAN

```bash
ovs-vsctl set port mgmt vlan_mode=native-untagged
```

Проверка:

```bash
ovs-vsctl list port mgmt
```

![mgmt native](../images/sw1-a_mgmt_native.png)

---

## sw2-a (Alt Server)

### Назначение имени

```bash
hostnamectl set-hostname sw2-a.office.ssa2026.region; exec bash
```

![Hostname check sw2-a](../images/sw2-a_hostname_check.png)

---

### Установка Open vSwitch

#### Временная настройка сети

```bash
ip link add link ens19 name ens19.300 type vlan id 300
ip link set dev ens19.300 up
ip addr add 172.20.30.2/24 dev ens19.300
ip route add 0.0.0.0/0 via 172.20.30.254
echo "nameserver 77.88.8.8" > /etc/resolv.conf
```

#### Установка пакета

```bash
apt-get update && apt-get install -y openvswitch
systemctl enable --now openvswitch
sed -i "s/OVS_REMOVE=yes/OVS_REMOVE=no/g" /etc/net/ifaces/default/options
reboot
```

#### Настройка физических интерфейсов

Проверка интерфейсов (до):

![Interfaces down sw2-a](../images/sw2-a_interfaces_down.png)

```bash
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens20
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens21
cp -r /etc/net/ifaces/ens19 /etc/net/ifaces/ens22
systemctl restart network
```

Проверка интерфейсов (после):

![Interfaces up sw2-a](../images/sw2-a_interfaces_up.png)

---

### Настройка коммутации

#### Создание коммутатора

```bash
ovs-vsctl add-br sw2-a
```

![OVS bridge sw2-a](../images/sw2-a_ovs_bridge.png)

#### Настройка портов

**Access порты в сторону клиентов (VLAN 200):**

```bash
ovs-vsctl add-port sw2-a ens22 tag=200
ovs-vsctl add-port sw2-a ens21 tag=200
```

**Trunk порты в сторону sw1-a:**

```bash
ovs-vsctl add-port sw2-a ens19 trunk=100,200,300
ovs-vsctl add-port sw2-a ens20 trunk=100,200,300
```

Проверка портов:

![OVS ports sw2-a](../images/sw2-a_ovs_ports.png)

#### Включение модуля 802.1Q

```bash
modprobe 8021q
echo "8021q" | tee -a /etc/modules
```

---

### Настройка RSTP

```bash
ovs-vsctl set bridge sw2-a rstp_enable=true
ovs-vsctl set bridge sw2-a other_config:stp-protocol=rstp
```

> 📝 **Примечание:** На sw2-a приоритет не задаём — он останется по умолчанию (32768), что сделает sw1-a корневым мостом.

Проверка RSTP:

![RSTP show sw2-a](../images/sw2-a_rstp_show.png)

![RSTP list sw2-a](../images/sw2-a_rstp_list.png)

---

### Настройка Management интерфейса

```bash
mkdir /etc/net/ifaces/mgmt
nano /etc/net/ifaces/mgmt/options
```

Содержимое файла options:

```
TYPE=ovsport
BOOTPROTO=static
CONFIG_IPV4=yes
BRIDGE=sw2-a
VID=300
```

Назначение IP-адреса и маршрута:

```bash
echo "172.20.30.2/24" > /etc/net/ifaces/mgmt/ipv4address
echo "default via 172.20.30.254" > /etc/net/ifaces/mgmt/ipv4route
systemctl restart network
```

Настройка Native VLAN:

```bash
ovs-vsctl set port mgmt vlan_mode=native-untagged
```

---

## Итоговая конфигурация

### sw1-a

```bash
# Коммутатор
ovs-vsctl add-br sw1-a

# Порты
ovs-vsctl add-port sw1-a ens19 trunk=100,200,300
ovs-vsctl add-port sw1-a ens20 tag=100
ovs-vsctl add-port sw1-a ens21 trunk=100,200,300
ovs-vsctl add-port sw1-a ens22 trunk=100,200,300

# RSTP (Root Bridge)
ovs-vsctl set bridge sw1-a rstp_enable=true
ovs-vsctl set bridge sw1-a other_config:stp-protocol=rstp
ovs-vsctl set bridge sw1-a other_config:rstp-priority=0

# Management
ovs-vsctl set port mgmt vlan_mode=native-untagged
```

### sw2-a

```bash
# Коммутатор
ovs-vsctl add-br sw2-a

# Порты
ovs-vsctl add-port sw2-a ens19 trunk=100,200,300
ovs-vsctl add-port sw2-a ens20 trunk=100,200,300
ovs-vsctl add-port sw2-a ens21 tag=200
ovs-vsctl add-port sw2-a ens22 tag=200

# RSTP
ovs-vsctl set bridge sw2-a rstp_enable=true
ovs-vsctl set bridge sw2-a other_config:stp-protocol=rstp

# Management
ovs-vsctl set port mgmt vlan_mode=native-untagged
```

---

## Проверка связности

### Проверка Native VLAN на sw2-a

```bash
ovs-vsctl list port mgmt
```

![mgmt native sw2-a](../images/sw2-a_mgmt_native.png)

### Проверка доступности коммутаторов

#### С маршрутизатора rtr-a

![Ping switches from rtr-a](../images/rtr-a_ping_switches.png)

```
rtr-a#ping 172.20.30.1
4 packets transmitted, 4 received, 0% packet loss

rtr-a#ping 172.20.30.2
4 packets transmitted, 4 received, 0% packet loss
```

✅ Оба коммутатора доступны с rtr-a!

#### С маршрутизатора rtr-cod (через туннель)

![Ping switches from rtr-cod](../images/rtr-cod_ping_switches.png)

```
rtr-cod#ping 172.20.30.1
4 packets transmitted, 4 received, 0% packet loss

rtr-cod#ping 172.20.30.2
4 packets transmitted, 4 received, 0% packet loss
```

✅ Оба коммутатора доступны с rtr-cod через GRE-туннель!

### Проверка доступа в Интернет с коммутаторов

#### С sw1-a

![Ping internet from sw1-a](../images/sw1-a_ping_internet_final.png)

```
ping -c3 77.88.8.8
3 packets transmitted, 3 received, 0% packet loss
```

#### С sw2-a

![Ping internet from sw2-a](../images/sw2-a_ping_internet.png)

```
ping -c3 77.88.8.8
3 packets transmitted, 3 received, 0% packet loss
```

✅ Доступ в Интернет с обоих коммутаторов работает!

---

[← Документация](../README.md) | [Оглавление раздела](README.md) | [← Предыдущий](06-ospf-config.md) | [Следующий →](08-fwcod-web-config.md)
