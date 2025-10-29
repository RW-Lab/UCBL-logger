import unittest
import logging
from io import StringIO
from ucbl_logger.logger import UCBLLogger  # Replace with actual import

class TestLogMethods(unittest.TestCase):

    def setUp(self):
        self.log_stream = StringIO()
        self.logger = UCBLLogger(log_level=logging.INFO)
        self.stream_handler = logging.StreamHandler(self.log_stream)
        # Access the underlying logger correctly
        if hasattr(self.logger, '_standard_logger'):
            self.logger._standard_logger.logger.addHandler(self.stream_handler)
        elif hasattr(self.logger, '_enhanced_logger'):
            # For enhanced logger, we'll mock the output
            pass
        self.logger.task_type = "User"  # Set a task type
        # Set the stack level globally for all tests
        if hasattr(self.logger, '_standard_logger'):
            self.logger._standard_logger.stack_level = 2

    def tearDown(self):
        self.logger.logger.handlers = []

    def test_log_risk(self):
        self.logger.log_risk("Test Risk", log_level=logging.WARNING)
        log_output = self.log_stream.getvalue()
        self.assertIn("~RISK~ Test Risk ~RISK~", log_output)

    def test_log_anomaly(self):
        """
        Test the log_anomaly method to ensure it logs anomalies correctly.
        """
        self.logger.log_anomaly("Anomaly detected", log_level=logging.ERROR)
        log_output = self.log_stream.getvalue()

        # Adjust the assertion to match the actual format of the log message
        self.assertIn("~ANOMALY~", log_output)
        self.assertIn("Anomaly Detected: Anomaly detected", log_output)
        self.assertIn("[File: logger.py]", log_output)  # Expect the file to be 'logger.py'

    def test_log_suspicious_activity(self):
        """
        Test the log_suspicious_activity method to ensure it logs suspicious activity correctly.
        """
        self.logger.log_suspicious_activity("Suspicious activity", log_level=logging.WARNING)
        log_output = self.log_stream.getvalue()

        # Adjust the assertion to match the actual format of the log message
        self.assertIn("~SUSPICIOUS~", log_output)
        self.assertIn("Suspicious Activity: Suspicious activity", log_output)
        self.assertIn("[File: logger.py]", log_output)  # Expect the file to be 'logger.py'

    def test_log_goal_start_stop(self):
        self.logger.log_goal_start("TestGoal")
        self.logger.log_goal_stop("TestGoal")
        log_output = self.log_stream.getvalue()
        self.assertIn("Goal '<? TestGoal ?>' started.", log_output)
        self.assertIn("Goal '<? TestGoal ?>' stopped.", log_output)

if __name__ == '__main__':
    unittest.main()
