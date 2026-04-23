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

### 6. Между офисами HQ и BR, на маршрутизаторах HQ-RTR и BR-RTR необходимо сконфигурировать ip туннель: • На выбор технологии GRE или IP in IP • Сведения о туннеле занесите в отчёт. (СЕТИ СТАВИМ НА СВОИ, ПОКА В НАСТРОЙКЕ СЕТИ ЛЕВЫЕ)
Настройка динамической маршрутизации

#### Настройка туннеля GRE и OSPF на HQ-RTR

1. **Создание интерфейса туннеля**

   Создайте каталог для интерфейса туннеля:
   ```bash
   mkdir /etc/net/ifaces/gre1
   ```

2. **Настройка файла options для туннеля**

   Создайте и отредактируйте файл:
   ```bash
   mcedit /etc/net/ifaces/gre1/options
   ```
   У вас ip могут отличаться
   Пример содержимого:
   ```
   TUNLOCAL=172.16.4.2
   TUNREMOTE=172.16.5.2
   TUNTYPE=gre
   TYPE=iptun
   TUNOPTIONS='ttl 64'
   HOST=ens192
   ```

3. **Настройка IP-адреса туннеля**

   Создайте файл:
   ```bash
   mcedit/etc/net/ifaces/gre1/ipv4address
   ```
   Пример:
   ```
   172.16.100.2/29
   ```

4. Перезагрузите сеть и проверьте интерфейс:
   ```bash
   systemctl restart network
   ip a
   ```

5. **Настройка frr**

   Добавьте службу `frr` в автозагрузку:
   ```bash
   systemctl enable --now frr
   ```
   Отредактируйте конфигурационный файл демонов:
   ```bash
   mcedit /etc/frr/daemons
   ```
     - Меняем ospfd:
     ```diff
     -#ospfd=no
     +ospfd=yes
     ```
   Сохраните изменения.
   
   Перезагрузите службу frr:
   ```
   systemctl reboot frr
   ```

6. **Настройка OSPF через vtysh**

   Введите:
   ```bash
   vtysh
   ```
   Комнды для настройки ospf
   ```
   show running-config (чтобы проверить если там что нибудь или нет)
   conf t
   router ospf
     passive interface default
     network 172.16.100.0/29 area 0 сеть тунеля 
     network 192.168.10.0/26 area 0 сеть в сторону hq-srv 
     network 192.168.20.0/28 area 0 сеть в сторону hq-сli
     area 0 authentication
   exit
   interface gre1 тут вы указывете название вашего тунеля между hq-rtr и br-rtr
     no ip ospf passive
     ip ospf authentication-key 1245 ваш ключ  
   exit
   do wr
   end
   exit
   ```
   Перезагрузите сеть:
   ```bash
   systemctl restart network
   ```

#### Настройка туннеля GRE и OSPF на BR-RTR

<details>
  <summary>Развернуть инструкцию</summary>

1. **Создание интерфейса туннеля**

   Создайте каталог:
   ```bash
   mkdir /etc/net/ifaces/gre1
   ```

2. **Настройка файла options для туннеля**

   Создайте и отредактируйте файл:
   ```bash
   mcedit /etc/net/ifaces/gre1/options
   ```
   Пример содержимого:
   ```
   TUNLOCAL=172.16.5.2
   TUNREMOTE=172.16.4.2
   TUNTYPE=gre
   TYPE=iptun
   TUNOPTIONS='ttl 64'
   HOST=ens192
   ```

3. **Настройка IP-адреса туннеля**

   Создайте файл:
   ```bash
   mcedit /etc/net/ifaces/gre1/ipv4address
   ```
   Пример:
   ```
   172.16.100.1/29
   ```

4. Перезагрузите сеть:
   ```bash
   systemctl restart network
   ip a
   ```

5. **Настройка frr**

   Добавьте службу `frr` в автозагрузку:
   ```bash
   systemctl enable --now frr
   ```
   Отредактируйте конфигурационный файл демонов:
   ```bash
   mcedit /etc/frr/daemons
   ```
     - Меняем ospfd:
   ```diff
   -#ospfd=no
   +ospfd=yes
   ```
   Сохраните изменения.
   
   Перезагрузите службу frr:
   ```
   systemctl reboot frr
   ```
