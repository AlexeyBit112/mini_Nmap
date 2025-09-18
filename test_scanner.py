import unittest
from unittest.mock import Mock, patch
from scanner.core.scanner import PortScanner
from scanner.core.port_strategy import TCPConnectStrategy
from scanner.exceptions import ValidationError

class TestPortScanner(unittest.TestCase):
    
    def setUp(self):
        self.scanner = PortScanner()
    
    def test_validate_ip_address(self):
        # Valid IPs
        self.scanner.validator.validate_ip_address("192.168.1.1")
        self.scanner.validator.validate_ip_address("8.8.8.8")
        
        # Invalid IPs
        with self.assertRaises(ValidationError):
            self.scanner.validator.validate_ip_address("invalid_ip")
        with self.assertRaises(ValidationError):
            self.scanner.validator.validate_ip_address("256.256.256.256")
    
    def test_parse_ports(self):
        # Single port
        self.assertEqual(self.scanner._parse_ports(80), [80])
        self.assertEqual(self.scanner._parse_ports("80"), [80])
        
        # Port range
        self.assertEqual(self.scanner._parse_ports("1-3"), [1, 2, 3])
        self.assertEqual(self.scanner._parse_ports([1, 3]), [1, 2, 3])
        
        # Multiple ports
        self.assertEqual(self.scanner._parse_ports("80,443"), [80, 443])
        
        # Invalid ports
        with self.assertRaises(ValidationError):
            self.scanner._parse_ports(0)
        with self.assertRaises(ValidationError):
            self.scanner._parse_ports(65536)

if __name__ == "__main__":
    unittest.main()