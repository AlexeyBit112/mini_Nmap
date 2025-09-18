from abc import ABC, abstractmethod
from typing import List, Dict, Any
import socket
import concurrent.futures
from ..exceptions import ConnectionError, TimeoutError
from ..utils.logger import ScannerLogger

class PortScanStrategy(ABC):
    """Abstract base class for port scanning strategies"""
    
    def __init__(self, timeout: float = 1.0):
        self.timeout = timeout
        self.logger = ScannerLogger(__name__)
    
    @abstractmethod
    def scan_port(self, target: str, port: int) -> Dict[str, Any]:
        """Scan a single port and return result"""
        pass
    
    def scan_ports(self, target: str, ports: List[int], max_workers: int = 100) -> List[Dict[str, Any]]:
        """Scan multiple ports concurrently"""
        results = []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_port = {
                executor.submit(self.scan_port, target, port): port 
                for port in ports
            }
            
            for future in concurrent.futures.as_completed(future_to_port):
                port = future_to_port[future]
                try:
                    result = future.result()
                    results.append(result)
                except Exception as e:
                    self.logger.error(f"Error scanning port {port}: {e}")
                    results.append({
                        'port': port,
                        'status': 'error',
                        'banner': str(e)
                    })
        
        return sorted(results, key=lambda x: x['port'])

class TCPSynStrategy(PortScanStrategy):
    """TCP SYN scan strategy (requires root privileges)"""
    
    def scan_port(self, target: str, port: int) -> Dict[str, Any]:
        # Implementation would require raw sockets (root privileges)
        # This is a placeholder for a more advanced implementation
        raise NotImplementedError("TCP SYN scan requires root privileges")

class TCPConnectStrategy(PortScanStrategy):
    """TCP Connect scan strategy (works without root privileges)"""
    
    def scan_port(self, target: str, port: int) -> Dict[str, Any]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.settimeout(self.timeout)
                result = sock.connect_ex((target, port))
                
                if result == 0:
                    banner = self._grab_banner(sock)
                    return {
                        'port': port,
                        'status': 'open',
                        'banner': banner
                    }
                else:
                    return {
                        'port': port,
                        'status': 'closed',
                        'banner': None
                    }
                        
        except socket.timeout:
            raise TimeoutError(f"Timeout scanning port {port}")
        except Exception as e:
            raise ConnectionError(f"Error scanning port {port}: {e}")
    
    def _grab_banner(self, sock: socket.socket) -> str:
        """Attempt to grab banner from open port"""
        try:
            sock.send(b'HEAD / HTTP/1.1\r\n\r\n')
            banner = sock.recv(1024).decode('utf-8', errors='ignore').strip()
            return banner if banner else "No banner"
        except:
            return "Banner grab failed"