5. **Настройка OSPF через vtysh**

   Введите:
   ```bash
   vtysh
   ```
   Комнды для настройки ospf
   ```
   show running-config (чтобы проверить если там что нибудь или нет)
   conf t
   router ospf
     passive interface default
     network 172.16.100.0/29 area 0 сеть тунеля 
     network 192.168.30.0/27 area 0 сеть в сторону br-rtr
     area 0 authentication
   exit
   interface gre1 тут вы указывете название вашего тунеля между hq-rtr и br-rtr
     no ip ospf passive
     ip ospf authentication-key 1245 ваш ключ  
   exit
   do wr
   end
   exit
   ```
9. Перезагрузите сеть:
   ```bash
   systemctl restart network
   ```
10. Проверьте настройки:
    ```bash
    vtysh
    show ip ospf neighbor
    ```
    Если сосед отображается – настройка выполнена корректно.

</details>

---



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



______________________________________________________

## Дальше идет немного в разнобой, используем поиск, если нужно конкретное

# Модуль 2. Задание 1: Настройка контроллера домена Samba DC

## Описание задания

- Имя домена: `au-team.irpo`
- Введите в созданный домен машину HQ-CLI
- Создайте 5 пользователей для офиса HQ: имена пользователей формата `hquser№` (например hquser1, hquser2 и т.д.)
- Создайте группу `hq`, введите в группу созданных пользователей
- Убедитесь, что пользователи группы `hq` имеют право аутентифицироваться на HQ-CLI
- Пользователи группы `hq` должны иметь возможность повышать привилегии для выполнения ограниченного набора команд: `cat`, `grep`, `id`. Запускать другие команды с повышенными привилегиями пользователи группы права не имеют.

---

## Решение

### Часть 1: Настройка Samba DC на BR-SRV

#### 1.1 Установка необходимых пакетов

```bash
apt-get update && apt-get install -y task-samba-dc
```

#### 1.2 Очистка предыдущей конфигурации Samba (если была)

```bash
rm -f /etc/samba/smb.conf
rm -rf /var/lib/samba
rm -rf /var/cache/samba
mkdir -p /var/lib/samba/sysvol
```

#### 1.3 Развёртывание домена

Запустите интерактивное развёртывание:

```bash
samba-tool domain provision
```

При запросе параметров:
- **Realm**: `AU-TEAM.IRPO` (подставится автоматически)
- **Domain**: `AU-TEAM` (подставится автоматически)
- **Server Role**: `dc` (нажмите Enter)
- **DNS backend**: `SAMBA_INTERNAL` (нажмите Enter)
- **DNS forwarder IP address**: `192.168.100.2` (IP HQ-SRV или другой DNS)
- **Administrator password**: введите пароль (минимум 7 символов, буквы верхнего/нижнего регистра, цифры)

![Развёртывание домена](Images/01-domain-provision.png)

Пример успешного вывода:

![Успешное развёртывание](Images/02-provision-success.png)

```
Server Role:            active directory domain controller
Hostname:               br-srv
NetBIOS Domain:         AU-TEAM
DNS Domain:             au-team.irpo
DOMAIN SID:             S-1-5-21-3779736722-240538183-1905
```

#### 1.4 Настройка служб

Включаем и добавляем в автозагрузку службу samba:

```bash
systemctl enable --now samba
```

Настройка Kerberos:

```bash
cp /var/lib/samba/private/krb5.conf /etc/krb5.conf
```

Перезагружаем службу samba:

```bash
systemctl restart samba
```

#### 1.5 Настройка DNS на BR-SRV

Редактируем resolv.conf для интерфейса:

```bash
echo "search au-team.irpo" > /etc/net/ifaces/ens192/resolv.conf
echo "nameserver 127.0.0.1" >> /etc/net/ifaces/ens192/resolv.conf
```

Перезагружаем сеть:

```bash
systemctl restart network
```

#### 1.6 Проверка работоспособности домена

Просмотр информации о домене:

```bash
samba-tool domain info 127.0.0.1
```

Проверка SMB-шар:

```bash
smbclient -L 127.0.0.1 -U administrator
```

![Проверка домена](Images/03-domain-info.png)

Введите пароль администратора. Должны отобразиться шары `sysvol` и `netlogon`.

