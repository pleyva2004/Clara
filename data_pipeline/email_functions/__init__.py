"""
Email functions package initialization
"""

from .email_reader import getEmail
from .email_listener import check_new_emails, monitor_inbox

__all__ = ['getEmail', 'check_new_emails', 'monitor_inbox']