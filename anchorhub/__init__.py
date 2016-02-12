"""
AnchorHub - a Markdown pre-compiler for utilizing GitHub's auto-generated anchors
"""

__all__ = ['__version__']

# AnchorHub version
import pkgutil
__version__ = pkgutil.get_data('anchorhub', 'VERSION').decode('ascii').strip()
del pkgutil
