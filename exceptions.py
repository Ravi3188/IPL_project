class IPLDataError(Exception):
    """Exception raised for errors in loading IPL data."""
    def __init__(self, message="Error loading IPL data"):
        super().__init__(message)

class IPLDatabaseError(Exception):
    """Exception raised for errors in database operations."""
    def __init__(self, message="Database operation failed"):
        super().__init__(message)

class IPLReportError(Exception):
    """Exception raised for errors in report generation or queries."""
    def __init__(self, message="Report generation failed"):
        super().__init__(message)