#### 1.7 Проверка DNS

Установка утилиты host (если не установлена):

```bash
apt-get install -y bind-utils
```

Проверка DNS-записей:

```bash
host au-team.irpo
host -t SRV _kerberos._udp.au-team.irpo
host -t SRV _ldap._tcp.au-team.irpo
host br-srv.au-team.irpo
```

![Проверка DNS](Images/04-dns-check.png)

#### 1.8 Проверка Kerberos

Получение билета (имя домена в ВЕРХНЕМ регистре):

```bash
kinit Administrator@AU-TEAM.IRPO
```

Просмотр полученного билета:

```bash
klist
```

![Проверка Kerberos](Images/05-kerberos-check.png)

---

### Часть 2: Создание пользователей и группы

#### 2.1 Создание группы hq

```bash
samba-tool group add hq
```

![Создание группы](Images/06-group-add.png)

Проверка:

```bash
samba-tool group list
```

![Список групп](Images/07-group-list.png)

#### 2.2 Создание пользователей и добавление в группу

```bash
for i in {1..5}; do
  samba-tool user add hquser$i P@ssw0rd
  samba-tool user setexpiry hquser$i --noexpiry
  samba-tool group addmembers "hq" hquser$i
done
```

Проверка членства в группе:

```bash
samba-tool group listmembers hq
```

Ожидаемый вывод:
```
hquser1
hquser2
hquser3
hquser4
hquser5
```

---

### Часть 3: Ввод HQ-CLI в домен

#### 3.1 Настройка сети на HQ-CLI

Задаём статические параметры адресации с указанием DNS-сервера BR-SRV.

Через графический интерфейс (Настройки сети → Проводное подключение → IPv4):
- **Метод IPv4**: Вручную
- **Адрес**: `192.168.200.2`
- **Маска**: `24`
- **Шлюз**: `192.168.200.1`
- **DNS**: `192.168.0.2` (IP адрес BR-SRV)

![Настройка сети](Images/08-network-settings.png)

Или через командную строку:

```bash
# В /etc/net/ifaces/<интерфейс>/resolv.conf
echo "search au-team.irpo" > /etc/net/ifaces/ens192/resolv.conf
echo "nameserver 192.168.0.2" >> /etc/net/ifaces/ens192/resolv.conf
systemctl restart network
```

Проверка разрешения доменного имени:

```bash
host au-team.irpo
```

#### 3.2 Установка пакетов для ввода в домен

```bash
apt-get update && apt-get install -y task-auth-ad-sssd
```

#### 3.3 Ввод в домен через Центр Управления Системой

1. Откройте **Центр управления системой**
2. Перейдите в раздел **Пользователи** → **Аутентификация**

![ЦУС - Аутентификация](Images/09-cus-auth.png)

3. Выберите **Active Directory**
4. Введите:
   - Домен: `au-team.irpo`
   - Имя компьютера: `hq-cli`
   - Администратор: `administrator`
   - Пароль: (пароль администратора домена)
5. Нажмите **Применить**

При успешном вводе появится сообщение:

![Успешный ввод в домен](Images/10-domain-welcome.png)

#### 3.4 Перезагрузка HQ-CLI

После ввода в домен необходимо перезагрузить машину:

![Перезагрузка](Images/11-reboot.png)

```bash
reboot
```

---

### Часть 4: Настройка ограниченного sudo для группы hq

#### 4.1 Установка libnss-role

```bash
apt-get install -y libnss-role
```

Проверка, что модуль включён:

```bash
control libnss-role
```

![Проверка libnss-role](Images/12-libnss-role.png)

Ожидаемый вывод: `enabled`

#### 4.2 Связывание доменной группы с локальной группой wheel

```bash
roleadd hq wheel
```

Проверка:

```bash
rolelst
```

![Связывание групп](Images/13-roleadd.png)

Ожидаемый вывод должен содержать строку:
```
hq:wheel
```

#### 4.3 Настройка sudoers

Редактируем файл `/etc/sudoers`:

```bash
visudo
```

или

```bash
nano /etc/sudoers
```

Добавляем алиас для разрешённых команд:

![Cmnd_Alias в sudoers](Images/14-sudoers-cmnd.png)

