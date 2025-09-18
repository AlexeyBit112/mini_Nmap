from typing import List, Dict, Any, Union
import time
from .port_strategy import PortScanStrategy, TCPConnectStrategy
from ..utils.validator import InputValidator
from ..utils.logger import ScannerLogger
from ..utils.output_formatter import OutputFormatter
from ..exceptions import ValidationError

class PortScanner:
    """Main port scanner class with comprehensive functionality"""
    
    def __init__(self, strategy: PortScanStrategy = None, timeout: float = 1.0):
        self.strategy = strategy or TCPConnectStrategy(timeout)
        self.validator = InputValidator()
        self.logger = ScannerLogger(__name__)
        self.output_formatter = OutputFormatter()
    
    def scan(self, target: str, ports: Union[str, List[int], int]) -> List[Dict[str, Any]]:
        """Perform port scan on target"""
        start_time = time.time()
        
        try:
            # Validate input
            validated_target = self.validator.validate_ip_address(target)
            port_list = self._parse_ports(ports)
            
            self.logger.info(f"Starting scan of {len(port_list)} ports on {validated_target}")
            
            # Perform scan
            results = self.strategy.scan_ports(validated_target, port_list)
            
            # Calculate scan time
            scan_time = time.time() - start_time
            
            # Display results
            self._display_results(results, scan_time)
            
            return results
            
        except ValidationError as e:
            self.logger.error(f"Validation error: {e}")
            raise
        except Exception as e:
            self.logger.error(f"Scan failed: {e}")
            raise
    
    def _parse_ports(self, ports: Union[str, List[int], int]) -> List[int]:
        """Parse ports input into list of port numbers"""
        if isinstance(ports, int):
            return [self.validator.validate_port(ports)]
        
        elif isinstance(ports, str):
            if '-' in ports:
                # Port range
                start, end = self.validator.validate_port_range(ports)
                return list(range(start, end + 1))
            elif ',' in ports:
                # Comma-separated ports
                port_list = []
                for port_str in ports.split(','):
                    port_list.append(self.validator.validate_port(int(port_str.strip())))
                return port_list
            else:
                # Single port
                return [self.validator.validate_port(int(ports))]
        
        elif isinstance(ports, list):
            if len(ports) == 2:
                # Port range as list
                start, end = self.validator.validate_port_range(ports)
                return list(range(start, end + 1))
            else:
                # List of ports
                return [self.validator.validate_port(port) for port in ports]
        
        else:
            raise ValidationError("Invalid ports format")
    
    def _display_results(self, results: List[Dict[str, Any]], scan_time: float):
        """Display scan results in formatted output"""
        for result in results:
            formatted = self.output_formatter.format_port_result(
                result['port'], result['status'], result.get('banner')
            )
            print(formatted)
        
        print(self.output_formatter.format_summary(results, scan_time))