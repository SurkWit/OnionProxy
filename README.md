
---

# OnionProxy

## 🇷🇺 Russian

Лёгкий способ запустить локальный SOCKS5-прокси поверх Tor с поддержкой obfs4 мостов для обхода блокировок.

### Что внутри
- Запуск Tor с конфигурацией под выбранный режим
- Поддержка obfs4 мостов (ClientTransportPlugin)
- Проверка выхода в сеть через Tor ([check.torproject.org](https://check.torproject.org))
- Красивый вывод статуса и подсказок по настройке клиентов (Telegram, Discord, браузеры и т.д.)

### Требования
- **Tor**
- **obfs4proxy** (для режима с мостами)
- **Python 3.8+**
- Python-модули: `requests[socks]`, `stem`, `shutil` (встроен в Python)

### Поддерживаемые платформы
- Linux
- macOS
- Termux (Android)

**Примечание**: Windows не поддерживается.

### Установка зависимостей

#### Linux
1. Установите Python 3, Tor и obfs4proxy с помощью пакетного менеджера:
   ```bash
   # Debian/Ubuntu
   sudo apt update && sudo apt install -y python3 python3-pip tor obfs4proxy

   # Fedora
   sudo yum install -y python3 python3-pip tor obfs4proxy

   # Arch
   sudo pacman -S python python-pip tor obfs4proxy
   ```
2. Установите Python-зависимости:
   ```bash
   pip3 install requests[socks] stem
   ```

#### macOS
1. Установите Python 3 и Tor с помощью Homebrew:
   ```bash
   brew install python tor
   ```
2. Установите obfs4proxy вручную (может потребоваться компиляция):
   ```bash
   # Следуйте инструкциям: https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/obfs4
   ```
3. Установите Python-зависимости:
   ```bash
   pip3 install requests[socks] stem
   ```

#### Termux
1. Установите зависимости:
   ```bash
   pkg update && pkg install python tor obfs4proxy
   pip3 install requests[socks] stem
   ```

### Запуск
1. Перейдите в директорию проекта:
   ```bash
   cd /path/to/OnionProxy
   ```
2. (Опционально) Запустите скрипт установки зависимостей:
   ```bash
   bash run.sh
   ```
3. Запустите основной скрипт:
   ```bash
   python3 OnionProxy.py
   ```

После запуска вы увидите данные для подключения (IP, порт, логин/пароль) и инструкции для настройки клиентов (Telegram, Discord, браузеры, Android).

### FAQ
- **obfs4proxy не найден**: Установите пакет `obfs4proxy` или укажите путь к бинарнику через переменную окружения `OBFSPROXY_PATH`.
- **Сайт проверки Tor недоступен**: Попробуйте позже или используйте другой IP.

### Автор
Mono_Seeker ([Telegram](https://t.me/Mono_Seeker))

---

**FU## РКН!**

---

## 🇬🇧 English

A lightweight way to run a local SOCKS5 proxy over Tor with support for obfs4 bridges to bypass censorship.

### Features
- Runs Tor with configuration for the selected mode
- Supports obfs4 bridges (ClientTransportPlugin)
- Verifies Tor network connectivity ([check.torproject.org](https://check.torproject.org))
- Pretty output with status and setup instructions for clients (Telegram, Discord, browsers, etc.)

### Requirements
- **Tor**
- **obfs4proxy** (for bridge mode)
- **Python 3.8+**
- Python modules: `requests[socks]`, `stem`, `shutil` (built into Python)

### Supported Platforms
- Linux
- macOS
- Termux (Android)

**Note**: Windows is not supported.

### Installation

#### Linux
1. Install Python 3, Tor, and obfs4proxy using your package manager:
   ```bash
   # Debian/Ubuntu
   sudo apt update && sudo apt install -y python3 python3-pip tor obfs4proxy

   # Fedora
   sudo yum install -y python3 python3-pip tor obfs4proxy

   # Arch
   sudo pacman -S python python-pip tor obfs4proxy
   ```
2. Install Python dependencies:
   ```bash
   pip3 install requests[socks] stem
   ```

#### macOS
1. Install Python 3 and Tor using Homebrew:
   ```bash
   brew install python tor
   ```
2. Install obfs4proxy manually (may require compilation):
   ```bash
   # Follow instructions: https://gitlab.torproject.org/tpo/anti-censorship/pluggable-transports/obfs4
   ```
3. Install Python dependencies:
   ```bash
   pip3 install requests[socks] stem
   ```

#### Termux
1. Install dependencies:
   ```bash
   pkg update && pkg install python tor obfs4proxy
   pip3 install requests[socks] stem
   ```

### Usage
1. Navigate to the project directory:
   ```bash
   cd /path/to/OnionProxy
   ```
2. (Optional) Run the dependency installation script:
   ```bash
   bash run.sh
   ```
3. Run the main script:
   ```bash
   python3 OnionProxy.py
   ```

Upon starting, you'll see connection details (IP, port, username/password) and setup instructions for clients (Telegram, Discord, browsers, Android).

### FAQ
- **obfs4proxy not found**: Install the `obfs4proxy` package or specify its path via the `OBFSPROXY_PATH` environment variable.
- **Tor check site unavailable**: Try again later or use a different IP.

### Author
Mono_Seeker ([Telegram](https://t.me/Mono_Seeker))

---

**FU## РКН!**

---

