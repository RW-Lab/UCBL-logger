# ucbl_logger/__init__.py

from .logger import UCBLLogger, UCBLLoggerFactory, LogLevel
from .interfaces import ILogger, ITaskLogger, IRiskLogger

# Enhanced EKS components (optional import for backward compatibility)
try:
    from .enhanced import (
        IEnhancedEKSLogger,
        EnhancedEKSLoggerBase,
        EnhancedEKSLogger,
        EnhancedEKSLoggerFactory,
        EnhancedEKSConfig,
        ConfigurationManager,
        LoggerInitializer,
        initialize_enhanced_logger,
        quick_setup,
        InitializationError,
        SamplingConfig,
        BufferConfig,
        PerformanceThresholds,
        HealthStatus,
        EnhancedLogEntry
    )
    _enhanced_available = True
except ImportError:
    _enhanced_available = False

__all__ = ['UCBLLogger', 'UCBLLoggerFactory', 'LogLevel', 'ILogger', 'ITaskLogger', 'IRiskLogger']

# Fargate logger (always available — no heavy dependencies)
from .fargate_logger import FargateLogger
from .enhanced.factory import FargateLoggerFactory
__all__.extend(['FargateLogger', 'FargateLoggerFactory'])

# Add enhanced components to __all__ if available
if _enhanced_available:
    __all__.extend([
        'IEnhancedEKSLogger',
        'EnhancedEKSLoggerBase',
        'EnhancedEKSLogger',
        'EnhancedEKSLoggerFactory',
        'EnhancedEKSConfig',
        'ConfigurationManager',
        'LoggerInitializer',
        'initialize_enhanced_logger',
        'quick_setup',
        'InitializationError',
        'SamplingConfig',
        'BufferConfig',
        'PerformanceThresholds',
        'HealthStatus',
        'EnhancedLogEntry'
    ])
