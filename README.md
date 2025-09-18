# mini_Nmap
 Python Port Scanner

A simple Python script that scans open ports on a target host, similar to a basic Nmap functionality.

## Features
- TCP port scanning
- Banner grabbing (if service responds)
- Customizable port range

## Requirements
- Python 3.8+
- socket (built-in)
- Optional: colorama for colored terminal output

## Usage
```bash
python scanner.py <target_ip>

🎯 Usage
# Basic scan
python main.py 127.0.0.1 -p 80,443

# Port range scan
python main.py example.com -p 1-1000

# With custom timeout
python main.py 192.168.1.1 -p 22,80,443 -t 0.5

# Verbose mode
python main.py 8.8.8.8 -p 53,80,443 -v


🧪 Testing
# Run all tests
python -m unittest discover tests/

# Run specific test
python -m unittest tests.test_scanner
