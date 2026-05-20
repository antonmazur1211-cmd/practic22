Write-Host "=== ТЕСТУВАННЯ CRUD API ===" -ForegroundColor Cyan

Write-Host "`n1. Створення користувача..." -ForegroundColor Yellow
$user = @{
    name = "Anton Mazur"
    email = "anton@example.com"
    age = 25
} | ConvertTo-Json

$response = Invoke-RestMethod -Uri "http://localhost:8000/users/" -Method Post -Body $user -ContentType "application/json"
Write-Host "✅ Створено: $($response | ConvertTo-Json)" -ForegroundColor Green

Write-Host "`n2. Отримання всіх користувачів..." -ForegroundColor Yellow
$users = Invoke-RestMethod -Uri "http://localhost:8000/users/" -Method Get
Write-Host "✅ Користувачі: $($users | ConvertTo-Json)" -ForegroundColor Green

Write-Host "`n3. Отримання користувача за ID..." -ForegroundColor Yellow
$user = Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Get
Write-Host "✅ Знайдено: $($user | ConvertTo-Json)" -ForegroundColor Green

Write-Host "`n4. Оновлення користувача..." -ForegroundColor Yellow
$update = @{
    name = "Anton Mazur Updated"
    age = 26
} | ConvertTo-Json
$updated = Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Put -Body $update -ContentType "application/json"
Write-Host "✅ Оновлено: $($updated | ConvertTo-Json)" -ForegroundColor Green

Write-Host "`n5. Статистика..." -ForegroundColor Yellow
$stats = Invoke-RestMethod -Uri "http://localhost:8000/users/stats/count" -Method Get
Write-Host "✅ Кількість користувачів: $($stats.count)" -ForegroundColor Green

Write-Host "`n6. Видалення користувача..." -ForegroundColor Yellow
Invoke-RestMethod -Uri "http://localhost:8000/users/1" -Method Delete
Write-Host "✅ Видалено" -ForegroundColor Green

Write-Host "`n=== ТЕСТУВАННЯ ЗАВЕРШЕНО ===" -ForegroundColor Cyan
