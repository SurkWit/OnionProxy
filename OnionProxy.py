#!/usr/bin/env python3
import os
import time
import subprocess
import sys
import shutil
import platform
from typing import Dict, Optional

try:
    import requests
except Exception:
    requests = None

TOR_DATA_DIR = os.path.expanduser('~/.tor_proxy')
TORRC_PATH = os.path.join(TOR_DATA_DIR, 'torrc')

SOCKS_IP = "127.0.0.1"
USERNAME = "proxyuser"
PASSWORD = "proxypass"

TOR_CHECK_URL = "https://check.torproject.org/api/ip"

PROTOCOLS = {
    "2": {
        "name": "SOCKS5 + obfs4 мосты",
        "port": 1081,
        "bridges": [
            "obfs4 64.23.136.154:53640 969202413807802849B9CCF6D781B0DAC3C255E8 cert=pACn2AIVKFDJqlMMcv5uPKZ34Y8rnKyDe0cbxHIuUsdLtzY/O3I3JkfbzJ4LpoXdtWv4Mw iat-mode=0",
            "obfs4 91.229.62.14:8042 60FBE30CDAD05EA2E43A84A03303811C74C71E2A cert=viLwWECfGgkNnVUEG1Sr1KD58JXBizufcENJwtaqoI9/cP2xYHY/HBY5HGrHpdI/ZM3/Og iat-mode=0",
            "obfs4 51.38.220.35:42954 B84BDFE3724928B06FC178FF50D5852E5AB7942A cert=6tpTDdnOaRl2elQqdxSmrJ5Gt9JkWcbquznpxx/lqVjRKv/bVecFnXie96KoblCWfvVjYA iat-mode=0",
            "obfs4 51.38.220.224:30996 22494A012CFA8C88B1D907E2CCB8409AC35B537B cert=dOPijSCG6FD89fYv5N2F9QoeK1od3tpG6VBE/kMY0Bt1aW/7aXPIzsENDoLWZe43gI8efw iat-mode=0"
        ],
        "transport": "obfs4",
        "description": "SOCKS5 с obfs4 мостами для обхода блокировок"
    }
}

def print_banner():
    banner = r"""
                                                   
█▀█ █▄░█ █ █▀█ █▄░█ █▀█ █▀█ █▀█ ▀▄▀ █▄█
█▄█ █░▀█ █ █▄█ █░▀█ █▀▀ █▀▄ █▄█ █░█ ░█░

Author: Mono_Seeker(tg)
    """
    print("\033[1;35m" + banner + "\033[0m")
    print("\033[1;36m" + "🌟 Добро пожаловать в OnionProxy - ваш универсальный прокси-сервер! 🌟" + "\033[0m")
    print("\033[1;36m" + "=" * 70 + "\033[0m")

def show_protocol_menu():
    print("\033[1;33m🔧 Выберите протокол прокси (или 'i' — инструкции):\033[0m")
    print("\033[1;36m" + "─" * 70 + "\033[0m")
    
    print("\033[1;34m📡 Базовые протоколы:\033[0m")
    for key in PROTOCOLS:
        protocol = PROTOCOLS[key]
        icon = "🔒" if "obfs4" in protocol.get('transport', '') else "🌐"
        print(f"  \033[1;32m{key}.\033[0m {icon} \033[1;37m{protocol['name']}\033[0m")
        print(f"     \033[0;33m{protocol['description']}\033[0m")
        print(f"     \033[0;36m📍 Порт: {protocol['port']}\033[0m")
        if protocol['bridges']:
            print(f"     \033[0;35m🌉 Мосты: {len(protocol['bridges'])} шт.\033[0m")
        print()
    
    print("\033[1;36m" + "─" * 70 + "\033[0m")
    
    while True:
        try:
            choice = input("\033[1;33mВведите номер протокола (2) или 'i' для инструкций: \033[0m").strip()
            if choice.lower() == 'i':
                print_install_instructions()
                print("\033[1;36m" + "-" * 60 + "\033[0m")
                continue
            if choice in PROTOCOLS:
                return choice
            else:
                print("\033[1;31m❌ Неверный выбор! Попробуйте снова.\033[0m")
        except KeyboardInterrupt:
            print("\n\033[1;31m❌ Отменено пользователем\033[0m")
            sys.exit(1)

def create_tor_config(protocol_config):
    os.makedirs(TOR_DATA_DIR, exist_ok=True)

    hashed_pw = subprocess.getoutput(f"tor --hash-password {PASSWORD}")
    
    port = protocol_config['port']
    bridges = protocol_config['bridges']
    
    config_content = f"""
DataDirectory {TOR_DATA_DIR}
ControlPort 9051
HashedControlPassword {hashed_pw}
"""

    config_content += f"SocksPort {SOCKS_IP}:{port}\n"

    if bridges:
        transport = protocol_config.get('transport')
        config_content += "\nUseBridges 1\n"

        if transport == 'obfs4':
            obfs4_path = resolve_obfs4proxy_path()
            if obfs4_path:
                config_content += f"ClientTransportPlugin obfs4 exec {obfs4_path}\n"
            else:
                print("\033[1;33m⚠️  obfs4proxy не найден. Установите obfs4proxy и укажите путь через переменную окружения OBFSPROXY_PATH.\033[0m")
            for bridge in bridges:
                config_content += f"Bridge {bridge}\n"

    with open(TORRC_PATH, 'w') as f:
        f.write(config_content)

    return TORRC_PATH

