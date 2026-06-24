#!/usr/bin/env bash
# Устанавливает GiveawayBot как systemd-сервис на Linux.
# Запускать на сервере под root (sudo): sudo bash deploy/install.sh
set -euo pipefail

APP_DIR="/var/giveaway_bot"
SERVICE_USER="giveaway"
SERVICE_FILE="giveaway-bot.service"

if [[ "$EUID" -ne 0 ]]; then
  echo "Запустите скрипт с правами root: sudo bash deploy/install.sh" >&2
  exit 1
fi

if [[ "$(pwd)" != "$APP_DIR" ]]; then
  echo "Скрипт ожидает, что код бота уже находится в $APP_DIR" >&2
  echo "Текущая директория: $(pwd)" >&2
  exit 1
fi

if ! id "$SERVICE_USER" &>/dev/null; then
  useradd --system --create-home --shell /usr/sbin/nologin "$SERVICE_USER"
  echo "Создан системный пользователь $SERVICE_USER"
fi

if [[ ! -d "$APP_DIR/venv" ]]; then
  python3 -m venv "$APP_DIR/venv"
  echo "Создан venv в $APP_DIR/venv"
fi

"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/requirements.txt"

chown -R "$SERVICE_USER:$SERVICE_USER" "$APP_DIR"

install -m 644 "$APP_DIR/deploy/$SERVICE_FILE" "/etc/systemd/system/$SERVICE_FILE"

systemctl daemon-reload
systemctl enable "$SERVICE_FILE"
systemctl restart "$SERVICE_FILE"

echo "Готово. Статус: systemctl status $SERVICE_FILE"
echo "Логи: journalctl -u $SERVICE_FILE -f"