```sudoers
## Cmnd alias specification
Cmnd_Alias      SHELLCMD = /bin/cat, /bin/grep, /usr/bin/id
```

Добавляем правило для группы wheel:

![WHEEL_USERS в sudoers](Images/15-sudoers-wheel.png)

```sudoers
## User privilege specification
WHEEL_USERS ALL=(ALL:ALL) SHELLCMD
```

> **Важно**: Убедитесь, что строка `WHEEL_USERS ALL=(ALL:ALL) ALL` закомментирована или удалена, чтобы пользователи группы wheel имели доступ только к указанным командам.

---

### Часть 5: Проверка работы

#### 5.1 Вход под доменным пользователем

На экране входа HQ-CLI нажмите **"Нет в списке?"**:

![Выход пользователя](Images/16-logout.png)

![Нет в списке](Images/17-not-in-list.png)

Введите:
- Логин: `hquser3` (или любой созданный пользователь)
- Пароль: `P@ssw0rd`

#### 5.2 Проверка разрешённых команд

```bash
sudo id
sudo cat /etc/hosts
sudo grep '127.0.0.1' /etc/hosts
```

![Проверка разрешённых команд](Images/18-sudo-allowed.png)

Результат: все команды выполняются успешно.

#### 5.3 Проверка запрещённых команд

```bash
sudo su -
```

![Проверка запрещённых команд](Images/19-sudo-denied.png)

Результат: **отказано в доступе**
```
Извините, пользователю hquser3 не разрешено выполнять «/bin/su -» как root на hq-cli.au-team.irpo.
```

---

## Итоговая проверка

| Проверка | Команда | Ожидаемый результат |
|----------|---------|---------------------|
| Информация о домене | `samba-tool domain info 127.0.0.1` | Показывает Forest, Domain, DC name |
| Список групп | `samba-tool group list` | Содержит группу `hq` |
| Члены группы hq | `samba-tool group listmembers hq` | hquser1-5 |
| DNS домена | `host au-team.irpo` | Резолвится в IP BR-SRV |
| Kerberos | `kinit Administrator@AU-TEAM.IRPO && klist` | Билет получен |
| Вход на HQ-CLI | Вход под hquser1-5 | Успешная аутентификация |
| sudo id | `sudo id` | Выполняется |
| sudo cat | `sudo cat /etc/hosts` | Выполняется |
| sudo grep | `sudo grep '127' /etc/hosts` | Выполняется |
| sudo su | `sudo su -` | Отказано |

---

## Возможные проблемы и решения

### Ошибка при развёртывании домена
- Убедитесь, что пароль соответствует требованиям сложности
- Проверьте, что hostname настроен корректно

### HQ-CLI не видит домен
- Проверьте, что DNS указывает на BR-SRV
- Убедитесь в сетевой связности: `ping 192.168.0.2`

### Пользователь не может войти
- Проверьте службу sssd: `systemctl status sssd`
- Проверьте логи: `journalctl -u sssd`

### sudo не работает
- Проверьте синтаксис sudoers: `visudo -c`
- Убедитесь, что libnss-role включён: `control libnss-role`

# Модуль 2. Задание 2: Конфигурация файлового хранилища (RAID)

## Описание задания

- При помощи двух подключенных к серверу дополнительных дисков размером 1 Гб сконфигурируйте дисковый массив уровня 0
- Имя устройства – `md0`, при необходимости конфигурация массива размещается в файле `/etc/mdadm.conf`
- Создайте раздел, отформатируйте раздел, в качестве файловой системы используйте `ext4`
- Обеспечьте автоматическое монтирование в папку `/raid`

---

## Решение

### Часть 1: Подготовка и установка

#### 1.1 Установка mdadm

`mdadm` — утилита для работы с программными RAID-массивами различных уровней.

```bash
apt-get update && apt-get install -y mdadm
```

#### 1.2 Определение дисков

Просматриваем физические диски для определения, какие будут использоваться в RAID-массиве:

```bash
lsblk
```

![Просмотр дисков](Images/20-lsblk.png)

В данном примере для работы будут использованы диски: `sdb` и `sdc` (оба по 1 Гб).

> **Важно**: У вас диски могут называться иначе. Используйте команду `lsblk` для определения правильных имён.

---

### Часть 2: Создание RAID-массива

#### 2.1 Зануление суперблоков