def resolve_obfs4proxy_path() -> Optional[str]:
    env_path = os.environ.get('OBFS4PROXY_PATH')
    if env_path and os.path.isfile(env_path):
        return env_path
    candidate = shutil.which('obfs4proxy')
    if candidate:
        return candidate
    termux_path = '/data/data/com.termux/files/usr/bin/obfs4proxy'
    if os.path.isfile(termux_path):
        return termux_path
    return None

def _build_requests_proxies(protocol_config) -> Dict[str, str]:
    port = protocol_config['port']
    return {
        'http': f'socks5h://{SOCKS_IP}:{port}',
        'https': f'socks5h://{SOCKS_IP}:{port}',
    }

def test_tor_connection(protocol_config, retries: int = 8, delay_seconds: int = 3) -> bool:
    global requests
    if requests is None:
        if not auto_install_requests():
            print("\033[1;31m❌ Не удалось установить 'requests'. Установите вручную: pip install requests[socks]\033[0m")
            return False
        try:
            import requests as _requests
            requests = _requests
        except Exception:
            return False

    proxies = _build_requests_proxies(protocol_config)
    print("\033[1;33m🔎 Проверяем подключение через сайт (Tor check)...\033[0m")

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(TOR_CHECK_URL, proxies=proxies, timeout=25)
            if response.status_code == 200:
                content_type = (response.headers.get('Content-Type') or '').lower()
                ip: Optional[str] = None
                is_tor: Optional[bool] = None

                if 'application/json' in content_type:
                    data = response.json()
                    ip = data.get('IP') or data.get('ip')
                    is_tor = data.get('IsTor')
                else:
                    ip = response.text.strip()

                if is_tor is True:
                    print(f"\033[1;32m✅ Соединение активно через Tor. Выходной IP: {ip}\033[0m")
                else:
                    print(f"\033[1;33m⚠️  Получен ответ. IP: {ip or 'неизвестен'}. Не удалось подтвердить признак Tor.\033[0m")
                return True
            else:
                print(f"\033[1;33m⏳ Попытка {attempt}/{retries}: статус {response.status_code}\033[0m")
        except Exception as e:
            print(f"\033[1;33m⏳ Попытка {attempt}/{retries} не удалась: {e}\033[0m")
        time.sleep(delay_seconds)

    print("\033[1;31m❌ Не удалось подтвердить работу через сайт. Попробуйте позже.\033[0m")
    return False

def auto_install_requests() -> bool:
    try:
        print("\033[1;33m🛠️  Устанавливаем зависимость: requests[socks]...\033[0m")
        cmd = [sys.executable, '-m', 'pip', 'install', '--user', 'requests[socks]']
        result = subprocess.run(cmd, capture_output=True)
        if result.returncode != 0:
            cmd = [sys.executable, '-m', 'pip', 'install', 'requests[socks]']
            result = subprocess.run(cmd, capture_output=True)
        success = result.returncode == 0
        if success:
            print("\033[1;32m✓ requests установлен\033[0m")
        else:
            print("\033[1;31m✗ Ошибка установки requests:\033[0m")
            try:
                stderr = result.stderr.decode(errors='ignore')
                if stderr:
                    print(stderr)
            except Exception:
                pass
        return success
    except Exception as e:
        print(f"\033[1;31m✗ Сбой установки requests: {e}\033[0m")
        return False

