import ipaddress
import re
from typing import Union, List
from ..exceptions import ValidationError

class InputValidator:
    """Validates input parameters for the scanner"""
    
    @staticmethod
    def validate_ip_address(ip: str) -> str:
        """Validate IP address format"""
        try:
            ipaddress.ip_address(ip)
            return ip
        except ValueError:
            raise ValidationError(f"Invalid IP address: {ip}")
    
    @staticmethod
    def validate_port(port: int) -> int:
        """Validate port number"""
        if not 1 <= port <= 65535:
            raise ValidationError(f"Port must be between 1 and 65535: {port}")
        return port
    
    @staticmethod
    def validate_port_range(port_range: Union[str, List[int]]) -> List[int]:
        """Validate and parse port range"""
        if isinstance(port_range, list):
            if len(port_range) != 2:
                raise ValidationError("Port range must contain exactly 2 values")
            start, end = port_range
        else:
            # Parse string like "1-100"
            if not re.match(r'^\d+-\d+$', port_range):
                raise ValidationError("Port range must be in format 'start-end'")
            start, end = map(int, port_range.split('-'))
        
        start = InputValidator.validate_port(start)
        end = InputValidator.validate_port(end)
        
        if start > end:
            raise ValidationError("Start port cannot be greater than end port")
        
        return [start, end]
    
    @staticmethod
    def validate_timeout(timeout: float) -> float:
        """Validate timeout value"""
        if timeout <= 0:
            raise ValidationError("Timeout must be positive")
        return timeout