Перед созданием массива необходимо занулить суперблоки на дисках:

```bash
mdadm --zero-superblock --force /dev/sdb /dev/sdc
```

> **Примечание**: Если диски новые и не использовались ранее в RAID, команда может выдать предупреждение — это нормально.

#### 2.2 Создание RAID-массива уровня 0

```bash
mdadm --create --verbose /dev/md0 -l 0 -n 2 /dev/sdb /dev/sdc
```

**Параметры команды:**
- `/dev/md0` — устройство RAID, которое появится после сборки
- `-l 0` — уровень RAID (0 = striping, чередование)
- `-n 2` — количество дисков в массиве
- `/dev/sdb /dev/sdc` — диски для сборки массива

![Создание RAID](Images/21-mdadm-create.png)

#### 2.3 Сохранение конфигурации массива

Сохраняем конфигурацию в файл `/etc/mdadm.conf`:

```bash
mdadm --detail --scan --verbose | tee -a /etc/mdadm.conf
```

---

### Часть 3: Форматирование и монтирование

#### 3.1 Создание файловой системы

Форматируем массив в файловую систему ext4:

```bash
mkfs.ext4 /dev/md0
```

![Форматирование](Images/22-mkfs.png)

#### 3.2 Проверка UUID массива

```bash
blkid /dev/md0
```

![blkid](Images/23-blkid.png)

Запомните UUID — он понадобится для fstab.

#### 3.3 Создание точки монтирования

```bash
mkdir /raid
```

#### 3.4 Настройка автоматического монтирования

Редактируем файл `/etc/fstab`:

```bash
nano /etc/fstab
```

Добавляем строку:

```
/dev/md0    /raid    ext4    defaults    0    0
```

![fstab](Images/24-fstab.png)

> **Альтернативный вариант** (с использованием UUID):
> ```
> UUID=65f87a3d-2f2a-471a-a04a-b29ccd9b0d55    /raid    ext4    defaults    0    0
> ```

#### 3.5 Монтирование

Выполняем монтирование всех разделов из fstab:

```bash
mount -av
```

![Монтирование](Images/25-mount.png)

---

### Часть 4: Проверка

#### 4.1 Проверка смонтированных разделов

```bash
df -h
```

![Проверка df](Images/26-df.png)

Должен отображаться `/dev/md0` размером ~2 Гб (сумма двух дисков при RAID 0), смонтированный в `/raid`.

#### 4.2 Проверка состояния RAID

```bash
cat /proc/mdstat
```

Или подробная информация:

```bash
mdadm --detail /dev/md0
```

---

## Итоговая проверка

| Проверка | Команда | Ожидаемый результат |
|----------|---------|---------------------|
| Диски в массиве | `lsblk` | sdb и sdc являются частью md0 |
| Состояние RAID | `cat /proc/mdstat` | md0 : active raid0 |
| Файловая система | `blkid /dev/md0` | TYPE="ext4" |
| Монтирование | `df -h \| grep raid` | /dev/md0 смонтирован в /raid |
| Автомонтирование | `cat /etc/fstab` | Строка с /dev/md0 и /raid |

---

## Дополнительная информация

### Уровни RAID

| Уровень | Описание | Минимум дисков | Ёмкость |
|---------|----------|----------------|---------|
| RAID 0 | Чередование (striping) | 2 | 100% (сумма дисков) |
| RAID 1 | Зеркалирование (mirroring) | 2 | 50% (размер одного диска) |
| RAID 5 | Чередование с распределённой чётностью | 3 | (N-1) × размер диска |

### Полезные команды

```bash
# Просмотр состояния всех массивов
cat /proc/mdstat

# Подробная информация о массиве
mdadm --detail /dev/md0

# Остановка массива
mdadm --stop /dev/md0

# Удаление массива
mdadm --remove /dev/md0
```

---

## Возможные проблемы и решения

### Диски не видны в lsblk
- Проверьте, что диски добавлены в виртуальной машине
- Перезагрузите систему после добавления дисков

### Ошибка при создании массива
- Убедитесь, что диски не используются (не смонтированы)
- Выполните зануление суперблоков

### Массив не монтируется автоматически
- Проверьте синтаксис в `/etc/fstab`
- Убедитесь, что директория `/raid` создана
- Проверьте: `mount -av` для диагностики

