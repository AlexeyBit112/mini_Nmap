#!/usr/bin/env python3
"""
Mini Nmap - Python Port Scanner
Entry point for the application
"""

import argparse
from scanner.core.scanner import PortScanner
from scanner.core.port_strategy import TCPConnectStrategy
from scanner.utils.logger import ScannerLogger

def main():
    """Main function to run the port scanner"""
    parser = argparse.ArgumentParser(description="Mini Nmap - Python Port Scanner")
    parser.add_argument("target", help="Target IP address to scan")
    parser.add_argument("-p", "--ports", default="1-1000", 
                       help="Ports to scan (e.g., 80, 1-1000, 22,80,443)")
    parser.add_argument("-t", "--timeout", type=float, default=1.0,
                       help="Timeout for connection attempts (seconds)")
    parser.add_argument("-v", "--verbose", action="store_true",
                       help="Enable verbose logging")
    
    args = parser.parse_args()
    
    # Setup logger
    log_level = "DEBUG" if args.verbose else "INFO"
    logger = ScannerLogger("mini-nmap", getattr(logging, log_level.upper()))
    
    try:
        # Create and run scanner
        strategy = TCPConnectStrategy(timeout=args.timeout)
        scanner = PortScanner(strategy=strategy, timeout=args.timeout)
        
        scanner.scan(args.target, args.ports)
        
    except KeyboardInterrupt:
        logger.info("Scan interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    import sys
    import logging
    sys.exit(main())