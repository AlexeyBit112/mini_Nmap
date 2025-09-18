from colorama import Fore, Style, init
from typing import Dict, Any, List

init(autoreset=True)  # Initialize colorama

class OutputFormatter:
    """Formats and colors the output of scan results"""
    
    COLORS = {
        'open': Fore.GREEN,
        'closed': Fore.RED,
        'filtered': Fore.YELLOW,
        'error': Fore.MAGENTA,
        'info': Fore.CYAN,
        'warning': Fore.YELLOW
    }
    
    @staticmethod
    def format_port_result(port: int, status: str, banner: str = None) -> str:
        """Format individual port result"""
        color = OutputFormatter.COLORS.get(status, Fore.WHITE)
        result = f"{color}Port {port}: {status.upper()}"
        
        if banner and status == 'open':
            result += f" - Banner: {banner}"
        
        return result + Style.RESET_ALL
    
    @staticmethod
    def format_summary(results: List[Dict[str, Any]], scan_time: float) -> str:
        """Format scan summary"""
        open_ports = [r for r in results if r['status'] == 'open']
        closed_ports = [r for r in results if r['status'] == 'closed']
        
        summary = f"\n{OutputFormatter.COLORS['info']}=== Scan Summary ==="
        summary += f"\nOpen ports: {len(open_ports)}"
        summary += f"\nClosed ports: {len(closed_ports)}"
        summary += f"\nScan time: {scan_time:.2f} seconds"
        summary += Style.RESET_ALL
        
        return summary