def print_install_instructions() -> None:
    os_name = platform.system()
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;33mИнструкции по установке Tor и транспортов\033[0m")
    print("\033[1;36m" + "-" * 60 + "\033[0m")

    print("\033[1;37mTor\033[0m:")
    if os_name == 'Windows':
        print("  1) Установите Tor (Expert Bundle):")
        print("     - winget: 'winget install TorProject.Tor' (если доступен)")
        print("     - Chocolatey: 'choco install tor' (если установлен Chocolatey)")
        print("     - Либо скачайте с сайта Tor Project: [Tor Expert Bundle](https://www.torproject.org/download/tor/)")
    elif os_name == 'Darwin':
        print("  1) macOS: 'brew install tor' (через Homebrew)")
    else:
        print("  1) Linux: используйте пакетный менеджер (apt/yum/pacman): 'sudo apt install tor'")
    print()

    print("\033[1;37mobfs4proxy\033[0m:")
    print("  - Часто ставится отдельным пакетом: 'sudo apt install obfs4proxy' (Linux)")
    print("  - На Windows скачайте бинарник или используйте сборки из репозиториев, затем укажите путь в переменной OBFSPROXY_PATH")
    print("  - Termux: 'pkg install obfs4proxy'")
    print()

    print("\033[1;37mPython-зависимости\033[0m:")
    print("  - Автоустановка 'requests[socks]' выполняется скриптом при первом запуске")
    print("\033[1;36m" + "=" * 60 + "\033[0m")

def display_proxy_info(protocol_config):
    protocol_name = protocol_config['name']
    port = protocol_config['port']
    
    print("\033[1;32m✅ Proxy успешно запущен!\033[0m")
    print("\033[1;36m" + "=" * 60 + "\033[0m")
    print("\033[1;33m📋 ДАННЫЕ ДЛЯ ПОДКЛЮЧЕНИЯ:\033[0m")
    print("\033[1;36m" + "-" * 60 + "\033[0m")
    
    print(f"\033[1;37m🔧 Протокол:\033[0m \033[1;32m{protocol_name}\033[0m")
    print(f"\033[1;37m🌐 IP адрес:\033[0m \033[1;32m{SOCKS_IP}\033[0m")
    print(f"\033[1;37m🚪 Порт:\033[0m \033[1;32m{port}\033[0m")
    
    print(f"\033[1;37m👤 Имя пользователя:\033[0m \033[1;32m{USERNAME}\033[0m")
    print(f"\033[1;37m🔐 Пароль:\033[0m \033[1;32m{PASSWORD}\033[0m")
    print(f"\033[1;37m📱 Тип прокси:\033[0m \033[1;32mSOCKS5\033[0m")
    
    print("\033[1;36m" + "-" * 60 + "\033[0m")
    
    print("\033[1;33m📱 НАСТРОЙКА В ПРИЛОЖЕНИЯХ:\033[0m")
    print("\033[1;36m" + "-" * 60 + "\033[0m")
    
    print("\033[1;34m🔷 Telegram:\033[0m")
    print("   Настройки → Данные и память → Настройки прокси")
    print(f"   Тип: SOCKS5 | Сервер: {SOCKS_IP} | Порт: {port}")
    print(f"   Логин: {USERNAME} | Пароль: {PASSWORD}")
    print()
    
    print("\033[1;34m🔷 Discord:\033[0m")
    print("   Настройки → Голос и видео → Настройки прокси")
    print(f"   Тип: SOCKS5 | Хост: {SOCKS_IP} | Порт: {port}")
    print(f"   Имя пользователя: {USERNAME} | Пароль: {PASSWORD}")
    print()
    
    print("\033[1;34m🔷 Браузеры:\033[0m")
    print("   Настройки → Сеть → Прокси → Ручная настройка")
    print(f"   SOCKS Host: {SOCKS_IP} | Port: {port} | SOCKS v5")
    print()
    
    print("\033[1;34m🔷 Системные настройки Android:\033[0m")
    print("   WiFi → Дополнительно → Прокси → Ручная настройка")
    print(f"   Хост: {SOCKS_IP} | Порт: {port}")
    
    if protocol_config['bridges']:
        print(f"\n\033[1;35m🌉 Используются мосты:\033[0m \033[1;32m{len(protocol_config['bridges'])} obfs4 мостов\033[0m")
        print("\033[1;33m   ⚡ Повышенная защита от блокировок\033[0m")
    
    print("\033[1;36m" + "=" * 60 + "\033[0m")

def start_tor(protocol_config):
    return start_tor_proxy(protocol_config)

def start_tor_proxy(protocol_config):
    config_path = create_tor_config(protocol_config)

    print(f"\033[1;33m🚀 Запускаем Tor с протоколом {protocol_config['name']}...\033[0m")
    
    process = subprocess.Popen(
        ['tor', '-f', config_path],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE
    )

    print("\033[1;33m⏳ Инициализация соединения...\033[0m")
    time.sleep(10)
    
    return process

def main():
    print_banner()

    try:
        subprocess.run(['tor', '--version'], check=True, capture_output=True)
    except:
        print("\033[1;31m❌ Tor не установлен! Установите: pkg install tor\033[0m")
        return

    try:
        subprocess.run(['obfs4proxy', '-version'], check=True, capture_output=True)
    except:
        print("\033[1;33m⚠️  obfs4proxy не найден. Мосты могут не работать.")
        print("   Установите: pkg install obfs4proxy\033[0m")
        time.sleep(3)

    # Автоматический выбор протокола без запроса у пользователя
    protocol_choice = '2'
    selected_protocol = PROTOCOLS[protocol_choice]
    
    print(f"\033[1;32m✓ Выбран протокол: {selected_protocol['name']}\033[0m")
    time.sleep(1)

    tor_process = start_tor(selected_protocol)
    if not tor_process:
        print("\033[1;31m❌ Не удалось запустить Tor\033[0m")
        return

    display_proxy_info(selected_protocol)

    test_tor_connection(selected_protocol)

    try:
        print("\n\033[1;33m💡 Прокси работает в фоне...")
        print("Нажмите Ctrl+C для остановки\033[0m")
        
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        pass
    finally:
        print("\n\033[1;31m🛑 Останавливаем прокси...\033[0m")
        tor_process.terminate()
        tor_process.wait()
        print("\033[1;32m✅ Прокси остановлен\033[0m")

if __name__ == "__main__":
    main()