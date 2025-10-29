import unittest
import logging
import os
from unittest.mock import patch, MagicMock
from io import StringIO

class TestLogMethods(unittest.TestCase):

    def setUp(self):
        # Mock the enhanced logger import to force standard logger
        self.log_stream = StringIO()
        self.stream_handler = logging.StreamHandler(self.log_stream)
        
    def tearDown(self):
        # Clean up environment
        for key in ['UCBL_DISABLE_EKS_FEATURES', 'SKIP_AWS_TESTS', 'SKIP_K8S_TESTS']:
            if key in os.environ:
                del os.environ[key]

    @patch('ucbl_logger.logger._enhanced_available', False)
    def test_log_risk(self):
        from ucbl_logger.logger import UCBLLogger
        logger = UCBLLogger(log_level=logging.INFO)
        
        # Mock the log method to capture output
        with patch.object(logger, '_standard_logger') as mock_logger:
            logger.log_risk("Test Risk")
            mock_logger.log_risk.assert_called_once_with("Test Risk", False, False)

    @patch('ucbl_logger.logger._enhanced_available', False)
    def test_log_anomaly(self):
        from ucbl_logger.logger import UCBLLogger
        logger = UCBLLogger(log_level=logging.INFO)
        
        with patch.object(logger, '_standard_logger') as mock_logger:
            logger.log_anomaly("Anomaly detected")
            mock_logger.log_anomaly.assert_called_once_with("Anomaly detected")

    @patch('ucbl_logger.logger._enhanced_available', False)
    def test_log_suspicious_activity(self):
        from ucbl_logger.logger import UCBLLogger
        logger = UCBLLogger(log_level=logging.INFO)
        
        with patch.object(logger, '_standard_logger') as mock_logger:
            logger.log_suspicious_activity("Suspicious activity")
            # This calls log_anomaly internally
            mock_logger.log_anomaly.assert_called_once()

    @patch('ucbl_logger.logger._enhanced_available', False)
    def test_log_goal_start_stop(self):
        from ucbl_logger.logger import UCBLLogger
        logger = UCBLLogger(log_level=logging.INFO)
        
        with patch.object(logger, '_standard_logger') as mock_logger:
            logger.log_task_start("TestGoal")
            logger.log_task_stop("TestGoal")
            mock_logger.log_task_start.assert_called_once_with("TestGoal", "System")
            mock_logger.log_task_stop.assert_called_once_with("TestGoal")

if __name__ == '__main__':
    unittest.main()