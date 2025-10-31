# Образец выполнения задания для ГИА ДЭ ПУ (инвариантная часть) по 09.02.06 Сетевое и системное администрирование - стенд ГАПОУ ПК №8 им. И. Ф. Павлова

❗Стенд прошлого года, пока собираю стенд для нового учебного года, но в целом изменения минимальны (вроде как)

Ссылочка на материалы в Yonote - https://itsliventsev.yonote.ru/share/548e46da-9cc5-41a8-9f77-0d4c7134ca73/doc/zapisi-po-podgotovke-k-demoekzamenu-EHSxCjnrWW

Базовый стенд представлен по сссылке - https://disk.yandex.ru/d/Qfry02DM_LYcGA (вложенный ахрив, открывать через 7-ZIP) (Стенд для добавления в VMware Player, вложенная виртуализация через ESXi). (в стенде могут быть изменения)

Для установки стенда через скрипт PVE (https://disk.yandex.ru/d/uT7Z3o0uaSBpjg), инструкция тут - https://itsliventsev.yonote.ru/share/548e46da-9cc5-41a8-9f77-0d4c7134ca73/doc/skript-dlya-avtorazvertyvaniya-stenda-de-2025-adm-na-pve-DT85xpRqXT

Задание и приложения к модулям можно найти тут - https://drive.google.com/drive/folders/1N712W9L0H1KyO9tdLrdTlMYv_eHGJA6a?usp=sharing (ЗАДАНИЕ ДЛЯ ДЭ ПУ (ДЛЯ ПК 8) СО СТРАНИЦЫ 55)

## Модуль 1. Настройка сетевой инфраструктуры  

Необходимо разработать и настроить инфраструктуру информационно коммуникационной системы согласно предложенной топологии (см. Рисунок 1) Задание включает базовую настройку устройств: • присвоение имен устройствам • расчет IP-адресации • настройку коммутации и маршрутизации В ходе проектирования и настройки сетевой инфраструктуры следует вести отчет о своих действиях, включая таблицы и схемы, предусмотренные в задании. По каждому пункту задания, требующего отчёт, составить текстовый документ, название которого должно содержать индекс пункта и краткое описание. Текстовый документ должен содержать текстовую информацию и может включать снимки экрана, кадрированные таким образом, чтобы относящаяся к выполнению задания информация на снимках была читаемой. Итоговый отчет по окончании работы следует сохранить на диске рабочего места и задать имя файла - **ФамилияУчастникаМодуль1** без учёта расширения.

  Приложения для выполнения задания лежат в корневом катологе репозитория 

### Данные по виртуальным машинам в рамках модуля 1 (будем использовать в рамках стенда скорее всего ТОЛЬКО ALT - ALT Server и ALT WorkStation)

<img width="527" height="726" alt="image" src="https://github.com/user-attachments/assets/0c55197b-4228-498e-818b-07c070a249fd" />

### Топология сети

<img width="592" height="704" alt="image" src="https://github.com/user-attachments/assets/42f32516-f55c-479c-896b-0e7924757f95" />

### Схема из Yonote

<img width="1941" height="920" alt="image" src="https://github.com/user-attachments/assets/0c950d66-c887-4d12-bee7-9a966e777103" />

## Задание модуль 1

### 1. Произведите базовую настройку устройств: Настройте имена устройств согласно топологии. Используйте полное доменное имя • На всех устройствах необходимо сконфигурировать IPv4: • IP-адрес должен быть из приватного диапазона, в случае, если сеть локальная, согласно RFC1918 • Локальная сеть в сторону HQ-SRV(VLAN 100) должна вмещать не более 32 адресов • Локальная сеть в сторону HQ-CLI(VLAN 200) должна вмещать не менее 16 адресов • Локальная сеть для управления(VLAN 999) должна вмещать не более 8 адресов • Локальная сеть в сторону BR-SRV должна вмещать не более 16 адресов • Сведения об адресах занесите в таблицу 2, в качестве примера используйте Прил_3_О1_КОД 09.02.06-1-2026-М1

<img width="627" height="206" alt="image" src="https://github.com/user-attachments/assets/061abb0c-b754-40a8-98ae-28bcea0c3d81" />

#### Произведите базовую настройку устройств: Настройте имена устройств согласно топологии

В терминале прописываем mcedit /etc/hostname

<img width="447" height="38" alt="image" src="https://github.com/user-attachments/assets/1270f23f-69ee-4425-83c6-7714d56d0c39" />

Далее заменяем значение на имя нашей ВМ - cтавим имя с учетом полного доменного имени (обращаю внимание, что просят **полное доменное имя**, т.е., согласно пункту задания 9 - *DNS-суффикс – au-team.irpo*, поэтому все названия в файле будут прописываться как *название_машины*.au-team.irpo.)

<img width="553" height="233" alt="image" src="https://github.com/user-attachments/assets/c56b716b-c55e-4002-81b7-db05f25736a6" />

#### На всех устройствах необходимо сконфигурировать IPv4: • IP-адрес должен быть из приватного диапазона, в случае, если сеть локальная, согласно RFC1918 • Локальная сеть в сторону HQ-SRV(VLAN 100) должна вмещать не более 32 адресов • Локальная сеть в сторону HQ-CLI(VLAN 200) должна вмещать не менее 16 адресов • Локальная сеть для управления(VLAN 999) должна вмещать не более 8 адресов • Локальная сеть в сторону BR-SRV должна вмещать не более 16 адресов

Далее необходимо настроить виртуальные сетевые адаптеры на ВМ, для этого переходим в настройки виртуальной машины, где добавляем необходимое по схеме кол-во сетевых адаптеров, а также прописываем сети в которых они будут работать, *ПРИМЕР НА ISP*

<img width="914" height="628" alt="image" src="https://github.com/user-attachments/assets/16484a31-5a5a-4342-91f9-7fa0fbaaa552" />

Настройки для других машин:

HQ-SRV

<img width="822" height="531" alt="image" src="https://github.com/user-attachments/assets/50dc1353-4d9d-4d54-8b72-44777add0f63" />

HQ-CLI

<img width="909" height="577" alt="image" src="https://github.com/user-attachments/assets/019d1de3-7241-415a-b98f-8ba9366f856d" />

BR-RTR

<img width="860" height="541" alt="image" src="https://github.com/user-attachments/assets/ecf0be23-0828-47f4-8395-259c97de296d" />

BR-SRV

<img width="864" height="587" alt="image" src="https://github.com/user-attachments/assets/d013a5f0-71b2-4527-9f3c-dc7eb2925ec9" />

HQ-RTR

<img width="869" height="558" alt="image" src="https://github.com/user-attachments/assets/f3de7848-60ad-4e2e-b94e-ceabf2e63a3f" />

⚠️Сеть VM Network не представлена в задании, используется, если есть проблемы с выходом в интернет, т.е., через неё **напрямую** дается выход в интернет с любой машины, если на адаптере включить DHCP.

Для проверки корректности сетевых адаптеров используем команду - ip -c a

<img width="880" height="340" alt="image" src="https://github.com/user-attachments/assets/9037ad7c-504a-4d56-a82a-b97b56ba36a4" />

Выводит список сетевых адаптеров. Далее через настройки ВМ, **ОБЯЗАТЕЛЬНО** сводим значения MAC-адресов, чтобы понять, какой сетевой адаптер куда подключается

<img width="1914" height="974" alt="image" src="https://github.com/user-attachments/assets/20558794-79e4-4c46-8d91-ea8d977449d9" />

#### Пример настройки сетевого адаптера для выхода на DHCP

Открываем файл конфигурации сетевого адаптера

<img width="541" height="38" alt="image" src="https://github.com/user-attachments/assets/a14f395a-c73c-4004-ad37-98ecf6d0c3cb" />

В значении *BOOTPROTO* меням static на dhcp (МАЛЕНЬКИМИ БУКВАМИ)

<img width="364" height="260" alt="image" src="https://github.com/user-attachments/assets/fac77d59-aac1-4b17-b272-9f435a2bf88c" />

#### Пример настройки нового сетевого адаптера на статику

Создаем новую директорию для конфигурации сетевого адаптера (НАЗВАНИЕ ДИРЕКТОРИИ, ПО ИМЕНИ СЕТЕВОГО АДАПТЕРА ИЗ КОМАНДЫ ip -c a)

<img width="501" height="50" alt="image" src="https://github.com/user-attachments/assets/32544dc0-b614-425e-b594-05562ace7d27" />

Копируем из базовой директории ens192 (есть всегда), файл конфигурации в новые директории для вновь созданных сетевых адаптеров

<img width="764" height="43" alt="image" src="https://github.com/user-attachments/assets/c66d26cf-74a4-4551-bd0e-823d6f96bfb7" />

Для статики оставляем *BOOTPROTO* = static

<img width="667" height="343" alt="image" src="https://github.com/user-attachments/assets/73a75d10-b89d-46d4-be58-5229422080d7" />

Создаем новый файл в папке с сетевым адаптером, для конфигурации IP-адреса

<img width="577" height="30" alt="image" src="https://github.com/user-attachments/assets/25dcb3b0-30ac-4450-8bd9-a73bddb1b886" />

Прописываем адрес с маской

<img width="380" height="142" alt="image" src="https://github.com/user-attachments/assets/d619e7fe-e640-4067-8aff-d8e6f9dc3d1f" />

⚠️В случае если, проставляем IP-адрес на конечном устройстве, или на маршрутизаторе в сторону ISP, НЕ ЗАБЫВАЕМ СТАВИТЬ ОСНОВНОЙ ШЛЮЗ, для этого создаем файл

<img width="557" height="45" alt="image" src="https://github.com/user-attachments/assets/9485b3f8-1dad-4c6b-a2cb-f6ac35216203" />

Прописываем только IP-адрес (БЕЗ МАСКИ), устройства куда нужно отправлять пакеты (ВЫШЕСТОЯЩЕЕ УСТРОЙСТВО ПО СХЕМЕ)

<img width="402" height="226" alt="image" src="https://github.com/user-attachments/assets/317c266d-b963-42f8-be0f-41ac03a416af" />

Для применения настроек (для перезагрузки сети), прописываем команду - systemctl restart network

<img width="431" height="43" alt="image" src="https://github.com/user-attachments/assets/7b6e0ac4-8918-4c5d-9763-17daac3e18dd" />

⚠️ДЛЯ ПРИМЕНЕНИЯ ИМЕНИ ХОСТА, НУЖНО ПЕРЕЗАГРУЗИТЬ ВМ - reboot (на клиенте через меню, графически)

### 2. Настройте доступ к сети Интернет, на маршрутизаторе ISP: • Настройте адресацию на интерфейсах: • Интерфейс, подключенный к магистральному провайдеру, получает адрес по DHCP • Настройте маршрут по умолчанию, если это необходимо • Настройте интерфейс, в сторону HQ-RTR, интерфейс подключен к сети 172.16.1.0/28 • Настройте интерфейс, в сторону BR-RTR, интерфейс подключен к сети 172.16.2.0/28 • На ISP настройте динамическую сетевую трансляцию портов для доступа к сети Интернет HQ-RTR и BR-RTR.

Базовая настройка на ISP не отличается. также прописываем имя хоста, выставляем IP-адреса, **ОБРАЩАЮ ВНИМАНИЕ, ЧТО ПОДСЕТИ НА ISP УКАЗАНЫ ПО ЗАДАНИЮ*. 

#### Настройте динамическую сетевую трансляцию портов

1. Включение IP-форвардинга
Это позволяет серверу маршрутизировать пакеты между интерфейсами.

Включение на время работы (немедленный эффект):

echo 1 > /proc/sys/net/ipv4/ip_forward
Сделать постоянным (через перезагрузки, редактируя конфиг):

sed -i 's/^net.ipv4.ip_forward.*/net.ipv4.ip_forward = 1/' /etc/sysctl.conf
grep -q "^net.ipv4.ip_forward" /etc/sysctl.conf || echo "net.ipv4.ip_forward = 1" >> /etc/sysctl.conf
sysctl -p

**ПРОЩЕ ТАК** - через файл:

<img width="443" height="49" alt="image" src="https://github.com/user-attachments/assets/7d8b41c7-8fe9-4d2a-922f-d6d7dd8c6e0c" />

Меняем значение ip_forward на 1

<img width="231" height="38" alt="image" src="https://github.com/user-attachments/assets/c881f413-00b0-4a89-9e8c-6ed92895551e" />

ПЕРЕЗАГРУЖАЕМСЯ

#### Проверка:

cat /proc/sys/net/ipv4/ip_forward  # Должен вернуть: 1
grep "^net.ipv4.ip_forward" /etc/sysctl.conf  # Должен показать: net.ipv4.ip_forward = 1

<details><summary>Сложный, но правильный вариант через через iptables и т.п., ЕСЛИ СТРАШНО, ТО ПРОПУСКАЕМ, ОСТАВЛЯЕМ ТОЛЬКО IP_forward</summary>

2. Очистка существующих правил iptables (опционально, но рекомендуется для чистоты)
Это удалит старые правила, чтобы избежать конфликтов. Будьте осторожны, если у вас есть другие правила файрвола!

##### iptables -t nat -F POSTROUTING

#### iptables -F FORWARD

#### Опционально: Полная очистка (используйте, если хотите полный сброс)

#### iptables -F

#### iptables -t nat -F

#### iptables -t mangle -F

#### 3. Добавление правила MASQUERADE для динамического NAT
Это переписывает исходящие пакеты из локальных сетей, используя динамический IP на ENS192.

iptables -t nat -A POSTROUTING -o ENS192 -j MASQUERADE
Проверка:
iptables -t nat -L POSTROUTING -n -v  # Должен показать: MASQUERADE  all  --  0.0.0.0/0  0.0.0.0/0 (с счётчиками пакетов)

#### 4. Добавление правил форвардинга
Это позволяет пересылать трафик между локальными сетями и интернетом. Указываем правила для установленных соединений и каждой сети.

#### Разрешение для установленных/связанных соединений (для обратного трафика)
iptables -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

#### Разрешение форвардинга для каждой локальной сети к/от интернета (через ENS192)
#### Для 172.16.1.0/28 (ISP-HQ)
iptables -A FORWARD -s 172.16.1.0/28 -o ENS192 -j ACCEPT
iptables -A FORWARD -d 172.16.1.0/28 -i ENS192 -j ACCEPT

#### Для 172.16.2.0/28 (ISP-BR)
iptables -A FORWARD -s 172.16.2.0/28 -o ENS192 -j ACCEPT
iptables -A FORWARD -d 172.16.2.0/28 -i ENS192 -j ACCEPT

#### Для 192.168.1.0/28 (BR-NET)
iptables -A FORWARD -s 192.168.1.0/28 -o ENS192 -j ACCEPT
iptables -A FORWARD -d 192.168.1.0/28 -i ENS192 -j ACCEPT

#### Для 192.168.2.0/27 (HQ-NET)
iptables -A FORWARD -s 192.168.2.0/27 -o ENS192 -j ACCEPT
iptables -A FORWARD -d 192.168.2.0/27 -i ENS192 -j ACCEPT

#### Опционально: Разрешение форвардинга между локальными сетями (например, если HQ-NET нужно общаться с BR-NET)
iptables -A FORWARD -s 172.16.1.0/28 -d 172.16.2.0/28 -j ACCEPT
iptables -A FORWARD -s 172.16.2.0/28 -d 172.16.1.0/28 -j ACCEPT
iptables -A FORWARD -s 192.168.1.0/28 -d 192.168.2.0/27 -j ACCEPT
iptables -A FORWARD -s 192.168.2.0/27 -d 192.168.1.0/28 -j ACCEPT
Проверка:
iptables -L FORWARD -n -v  # Список всех правил FORWARD с счётчиками; ищите ваши сети
iptables -L FORWARD -n | grep "172.16.1.0/28"  # Проверка для конкретной сети
5. Сохранение конфигурации (чтобы правила сохранялись после перезагрузки)
ALT Linux использует iptables-save и сервис iptables для сохранения 3 (похоже на Red Hat/Fedora).

#### Сохранение правил
iptables-save > /etc/sysconfig/iptables

#### Включение и запуск сервиса iptables
systemctl enable iptables
systemctl start iptables
Проверка:
systemctl status iptables  # Должен показать active (running)
После перезагрузки правила должны загрузиться автоматически. Если нет, установите iptables-persistent (если доступно: apt-get install iptables-persistent, затем netfilter-persistent save).

</details>

### 3. Создайте локальные учетные записи на серверах HQ-SRV и BR-SRV: • Создайте пользователя sshuser • Пароль пользователя sshuser с паролем P@ssw0rd • Идентификатор пользователя 2026 • Пользователь sshuser должен иметь возможность запускать sudo без ввода пароля 59 • Создайте пользователя net_admin на маршрутизаторах HQ-RTR и BR RTR • Пароль пользователя net_admin с паролем P@ssw0rd • При настройке ОС на базе Linux, запускать sudo без ввода пароля • При настройке ОС отличных от Linux пользователь должен обладать максимальными привилегиями.

#### Создайте локальные учетные записи на серверах HQ-SRV и BR-SRV

useradd - создание пользователя

Ключи для команды useradd

<img width="747" height="969" alt="image" src="https://github.com/user-attachments/assets/aa9ce066-bbb6-43c9-b718-5419b71a0560" />

Для создания пользователя с определенным UID (Идентификатором) используем ключ -u (МАЛЕЬНКАЯ)

<img width="383" height="39" alt="image" src="https://github.com/user-attachments/assets/09832d19-8c31-4bc5-8e11-97db6cb6e961" />

Поставить/изменить пароль пользователя

<img width="299" height="38" alt="image" src="https://github.com/user-attachments/assets/378fc7c8-9bbb-4953-b279-aeee76119bdd" />

####  При настройке ОС на базе Linux, запускать sudo без ввода пароля

Добавить пользователя в группу пользователей

<img width="397" height="38" alt="image" src="https://github.com/user-attachments/assets/c059ead3-527d-45ee-8ae8-af50e433a213" />

При необходимости, проверяем, что пользователь в группе

<img width="614" height="48" alt="image" src="https://github.com/user-attachments/assets/102dc15d-2114-4b9a-a82d-3bef2582264a" />

##### Разрешаем использовать sudo без ввода пароля для группы пользователей wheel

Редактируем файл sudoers

<img width="358" height="36" alt="image" src="https://github.com/user-attachments/assets/8b62e47c-17a9-45bf-8c60-ec3d23a7aff7" />

Находим следующие строки

<img width="644" height="101" alt="image" src="https://github.com/user-attachments/assets/44dac93e-42f7-4dd7-afef-8c756eed1510" />

Убираем с двух атрибутов решетки (раскоментирование), чтобы работали (#) 

<img width="648" height="111" alt="image" src="https://github.com/user-attachments/assets/b10aab12-3d80-4dcc-aa81-4cd119e96ed3" />

Можем проверить, через авторизацию под нашим вновь созданным пользователем


<img width="495" height="275" alt="image" src="https://github.com/user-attachments/assets/998576ad-66f6-43ba-a2cc-402e99af9cc4" />

### ⚠️4. Настройте коммутацию в сегменте HQ следующим образом: • Трафик HQ-SRV должен принадлежать VLAN 100 • Трафик HQ-CLI должен принадлежать VLAN 200 • Предусмотреть возможность передачи трафика управления в VLAN 999 • Реализовать на HQ-RTR маршрутизацию трафика всех указанных VLAN с использованием одного сетевого адаптера ВМ/физического порта • Сведения о настройке коммутации внесите в отчёт (ПОКА НЕ ТРОГАЕМ ЭТО ЗАДАНИЕ) - В СТЕНДЕ НЕ БУДЕТ ВИРТУАЛЬНОГО КОММУТАТОРА⚠️

### 5. Настройте безопасный удаленный доступ на серверах HQ-SRV и BR SRV: • Для подключения используйте порт 2026 • Разрешите подключения исключительно пользователю sshuser • Ограничьте количество попыток входа до двух • Настройте баннер «Authorized access only».

Устанавливаем OpenSSH-server

<img width="618" height="49" alt="image" src="https://github.com/user-attachments/assets/e2b7a58e-eb04-4a31-9ddb-ddb422d0580a" />

Если выходит ошибка, прописываем systemctl daemon-reload

<img width="678" height="142" alt="image" src="https://github.com/user-attachments/assets/f619a90b-f4e8-4638-9145-d901a36e3d98" />

После чего повторно проводим команду на установку

Добавляем сервис в автозагрузку systemctl enable —now sshd

<img width="564" height="44" alt="image" src="https://github.com/user-attachments/assets/c25e3370-32ad-467b-9b7a-e1d58c90c66c" />

Настройка файла конфигурации OpenSSH

<img width="621" height="59" alt="image" src="https://github.com/user-attachments/assets/5640698a-e293-466e-bc48-db2e60b09aa9" />

По заданию нужен порт 2026, поэтому меняем значение

<img width="1020" height="511" alt="image" src="https://github.com/user-attachments/assets/13a629c1-47ba-4e0f-84f7-cfbdc056755e" />

По заданию кол-во попыток 2, меняем значение

<img width="382" height="81" alt="image" src="https://github.com/user-attachments/assets/4e01e63c-f74b-4d28-ac30-2b56f48a25b4" />

Добавляем значение AllowUsers, куда по заданию прописываем только sshuser

<img width="250" height="60" alt="image" src="https://github.com/user-attachments/assets/d74f3ebf-1be2-4c95-b277-8fcbeadf3a05" />

Добавляем путь для баннера

<img width="351" height="74" alt="image" src="https://github.com/user-attachments/assets/6e14c378-b5c8-4102-bb12-007537c80e17" />

Создаем папку и файл в ней для баннера

<img width="629" height="76" alt="image" src="https://github.com/user-attachments/assets/9744f240-088a-4730-84a7-b124b9ca9f4a" />

Прописываем по заданию - Authorized access only

<img width="575" height="214" alt="image" src="https://github.com/user-attachments/assets/7499bc53-6496-478e-a460-f06dcfb2b2ef" />

Проверяем, видим что включен и порт поменялся

<img width="990" height="386" alt="image" src="https://github.com/user-attachments/assets/f50e2c4a-e852-4825-b248-76f389158d10" />

Для проверки подключения по SSH на другой машине пишем:

ssh sshuser@192.168.2.3 -p 2026

ssh sshuser@192.168.1.2 -p 2026

### 6. Между офисами HQ и BR, на маршрутизаторах HQ-RTR и BR-RTR необходимо сконфигурировать ip туннель: • На выбор технологии GRE или IP in IP • Сведения о туннеле занесите в отчёт.

### 7. Обеспечьте динамическую маршрутизацию на маршрутизаторах HQ RTR и BR-RTR: сети одного офиса должны быть доступны из другого офиса и наоборот. Для обеспечения динамической маршрутизации используйте link state протокол на усмотрение участника: • Разрешите выбранный протокол только на интерфейсах ip туннеля • Маршрутизаторы должны делиться маршрутами только друг с другом • Обеспечьте защиту выбранного протокола посредством парольной защиты • Сведения о настройке и защите протокола занесите в отчёт.

apt-get update - обновление репозиториев

<img width="1079" height="243" alt="image" src="https://github.com/user-attachments/assets/66e0c8db-f9c6-4249-955b-3892e6fe9e53" />

apt-get install frr -y - устанавливаем пакет FRR

<img width="1068" height="452" alt="image" src="https://github.com/user-attachments/assets/b5ed2f4b-2b10-4d40-aa7e-62ab6230fb81" />

Заходим в файл конфигурации демонов FRR

<img width="327" height="23" alt="image" src="https://github.com/user-attachments/assets/d3224633-5c26-4aeb-8a1a-40c847f56198" />

Видим список протоколов

<img width="168" height="305" alt="image" src="https://github.com/user-attachments/assets/00af27bf-5401-4346-81b7-b141ff4aaba6" />

Изменяем значение eigrpd с no на yes

<img width="247" height="321" alt="image" src="https://github.com/user-attachments/assets/3f652885-7352-492d-aabb-3ed67665e176" />

Применяем новую конфигурацию, перезагружая сервис

<img width="382" height="50" alt="image" src="https://github.com/user-attachments/assets/235362ed-31c4-48ba-a879-a246115ff235" />

Проверяем, что FRR запустился

<img width="1042" height="508" alt="image" src="https://github.com/user-attachments/assets/bcbf2b4e-79a0-4371-936b-687b8dd61099" />

Заходим в управление FRR

<img width="176" height="32" alt="image" src="https://github.com/user-attachments/assets/dee2c994-d1fe-4a93-ad84-da9f2a6e3fa0" />

**СИНТАКСИС ВНУТРИ, КАК В CISCO**

Настройка FRR для BR-RTR

<img width="363" height="296" alt="image" src="https://github.com/user-attachments/assets/74bf5ab6-6fff-44bb-b08e-77e45658707f" />

Настройка FRR для HQ-RTR

<img width="325" height="383" alt="image" src="https://github.com/user-attachments/assets/23351034-56eb-4143-8a1e-d793c5d334be" />

Настройка FRR для ISP

<img width="320" height="278" alt="image" src="https://github.com/user-attachments/assets/a92e64fd-8162-4a95-8163-635e370c458c" />


### 8. Настройка динамической трансляции адресов маршрутизаторах HQ RTR и BR-RTR: • Настройте динамическую трансляцию адресов для обоих офисов в сторону ISP, все устройства в офисах должны иметь доступ к сети Интернет

**ПРОЩЕ ТАК** - через файл:

<img width="443" height="49" alt="image" src="https://github.com/user-attachments/assets/7d8b41c7-8fe9-4d2a-922f-d6d7dd8c6e0c" />

Меняем значение ip_forward на 1

<img width="231" height="38" alt="image" src="https://github.com/user-attachments/assets/c881f413-00b0-4a89-9e8c-6ed92895551e" />

ПЕРЕЗАГРУЖАЕМСЯ

### 9. Настройте протокол динамической конфигурации хостов для сети в сторону HQ-CLI: • Настройте нужную подсеть • В качестве сервера DHCP выступает маршрутизатор HQ-RTR • Клиентом является машина HQ-CLI • Исключите из выдачи адрес маршрутизатора • Адрес шлюза по умолчанию – адрес маршрутизатора HQ-RTR • Адрес DNS-сервера для машины HQ-CLI – адрес сервера HQ-SRV • DNS-суффикс – au-team.irpo • Сведения о настройке протокола занесите в отчёт.

Устанавливаем DHCP-server

<img width="647" height="56" alt="image" src="https://github.com/user-attachments/assets/aeb83485-966a-4732-bf14-907f4e60f233" />

<img width="1181" height="107" alt="image" src="https://github.com/user-attachments/assets/3a4af180-c663-4ee6-82ce-3d94ae7f1512" />

Копируем файл конфигурации и называем его dhcpd.conf

<img width="834" height="34" alt="image" src="https://github.com/user-attachments/assets/c3f22dbb-7348-4ba8-8825-13f06bc4f102" />

Настройка выдачи DHCP, заходим в файл через mcedit

<img width="605" height="337" alt="image" src="https://github.com/user-attachments/assets/a442690d-a654-4ebf-b551-f02445b03144" />

Ставим выдачу DHCP только с опеделенного сетевого адаптера

<img width="683" height="77" alt="image" src="https://github.com/user-attachments/assets/8b8e5e75-ca8f-4dfc-bdf1-7a5460946f84" />

<img width="1420" height="1077" alt="image" src="https://github.com/user-attachments/assets/d10d7221-5f13-4a01-97ab-2e523a386444" />

Проверяем, что DHCP заработал

<img width="1404" height="552" alt="image" src="https://github.com/user-attachments/assets/2d126d70-58aa-42b5-be5b-92744fedeb03" />


### 10. Настройте инфраструктуру разрешения доменных имён для офисов HQ и BR: • Основной DNS-сервер реализован на HQ-SRV • Сервер должен обеспечивать разрешение имён в сетевые адреса устройств и обратно в соответствии с таблицей 3 • В качестве DNS сервера пересылки используйте любой общедоступный DNS сервер(77.88.8.7, 77.88.8.3 или другие) (ЗОНА ОБРАТНОГО ПРОСМОТРА ПОКА НА ДОРАБОТКЕ)

<img width="631" height="272" alt="image" src="https://github.com/user-attachments/assets/beb4fbab-9764-4252-afcc-03e6826a2db9" />

Устанавливаем bind и утилиты

<img width="654" height="46" alt="image" src="https://github.com/user-attachments/assets/b64d6097-8e52-434c-bcb1-a57c3b39049d" />

<img width="638" height="70" alt="image" src="https://github.com/user-attachments/assets/5f1ab4f7-f0ed-4356-bdb5-7e5b1101dcee" />

Меняем значение

<img width="1348" height="1051" alt="image" src="https://github.com/user-attachments/assets/f7e6885d-3e0e-495c-9326-f24b2515e66f" />

где:
listen-on port 53 { any; }; — IP-сети DNS-сервера, на котором он будет принимать запросы; (можно прописать any - слушать везде)
listen-on-v6 port 53 присвоим значение none, тем самым отключив IPv6
allow-query разрешает выполнять запросы всем, но из соображений безопасности можно ограничить доступ для конкретной сети.
forwarders перенаправляем запросы, которые сами не резолвим, на DNS сервер Яндекса.

Добавляем зоны в данный файл

<img width="745" height="54" alt="image" src="https://github.com/user-attachments/assets/69f6e79f-63e4-444a-b3cc-6c2cdbff3385" />

<img width="1349" height="1045" alt="image" src="https://github.com/user-attachments/assets/f767273d-7687-45c9-8878-63933b2d81dd" />

Проверяем, что нет ошибок

<img width="445" height="38" alt="image" src="https://github.com/user-attachments/assets/e4d85eca-8709-4c25-a201-1004b3805592" />

Создаем базы для зон

База для зоны прямого просмотра

<img width="672" height="50" alt="image" src="https://github.com/user-attachments/assets/f09d0d74-bc2b-4188-aaee-ad4f4a5cc411" />

База для зоны обратного просмотра

<img width="813" height="53" alt="image" src="https://github.com/user-attachments/assets/a75e4044-1a5b-44f8-a29f-72761a28ecba" />

Пример заполнения базы данных для зоны прямого просмотра

<img width="1282" height="1036" alt="image" src="https://github.com/user-attachments/assets/55275034-06e4-468f-b74b-d2350e03b767" />

**НА ДОРАБОТКЕ**

Пример заполнения базы данных для зоны обратного просмотра

<img width="1267" height="1023" alt="image" src="https://github.com/user-attachments/assets/2ce18cc0-3b88-48cb-9383-5995043ce3c9" />

..........

### 11. Настройте часовой пояс на всех устройствах (за исключением виртуального коммутатора, в случае его использования) согласно месту проведения экзамена

Выставляем зону для Москвы на всех ВМ

<img width="439" height="28" alt="image" src="https://github.com/user-attachments/assets/8d6b0159-b4f0-419a-9982-6ff312841bf4" />

Если по заданию просят другой регион, то смотрим регионы по следующему пути

<img width="1035" height="123" alt="image" src="https://github.com/user-attachments/assets/36f4d420-cc87-4f2f-b03e-162114a24702" />
