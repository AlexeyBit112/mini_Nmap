#!/usr/bin/env python3
"""
Простой тест для проверки работы сканера
"""

from scanner.core.scanner import PortScanner

def test_scanner():
    print("🔍 Тестирование Mini Nmap...")
    
    try:
        scanner = PortScanner()
        
        # Тестируем на localhost
        print("Сканируем порты 80 и 443 на localhost...")
        results = scanner.scan("127.0.0.1", [80, 443])
        
        print("✅ Тест пройден успешно!")
        print(f"Найдено результатов: {len(results)}")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    test_scanner()