# Модуль 2. Задание 3: Настройка сервера сетевой файловой системы (NFS)

## Описание задания

- В качестве папки общего доступа выберите `/raid/nfs`, доступ для чтения и записи исключительно для сети в сторону HQ-CLI
- На HQ-CLI настройте автомонтирование в папку `/mnt/nfs`
- Основные параметры сервера отметьте в отчёте

---

## Решение

### Часть 1: Настройка NFS-сервера на HQ-SRV

#### 1.1 Установка пакетов

```bash
apt-get install -y nfs-server nfs-utils
```

#### 1.2 Создание директории общего доступа

Создаём директорию внутри RAID-массива:

```bash
mkdir /raid/nfs
```

#### 1.3 Назначение прав

```bash
chmod 777 /raid/nfs
```

#### 1.4 Настройка экспорта

Редактируем файл `/etc/exports`:

```bash
vim /etc/exports
```

Добавляем строку:

```
/raid/nfs    192.168.200.0/24(rw,no_root_squash)
```

![Настройка exports](Images/27-exports.png)

**Параметры:**
- `/raid/nfs` — общий ресурс (директория для экспорта)
- `192.168.200.0/24` — клиентская сеть, которой разрешено монтирование
- `rw` — разрешены чтение и запись
- `no_root_squash` — отключение ограничения прав root (root на клиенте = root на сервере)

#### 1.5 Экспорт файловой системы

```bash
exportfs -arv
```

![Экспорт NFS](Images/28-exportfs.png)

**Флаги команды:**
- `-a` — экспортировать все каталоги из `/etc/exports`
- `-r` — повторный экспорт всех каталогов (синхронизация)
- `-v` — подробный вывод

#### 1.6 Запуск и автозагрузка NFS-сервера

```bash
systemctl enable --now nfs-server
```

---

### Часть 2: Настройка NFS-клиента на HQ-CLI

#### 2.1 Установка пакетов

```bash
apt-get update && apt-get install -y nfs-utils nfs-clients
```

#### 2.2 Создание точки монтирования

```bash
mkdir /mnt/nfs
```

#### 2.3 Назначение прав

```bash
chmod 777 /mnt/nfs
```

#### 2.4 Настройка автомонтирования

Редактируем файл `/etc/fstab`:

```bash
vim /etc/fstab
```

Добавляем строку:

```
192.168.100.2:/raid/nfs    /mnt/nfs    nfs    defaults    0    0
```

![Настройка fstab на клиенте](Images/29-fstab-nfs.png)

> **Примечание**: `192.168.100.2` — IP-адрес сервера HQ-SRV. Замените на актуальный адрес в вашей сети.

#### 2.5 Монтирование

```bash
mount -av
```

![Монтирование NFS](Images/30-mount-nfs.png)

---

### Часть 3: Проверка

#### 3.1 Проверка на клиенте (HQ-CLI)

```bash
df -h
```

![Проверка df на клиенте](Images/31-df-nfs.png)

Должна отображаться строка с `192.168.100.2:/raid/nfs`, смонтированная в `/mnt/nfs`.

#### 3.2 Проверка записи через файловый менеджер

На HQ-CLI откройте файловый менеджер и перейдите в `/mnt/nfs`. Создайте тестовый файл:

![Файловый менеджер](Images/32-file-manager.png)

#### 3.3 Проверка на сервере (HQ-SRV)

```bash
ls -l /raid/nfs/
```

![Проверка на сервере](Images/33-ls-server.png)

Файл `test.txt`, созданный на клиенте, должен отображаться на сервере.

---

## Итоговая проверка

| Проверка | Где | Команда | Ожидаемый результат |
|----------|-----|---------|---------------------|
| NFS-сервер работает | HQ-SRV | `systemctl status nfs-server` | active (running) |
| Экспорт настроен | HQ-SRV | `exportfs -v` | /raid/nfs с параметрами |
| Ресурс смонтирован | HQ-CLI | `df -h \| grep nfs` | 192.168.100.2:/raid/nfs |
| Запись работает | HQ-CLI | `touch /mnt/nfs/test` | Файл создаётся |
| Файл виден на сервере | HQ-SRV | `ls /raid/nfs/` | test виден |

