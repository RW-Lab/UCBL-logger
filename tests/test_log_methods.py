import unittest
import logging
import os
from io import StringIO
from ucbl_logger.logger import UCBLLogger

class TestLogMethods(unittest.TestCase):

    def setUp(self):
        # Disable enhanced features for testing
        os.environ['UCBL_DISABLE_EKS_FEATURES'] = 'true'
        
        self.log_stream = StringIO()
        self.logger = UCBLLogger(log_level=logging.INFO, enable_eks_features=False)
        self.stream_handler = logging.StreamHandler(self.log_stream)
        
        # Access the standard logger
        if hasattr(self.logger, '_standard_logger') and self.logger._standard_logger:
            self.logger._standard_logger.logger.addHandler(self.stream_handler)
            if hasattr(self.logger._standard_logger, 'task_type'):
                self.logger._standard_logger.task_type = "User"
            if hasattr(self.logger._standard_logger, 'stack_level'):
                self.logger._standard_logger.stack_level = 2

    def tearDown(self):
        if hasattr(self.logger, '_standard_logger') and self.logger._standard_logger:
            self.logger._standard_logger.logger.handlers = []
        # Clean up environment
        if 'UCBL_DISABLE_EKS_FEATURES' in os.environ:
            del os.environ['UCBL_DISABLE_EKS_FEATURES']

    def test_log_risk(self):
        self.logger.log_risk("Test Risk")
        log_output = self.log_stream.getvalue()
        self.assertIn("Test Risk", log_output)

    def test_log_anomaly(self):
        """
        Test the log_anomaly method to ensure it logs anomalies correctly.
        """
        self.logger.log_anomaly("Anomaly detected")
        log_output = self.log_stream.getvalue()
        self.assertIn("Anomaly detected", log_output)

    def test_log_suspicious_activity(self):
        """
        Test the log_suspicious_activity method to ensure it logs suspicious activity correctly.
        """
        self.logger.log_suspicious_activity("Suspicious activity")
        log_output = self.log_stream.getvalue()
        self.assertIn("Suspicious activity", log_output)

    def test_log_goal_start_stop(self):
        # Use task methods instead of goal methods for compatibility
        self.logger.log_task_start("TestGoal")
        self.logger.log_task_stop("TestGoal")
        log_output = self.log_stream.getvalue()
        self.assertIn("TestGoal", log_output)

if __name__ == '__main__':
    unittest.main()