#!/bin/bash
# Установка Docker на Debian 12 (Bookworm) — ОДИН скрипт!
# запустить скрипт или выполнить эти команды поочереди в консоли

set -e  # Остановка при ошибке

echo "🐳 Установка Docker на $(lsb_release -ds)..."

# 1. Обновление системы
echo "📦 Обновление системы..."
apt update && apt upgrade -y
  
# 2. Зависимости
echo "🔧 Установка зависимостей..."
apt install -y ca-certificates curl gnupg lsb-release

# 3. GPG ключ
echo "🔑 Добавление GPG ключа Docker..."
install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
chmod a+r /etc/apt/keyrings/docker.gpg

# 4. Репозиторий
echo "📂 Добавление репозитория..."
echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
  $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Установка Docker
echo "🐳 Установка Docker..."
apt update
apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# 6. Запуск службы
echo "▶️ Запуск Docker..."
systemctl enable --now docker

# 7. Права пользователя
echo "👤 Добавление пользователя в группу docker..."
usermod -aG docker $USER

# 8. Проверка
echo "✅ ПРОВЕРКА..."
docker --version
docker run --rm hello-world | grep "Hello from Docker!"

echo ""
echo "🎉 ✅ Docker установлен!"
echo "🔄 **ПЕРЕЛОГИНИТЕСЬ** и проверьте: docker run hello-world"
echo "📱 docker-compose: docker compose version"