---

## Основные параметры сервера (для отчёта)

| Параметр | Значение |
|----------|----------|
| Сервер | HQ-SRV (192.168.100.2) |
| Экспортируемая директория | /raid/nfs |
| Разрешённая сеть | 192.168.200.0/24 |
| Права доступа | rw (чтение и запись) |
| Root squash | отключён (no_root_squash) |
| Точка монтирования на клиенте | /mnt/nfs |
| Автомонтирование | через /etc/fstab |

---

## Дополнительные параметры exports

| Параметр | Описание |
|----------|----------|
| `rw` | Чтение и запись |
| `ro` | Только чтение |
| `sync` | Синхронная запись (безопаснее) |
| `async` | Асинхронная запись (быстрее) |
| `no_root_squash` | Root на клиенте = root на сервере |
| `root_squash` | Root на клиенте = nobody на сервере |
| `all_squash` | Все пользователи = nobody |
| `no_subtree_check` | Отключить проверку поддерева |

---

## Полезные команды

```bash
# Просмотр экспортированных ресурсов (на сервере)
exportfs -v

# Просмотр доступных ресурсов на сервере (с клиента)
showmount -e 192.168.100.2

# Принудительное размонтирование
umount -f /mnt/nfs

# Перезагрузка экспорта без перезапуска сервера
exportfs -ra
```

---

## Возможные проблемы и решения

### Ошибка "access denied" при монтировании
- Проверьте IP-адрес клиента в `/etc/exports`
- Убедитесь, что firewall не блокирует NFS (порты 111, 2049)

### Нет прав на запись
- Проверьте параметр `rw` в `/etc/exports`
- Проверьте права на директорию: `chmod 777 /raid/nfs`

### Ресурс не монтируется автоматически
- Проверьте синтаксис в `/etc/fstab`
- Добавьте опцию `_netdev` для сетевых ресурсов:
  ```
  192.168.100.2:/raid/nfs  /mnt/nfs  nfs  defaults,_netdev  0  0
  ```

### Таймаут при монтировании
- Проверьте сетевую связность: `ping 192.168.100.2`
- Убедитесь, что NFS-сервер запущен

# Модуль 2. Задание 4: Настройка службы сетевого времени (Chrony)

## Описание задания

- Вышестоящий сервер NTP на маршрутизаторе ISP — на выбор участника
- Стратум сервера — 5
- В качестве клиентов NTP настройте: HQ-SRV, HQ-CLI, BR-RTR, BR-SRV

---

## Решение

### Часть 1: Настройка NTP-сервера на ISP

#### 1.1 Установка chrony (если не установлен)

```bash
apt-get install -y chrony
```

#### 1.2 Редактирование конфигурации

Редактируем файл `/etc/chrony.conf`:

```bash
vim /etc/chrony.conf
```

Добавляем/изменяем следующие строки:

```conf
# Вышестоящий NTP-сервер (на выбор)
pool pool.ntp.org iburst

# Установка стратума 5
local stratum 5

# Разрешаем синхронизацию для локальных сетей
allow 172.16.4.0/28
allow 172.16.5.0/28
```

![Конфигурация chrony на ISP](Images/35-chrony-conf.png)

**Параметры:**
- `pool pool.ntp.org iburst` — использование пула NTP-серверов
- `local stratum 5` — установка стратума сервера равным 5
- `allow` — разрешение синхронизации для указанных сетей

#### 1.3 Перезапуск службы

```bash
systemctl restart chronyd
systemctl enable chronyd
```

#### 1.4 Проверка работы NTP-сервера

```bash
chronyc tracking
chronyc sources
```

![Проверка chrony на ISP](Images/34-chrony-isp.png)

**Что проверяем:**
- `Stratum: 5` — стратум сервера
- В `chronyc sources` должен отображаться вышестоящий сервер с символом `*`

---

### Часть 2: Настройка NTP-клиентов

#### 2.1 Настройка HQ-RTR и BR-RTR

На маршрутизаторах редактируем `/etc/chrony.conf`:

```bash
vim /etc/chrony.conf
```

Закомментируем стандартные серверы и добавляем ISP:

```conf
# Закомментировать стандартный пул
#pool pool.ntp.org iburst

# Добавить ISP как NTP-сервер
server 172.16.4.1 iburst
```

