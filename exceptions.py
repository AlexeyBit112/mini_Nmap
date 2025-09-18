class ScannerError(Exception):
    """Base exception for scanner errors"""
    pass

class ValidationError(ScannerError):
    """Raised when input validation fails"""
    pass

class ConnectionError(ScannerError):
    """Raised when connection fails"""
    pass

class TimeoutError(ScannerError):
    """Raised when operation times out"""
    pass