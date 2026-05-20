# build-and-run.ps1

Write-Host "=== Збірка та запуск Docker контейнерів ===" -ForegroundColor Cyan

# Зупинка старих контейнерів
Write-Host "`n1. Зупинка старих контейнерів..." -ForegroundColor Yellow
docker-compose down

# Очищення старих образів
Write-Host "`n2. Очищення старих образів..." -ForegroundColor Yellow
docker system prune -f

# Збірка образів
Write-Host "`n3. Збірка Docker образів..." -ForegroundColor Yellow
docker-compose build --no-cache

# Запуск контейнерів
Write-Host "`n4. Запуск контейнерів..." -ForegroundColor Green
docker-compose up -d

# Очікування запуску
Write-Host "`n5. Очікування запуску контейнерів..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Перевірка статусу
Write-Host "`n6. Статус контейнерів:" -ForegroundColor Green
docker ps

# Логи контейнерів
Write-Host "`n7. Логи FastAPI контейнера:" -ForegroundColor Green
docker logs antonmazur_fastapi --tail 20

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "✅ КОНТЕЙНЕРИ ЗАПУЩЕНО!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "FastAPI: http://localhost:8000" -ForegroundColor Yellow
Write-Host "FastAPI Docs: http://localhost:8000/docs" -ForegroundColor Yellow
Write-Host "PostgreSQL: localhost:5432" -ForegroundColor Yellow
Write-Host "PgAdmin: http://localhost:5050 (admin@antonmazur.com / admin123)" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