> **Примечание**: Для BR-RTR используйте `server 172.16.5.1 iburst`

Перезапускаем службу:

```bash
systemctl restart chronyd
```

#### 2.2 Настройка HQ-SRV

Редактируем `/etc/chrony.conf`:

```bash
vim /etc/chrony.conf
```

```conf
#pool pool.ntp.org iburst
server 172.16.1.1 iburst
```

> **Примечание**: Используйте IP-адрес HQ-RTR или ISP, доступный из сети HQ-SRV

Перезапускаем:

```bash
systemctl restart chronyd
```

Проверяем:

```bash
chronyc sources
```

![Проверка chrony на HQ-SRV](Images/37-chrony-hq-srv.png)

#### 2.3 Настройка HQ-CLI

Редактируем `/etc/chrony.conf`:

```bash
vim /etc/chrony.conf
```

```conf
#pool pool.ntp.org iburst
server 172.16.1.1 iburst
```

Перезапускаем:

```bash
systemctl restart chronyd
```

Проверяем:

```bash
chronyc sources
```

![Проверка chrony на HQ-CLI](Images/36-chrony-hq-cli.png)

#### 2.4 Настройка BR-SRV

Аналогично HQ-SRV, редактируем `/etc/chrony.conf`:

```bash
vim /etc/chrony.conf
```

```conf
#pool pool.ntp.org iburst
server 172.16.2.1 iburst
```

> **Примечание**: Используйте IP-адрес BR-RTR или ISP, доступный из сети BR-SRV

Перезапускаем:

```bash
systemctl restart chronyd
```

Проверяем:

```bash
chronyc sources
```

![Проверка chrony на BR-SRV](Images/38-chrony-br-srv.png)

---

## Итоговая проверка

| Устройство | Роль | NTP-сервер | Команда проверки |
|------------|------|------------|------------------|
| ISP | Сервер (stratum 5) | pool.ntp.org | `chronyc tracking` |
| HQ-RTR | Клиент | ISP (172.16.4.1) | `chronyc sources` |
| BR-RTR | Клиент | ISP (172.16.5.1) | `chronyc sources` |
| HQ-SRV | Клиент | HQ-RTR/ISP | `chronyc sources` |
| HQ-CLI | Клиент | HQ-RTR/ISP | `chronyc sources` |
| BR-SRV | Клиент | BR-RTR/ISP | `chronyc sources` |

### Ожидаемый результат `chronyc sources`

```
MS Name/IP address         Stratum Poll Reach LastRx Last sample
===============================================================================
^* 172.16.x.x                    5   6    17    40   -613us[+2976us] +/-   34ms
```

**Символы состояния:**
- `*` — текущий источник синхронизации
- `+` — приемлемый источник
- `-` — источник исключён алгоритмом
- `?` — источник потерял связь

---

## Основные параметры (для отчёта)

| Параметр | Значение |
|----------|----------|
| NTP-сервер | ISP |
| Стратум | 5 |
| Вышестоящий сервер | pool.ntp.org |
| Клиенты | HQ-RTR, BR-RTR, HQ-SRV, HQ-CLI, BR-SRV |
| Порт NTP | 123/UDP |

---

## Полезные команды chrony

```bash
# Статус синхронизации
chronyc tracking

# Список источников времени
chronyc sources

# Подробная информация об источниках
chronyc sourcestats

# Принудительная синхронизация
chronyc makestep

# Список клиентов (на сервере)
chronyc clients

# Проверка конфигурации
chronyd -p
```

---

## Возможные проблемы и решения

### Клиент не синхронизируется
- Проверьте сетевую связность: `ping 172.16.4.1`
- Убедитесь, что на сервере добавлена директива `allow` для сети клиента
- Проверьте firewall: порт 123/UDP должен быть открыт

### Stratum показывает 0 или 16
- Stratum 0 — источник времени (атомные часы, GPS)
- Stratum 16 — сервер не синхронизирован
- Подождите несколько минут после запуска службы

### Источник помечен символом `?`
- Сервер временно недоступен
- Проверьте сеть и статус службы на сервере

### Ошибка "No sources"
- Проверьте правильность IP-адреса в конфигурации
- Убедитесь, что служба chronyd запущена на сервере
