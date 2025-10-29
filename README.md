

# UCBLLogger - User-Centric Behavior Logging

## Overview
`UCBLLogger` is an advanced logging system designed to handle structured logging for both user and system tasks, with **enhanced EKS (Elastic Kubernetes Service) optimization** for containerized GraphRAG Toolkit applications. This logger helps track various activities, including user-initiated, system-initiated, and composite tasks, providing deep insights into system behavior, suspicious activities, risks, anomalies, and more.

The logger incorporates flexible metadata handling, customizable task types, timezone-aware logging, **distributed tracing**, **Kubernetes metadata collection**, **performance monitoring**, **intelligent log sampling**, and **enhanced CloudWatch integration**. This detailed and structured logging allows you to easily debug, analyze user behavior, detect anomalies, and maintain observability in cloud-native environments.

## 🚀 Enhanced EKS Features

The enhanced UCBLLogger provides enterprise-grade logging capabilities optimized for EKS deployments:

- **🔗 Distributed Tracing**: Automatic correlation ID generation and propagation across microservices
- **☸️ Kubernetes Integration**: Automatic collection of pod, node, and cluster metadata
- **📊 Performance Monitoring**: Real-time CPU, memory, disk, and network metrics collection
- **🎯 Intelligent Sampling**: Dynamic log volume control with preservation of critical logs
- **☁️ CloudWatch Optimization**: Efficient batching, compression, and cost optimization
- **🔒 Enhanced Security**: Container security context monitoring and sensitive data redaction
- **💚 Health Monitoring**: Comprehensive health checks and system status reporting
- **🔄 Robust Error Handling**: Advanced retry mechanisms and graceful failure handling

---

## Key Features

### Core Logging Features
- **Structured Logging**: Logs user and system activities, distinguishing between different task types
- **Task Tracking**: Handles both system and user tasks, including retries and slow-step detection
- **Risk Logging**: Supports logging of risks, suspicious activities, and anomalies with customizable severity levels
- **Metadata Support**: Allows passing of context-specific metadata to each log entry
- **Customizable Time Zones**: Automatically formats log timestamps to a specified timezone (defaults to UTC)
- **Retry Tracking**: Monitors task retries, with configurable retry thresholds
- **Task Types**: Supports a variety of task types, such as user tasks, system tasks, and hybrid tasks
- **Error and Exception Logging**: Includes robust exception logging with detailed stack traces

### Enhanced EKS Features
- **🔗 Distributed Tracing**: Correlation ID generation, propagation, and OpenTelemetry integration
- **☸️ Kubernetes Metadata**: Automatic pod, node, deployment, and security context collection
- **📊 Performance Monitoring**: Real-time system metrics with configurable thresholds and alerts
- **🎯 Intelligent Sampling**: Volume-based and adaptive sampling with critical log preservation
- **☁️ CloudWatch Integration**: Optimized delivery with batching, compression, and rate limiting
- **🔒 Security Enhancements**: Container security monitoring and sensitive data redaction
- **💚 Health Monitoring**: Comprehensive health checks and Kubernetes probe integration
- **🔄 Enhanced Buffering**: Advanced retry logic, circuit breakers, and graceful failure handling

---

## 📚 Quick Links

- **[📖 Comprehensive Examples](EXAMPLES.md)** - Detailed use case scenarios and integration examples
- **[⚙️ Configuration Guide](docs/configuration-guide.md)** - Complete configuration reference
- **[🚀 Deployment Best Practices](docs/deployment-best-practices.md)** - Production deployment guide
- **[🔧 Troubleshooting Guide](docs/troubleshooting-guide.md)** - Common issues and solutions
- **[☸️ Kubernetes Deployments](deployment/kubernetes/)** - Ready-to-use Kubernetes manifests
- **[📊 Monitoring Setup](deployment/monitoring/)** - Prometheus, Grafana, and AlertManager configurations

---

## Task Types
The logger supports a variety of predefined task types to handle different aspects of user and system activities:

- **User**: `USER_TASK`
- **System**: `SYSTEM_TASK`
- **SystemUser**: `SYSTEM_USER_TASK`
- **AdminUser**: `ADMIN_USER_TASK`
- **EndUser**: `END_USER_TASK`
- **ExternalUser**: `EXTERNAL_USER_TASK`
- **SystemInternal**: `SYSTEM_INTERNAL_TASK`
- **SystemSecurity**: `SYSTEM_SECURITY_TASK`
- **SystemMaintenance**: `SYSTEM_MAINTENANCE_TASK`
- **UserInitiatedSystemTask**: `USER_INITIATED_SYSTEM_TASK`
- **SystemInitiatedUserTask**: `SYSTEM_INITIATED_USER_TASK`

These task types can be dynamically set when logging specific events, providing a clear understanding of who or what initiated the action.

---

## Installation

### Basic Installation
```bash
pip install ucbl-logger
```

### Enhanced EKS Installation
For EKS-optimized features, install with additional dependencies:
```bash
pip install ucbl-logger[eks]
# or
pip install ucbl-logger pytz kubernetes boto3 psutil opentelemetry-api
```

### Docker Installation
```dockerfile
FROM python:3.9-slim
RUN pip install ucbl-logger[eks]
COPY . /app
WORKDIR /app
```

---

## Usage Examples

### Basic Setup

```python
import logging
from ucbl_logger import UCBLLogger

# Initialize the logger
logger = UCBLLogger(log_level=logging.DEBUG, timezone_str='America/New_York')

# Start a user task
logger.task("Starting user task", switch=True, task_type="User")

# Log an anomaly
logger.log_anomaly("Unexpected behavior detected in module X", metadata={"module": "X"})

# Log task completion
logger.task("User task completed", switch=False)

# Log suspicious activity
logger.log_suspicious_activity("Suspicious login attempt detected", metadata={"user": "John Doe"})

# Log an error
try:
    1 / 0
except ZeroDivisionError as e:
    logger.log_exception(e)
```

### Enhanced EKS Setup

```python
import logging
from ucbl_logger.enhanced import EnhancedEKSLogger
from ucbl_logger.enhanced.config import (
    SamplingConfig, BufferConfig, PerformanceThresholds
)

# Configure enhanced features
sampling_config = SamplingConfig(
    enabled=True,
    default_rate=0.1,  # Sample 10% of logs
    volume_threshold=1000,
    preserve_errors=True
)

buffer_config = BufferConfig(
    max_size=10000,
    flush_interval=5,
    max_retry_attempts=3
)

# Initialize enhanced EKS logger
logger = EnhancedEKSLogger(
    service_name="graphrag-toolkit",
    namespace="production",
    enable_tracing=True,
    enable_performance_monitoring=True,
    sampling_config=sampling_config,
    buffer_config=buffer_config
)

# Use with automatic tracing
correlation_id = logger.start_trace("user_query_processing")
logger.info("Processing user query", correlation_id=correlation_id, 
           metadata={"user_id": "12345", "query_type": "semantic_search"})

# Performance metrics are automatically collected
logger.log_performance_metrics()

# End trace
logger.end_trace(correlation_id, success=True)

# Health check
health_status = logger.get_health_status()
print(f"Logger health: {health_status.status}")
```

### Kubernetes Deployment Example

```python
import os
from ucbl_logger.enhanced import EnhancedEKSLogger

# Configuration from environment variables (set in Kubernetes ConfigMap)
logger = EnhancedEKSLogger(
    service_name=os.getenv('SERVICE_NAME', 'graphrag-toolkit'),
    namespace=os.getenv('NAMESPACE', 'default'),
    enable_tracing=os.getenv('UCBL_ENABLE_TRACING', 'true').lower() == 'true',
    enable_performance_monitoring=os.getenv('UCBL_ENABLE_PERFORMANCE_MONITORING', 'true').lower() == 'true',
    enable_cloudwatch=os.getenv('UCBL_ENABLE_CLOUDWATCH', 'true').lower() == 'true'
)

# Kubernetes metadata is automatically collected
logger.info("Application started", metadata={
    "version": os.getenv('APP_VERSION', '1.0.0'),
    "environment": os.getenv('ENVIRONMENT', 'production')
})
```

---

## Key Methods

### Logging Tasks

- **`log_task_start(task_name, task_type="System", metadata=None)`**: Logs the start of a task.
- **`log_task_stop(task_name, metadata=None)`**: Logs the completion of a task.

### Risk and Anomaly Logging

- **`log_risk(msg, metadata=None, critical=False, minor=False)`**: Logs a risk event with severity levels.
- **`log_anomaly(msg, metadata=None)`**: Logs an anomaly detected in the system.

### Suspicious Activity Logging

- **`log_suspicious_activity(msg, metadata=None)`**: Logs suspicious activities with optional metadata.

### Task Retry Logging

- **`log_user_retry(task_name, retries, metadata=None)`**: Logs the number of retries for a specific task and issues warnings if the retry threshold is exceeded.

### Custom Task Types

You can use custom task types or switch between them using:

```python
logger.task_type = "AdminUser"  # Set task type to AdminUser
```

---

## Customizable Settings

### Timezones

You can configure the timezone for logs using the `timezone_str` parameter when initializing `UCBLLogger`. The logger automatically formats timestamps according to the selected timezone:

```python
logger = UCBLLogger(timezone_str="America/Los_Angeles")
```

### Slow Step Threshold

You can set a custom slow step threshold to track tasks or steps that take too long:

```python
logger.slow_step_threshold = 10  # Set threshold to 10 seconds
```

### Retry Threshold

Configure the retry threshold for tasks that are retried multiple times:

```python
logger.retry_threshold = 5  # Set threshold to 5 retries
```


## Advanced Markup Methods

The logger provides various **markup methods** for formatting log entries to clearly identify different parts of the log message, such as task goals, operators, and environment variables.

- **`mark_goal(goal)`**: Marks the goal of a task.
- **`mark_operator(operator)`**: Marks an operator performing the task.
- **`mark_method(method)`**: Marks the method name in the logs.
- **`mark_selection(selection_rule)`**: Marks a selection rule.
- **`mark_variable(var_name)`**: Marks a variable in the log.
- **`mark_env_variable(env_var)`**: Marks an environment variable.
- **`mark_id(id_value)`**: Marks a specific identifier or ID in the log.

### Example Usage of `mark_id`:

```python
task_id = "12345"
logger.info(f"Starting task with ID {logger.mark_id(task_id)}")
```

This will output a formatted log message where the task ID is clearly marked, making it easier to search and analyze logs.



## Getters and Setters

`UCBLLogger` includes several **getters** and **setters** that allow you to retrieve and modify key internal properties of the logger. This enables you to configure the logger dynamically and ensures better control over logging behavior.

### Key Properties

### 1. **`stack_level`** 
- **Getter**: Retrieves the current stack level used by the logger to extract logging information (file, line number, function).
- **Setter**: Allows you to set the stack level dynamically. Changing this affects which part of the call stack is used when logging the file and line information.

#### Usage:
```python
# Get the current stack level
current_level = logger.stack_level

# Set a new stack level
logger.stack_level = 5
```

### 2. **`user_retry`**
- **Getter**: Retrieves the current retry threshold for user tasks.
- **Setter**: Allows you to dynamically set the maximum number of retries a user is allowed before logging a warning.

#### Usage:
```python
# Get the current user retry limit
retry_limit = logger.user_retry

# Set a new retry limit
logger.user_retry = 5
```

### 3. **`log_level`**
- **Getter**: Retrieves the current logging level (e.g., `INFO`, `DEBUG`, `WARNING`, etc.).
- **Setter**: Dynamically adjusts the logging level for both the logger and its handlers. This is useful if you want to increase or decrease the verbosity of logs during execution.

#### Usage:
```python
# Get the current log level
current_log_level = logger.log_level

# Set a new log level to DEBUG
logger.log_level = logging.DEBUG
```

### 4. **`slow_step_threshold`**
- **Getter**: Retrieves the threshold for identifying a slow step (in seconds).
- **Setter**: Sets a new threshold to define what constitutes a slow step. Tasks or steps that exceed this threshold will be logged as slow.

#### Usage:
```python
# Get the current slow step threshold
current_threshold = logger.slow_step_threshold

# Set a new threshold for slow steps (e.g., 10 seconds)
logger.slow_step_threshold = 10
```

### 5. **`retry_threshold`**
- **Getter**: Retrieves the retry threshold value for tasks that are retried multiple times.
- **Setter**: Sets a new retry threshold. If the task retries exceed this threshold, the logger will issue warnings.

#### Usage:
```python
# Get the current retry threshold
current_retry_threshold = logger.retry_threshold

# Set a new retry threshold (e.g., 3 retries)
logger.retry_threshold = 3
```

### 6. **`timezone`**
- **Getter**: Retrieves the current timezone set for the logger.
- **Setter**: Dynamically updates the timezone used for timestamps in log messages. If an unknown timezone is provided, the logger will default to UTC.

#### Usage:
```python
# Get the current timezone
current_timezone = logger.timezone

# Set a new timezone (e.g., 'America/New_York')
logger.timezone = 'America/New_York'
```

---

### Benefits of Using Getters and Setters

- **Customization**: Dynamically adjust settings such as retry thresholds, logging levels, and slow step thresholds during runtime to fit changing conditions.
- **Control**: Getters provide easy access to important properties, while setters allow you to modify behavior without needing to change core code.
- **Error Handling**: Some setters (e.g., for `retry_threshold` and `timezone`) include built-in validation and error handling to ensure valid values are used.



## Error and Exception Handling

Use `log_exception` to handle exceptions with detailed stack traces:

```python
try:
    risky_code()
except Exception as e:
    logger.log_exception(e)
```

---


## GOMS Model for After-the-Fact Observation

The **GOMS model** integration in `UCBLLogger` is designed to help analyze system behavior and user interactions **after the fact**. It is particularly useful in development, testing, and operations for understanding what has happened, rather than what is supposed to happen.

By capturing the detailed sequence of goals, operators, methods, and selection rules (GOMS), you can evaluate user behavior, identify inefficiencies, and optimize both user and system performance in real-world scenarios.

### Use Cases
- **Development**: Understand how the system is actually used versus expected behavior, helping to refine and improve features.
- **Testing**: Analyze how users interact with the system during testing phases to uncover issues or inefficiencies.
- **Operations**: Monitor and log system performance and user behavior to better identify operational bottlenecks or risks.

### Key GOMS Methods

- **`log_goal_start(goal_name)`**: Logs the start of a goal.
- **`log_goal_stop(goal_name)`**: Logs the completion of a goal.
- **`log_operator(operator_name)`**: Logs the execution of an operator (action).
- **`log_method(method_name)`**: Logs the execution of a method.
- **`log_selection(selection_rule)`**: Logs the application of a selection rule.

### Example Use in Operations

```python
# Log the start of a user transaction goal
logger.log_goal_start("User Transaction")

# Log each operator (user action) and method executed
logger.log_operator("Entered payment details")
logger.log_method("Validated payment")

# Log the selection rule applied during the transaction
logger.log_selection("User chose credit card payment method")

# Log the completion of the goal
logger.log_goal_stop("User Transaction")
```

### Benefits of After-the-Fact Observation

- **Behavior Analysis**: Provides insights into actual user behavior during interactions with the system, as opposed to theoretical models.
- **Performance Monitoring**: Tracks operational tasks and identifies slow steps or system bottlenecks.
- **Optimization**: Helps optimize system and user behavior based on real-world usage patterns observed during development, testing, and operations.

By capturing and logging real interactions, the GOMS model enables you to gain a deeper understanding of system and user performance over time.


## License
Licensed under MIT. Please refer to the LICENSE file for details.

---

For any questions or contributions, feel free to reach out to the author:  
**Evan Erwee**  
Email: evan@erwee.com

---

This README provides a comprehensive guide for getting started with UCBLLogger, its key features, and how to integrate it into your system for effective logging.


---

## 🔧 Enhanced EKS Configuration Guide

### Environment Variables Configuration

The enhanced EKS logger can be configured using environment variables, making it ideal for Kubernetes deployments:

```bash
# Service Configuration
SERVICE_NAME=graphrag-toolkit
NAMESPACE=production
ENVIRONMENT=production

# Tracing Configuration
UCBL_ENABLE_TRACING=true
UCBL_ENABLE_OPENTELEMETRY=false

# Performance Monitoring
UCBL_ENABLE_PERFORMANCE_MONITORING=true
UCBL_PERFORMANCE_COLLECTION_INTERVAL=60
UCBL_CPU_WARNING_THRESHOLD=80.0
UCBL_CPU_CRITICAL_THRESHOLD=95.0
UCBL_MEMORY_WARNING_THRESHOLD=80.0
UCBL_MEMORY_CRITICAL_THRESHOLD=95.0

# Sampling Configuration
UCBL_ENABLE_SAMPLING=true
UCBL_DEFAULT_SAMPLING_RATE=0.1
UCBL_VOLUME_THRESHOLD=1000
UCBL_SAMPLING_WINDOW_SIZE=60
UCBL_PRESERVE_ERRORS=true

# Buffer Configuration
UCBL_BUFFER_MAX_SIZE=10000
UCBL_BUFFER_FLUSH_INTERVAL=5
UCBL_MAX_RETRY_ATTEMPTS=3
UCBL_RETRY_BACKOFF_MULTIPLIER=2.0

# CloudWatch Configuration
UCBL_ENABLE_CLOUDWATCH=true
UCBL_CLOUDWATCH_LOG_GROUP=/aws/eks/graphrag-toolkit
UCBL_CLOUDWATCH_REGION=us-west-2
UCBL_ENABLE_COMPRESSION=true
UCBL_BATCH_SIZE=100

# Security Configuration
UCBL_ENABLE_SECURITY_MONITORING=true
UCBL_ENABLE_DATA_REDACTION=true

# Health Monitoring
UCBL_ENABLE_HEALTH_MONITORING=true
UCBL_HEALTH_CHECK_PORT=8080
UCBL_HEALTH_CHECK_PATH=/health
```

### Kubernetes ConfigMap Example

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: ucbl-logger-config
  namespace: production
data:
  # Copy the environment variables above
  SERVICE_NAME: "graphrag-toolkit"
  UCBL_ENABLE_TRACING: "true"
  # ... (other configuration values)
```

### Advanced Configuration Classes

```python
from ucbl_logger.enhanced.config import (
    SamplingConfig, BufferConfig, PerformanceThresholds,
    CloudWatchConfig, SecurityConfig, HealthConfig
)

# Detailed sampling configuration
sampling_config = SamplingConfig(
    enabled=True,
    default_rate=0.1,
    level_rates={
        'DEBUG': 0.01,    # Sample 1% of debug logs
        'INFO': 0.1,      # Sample 10% of info logs
        'WARNING': 0.5,   # Sample 50% of warning logs
        'ERROR': 1.0,     # Keep all error logs
        'CRITICAL': 1.0   # Keep all critical logs
    },
    volume_threshold=1000,
    window_size=60,
    preserve_errors=True
)

# Performance monitoring thresholds
performance_config = PerformanceThresholds(
    cpu_warning=70.0,
    cpu_critical=90.0,
    memory_warning=75.0,
    memory_critical=90.0,
    disk_io_warning=80.0,
    network_latency_warning=100.0
)

# CloudWatch optimization
cloudwatch_config = CloudWatchConfig(
    log_group="/aws/eks/graphrag-toolkit",
    region="us-west-2",
    enable_compression=True,
    batch_size=500,
    max_batch_wait_time=10,
    enable_deduplication=True
)

# Security configuration
security_config = SecurityConfig(
    enable_security_monitoring=True,
    enable_data_redaction=True,
    redaction_patterns=[
        r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',  # Credit cards
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',  # Emails
        r'\b\d{3}-\d{2}-\d{4}\b'  # SSN
    ]
)
```

---

## 📊 Monitoring and Observability

### Prometheus Metrics

The enhanced logger exposes comprehensive metrics for monitoring:

```python
# Metrics exposed by the logger
ucbl_logger_logs_total{level, service, namespace}
ucbl_logger_sampling_rate{service, namespace}
ucbl_logger_logs_sampled_total{level, service, namespace}
ucbl_logger_cpu_usage_percent{service, namespace}
ucbl_logger_memory_usage_percent{service, namespace}
ucbl_logger_buffer_size{service, namespace}
ucbl_logger_buffer_flushes_total{service, namespace}
ucbl_logger_cloudwatch_logs_sent_total{service, namespace}
ucbl_logger_cloudwatch_errors_total{service, namespace}
ucbl_logger_traces_generated_total{service, namespace}
ucbl_logger_health_checks_total{status, service, namespace}
```

### Grafana Dashboard

Import the provided Grafana dashboard from `deployment/monitoring/grafana-dashboard.json` for comprehensive visualization of:

- Log volume and trends
- Sampling efficiency
- Buffer usage and health
- Performance metrics
- CloudWatch delivery status
- System health scores
- Error rates and patterns

### Health Checks

The logger provides health check endpoints for Kubernetes:

```python
# Health check endpoint
GET /health
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00Z",
  "components": {
    "buffer": {"status": "healthy", "usage_percent": 45.2},
    "cloudwatch": {"status": "healthy", "error_rate": 0.001},
    "performance": {"status": "healthy", "cpu_percent": 23.5},
    "sampling": {"status": "active", "current_rate": 0.1}
  },
  "metrics": {
    "logs_per_second": 150.5,
    "buffer_size": 4520,
    "health_score": 0.95
  }
}
```

---

## 🚀 Deployment Guide

### 1. Basic Kubernetes Deployment

```bash
# Apply RBAC permissions
kubectl apply -f deployment/kubernetes/rbac.yaml

# Apply configuration
kubectl apply -f deployment/kubernetes/configmap.yaml

# Deploy application
kubectl apply -f deployment/kubernetes/deployment.yaml
```

### 2. Production Deployment

```bash
# Create production namespace
kubectl create namespace production

# Apply production configuration
kubectl apply -f deployment/kubernetes/configmap.yaml -n production

# Deploy with production settings
kubectl apply -f deployment/kubernetes/production-deployment.yaml
```

### 3. Monitoring Setup

```bash
# Deploy Prometheus configuration
kubectl apply -f deployment/monitoring/prometheus-config.yaml

# Deploy AlertManager rules
kubectl apply -f deployment/monitoring/alertmanager-rules.yaml

# Import Grafana dashboard
kubectl apply -f deployment/monitoring/grafana-provisioning.yaml
```

### 4. Security Policies

```bash
# Apply network policies
kubectl apply -f deployment/kubernetes/network-policy.yaml

# Apply pod security policies
kubectl apply -f deployment/kubernetes/pod-security-policy.yaml
```

---

## 🔍 Troubleshooting Guide

### Common Issues and Solutions

#### 1. Logger Not Collecting Kubernetes Metadata

**Symptoms:**
- Missing pod/node information in logs
- Errors about Kubernetes API access

**Solutions:**
```bash
# Check RBAC permissions
kubectl auth can-i get pods --as=system:serviceaccount:default:ucbl-logger-service-account

# Verify service account is mounted
kubectl describe pod <pod-name> | grep -A 5 "Service Account"

# Check if running in Kubernetes
kubectl exec <pod-name> -- ls /var/run/secrets/kubernetes.io/serviceaccount/
```

#### 2. High Memory Usage

**Symptoms:**
- Pod OOMKilled errors
- High memory usage metrics

**Solutions:**
```python
# Reduce buffer size
buffer_config = BufferConfig(
    max_size=5000,  # Reduce from default 10000
    flush_interval=2  # Flush more frequently
)

# Enable aggressive sampling
sampling_config = SamplingConfig(
    enabled=True,
    default_rate=0.05,  # Reduce sampling rate
    volume_threshold=500  # Lower threshold
)
```

#### 3. CloudWatch Delivery Issues

**Symptoms:**
- Logs not appearing in CloudWatch
- Rate limiting errors

**Solutions:**
```bash
# Check AWS credentials
kubectl exec <pod-name> -- aws sts get-caller-identity

# Verify CloudWatch permissions
aws logs describe-log-groups --log-group-name-prefix /aws/eks/

# Check rate limiting
kubectl logs <pod-name> | grep "rate.limit"
```

**Configuration fixes:**
```python
# Optimize CloudWatch delivery
cloudwatch_config = CloudWatchConfig(
    batch_size=1000,  # Larger batches
    max_batch_wait_time=30,  # Longer wait time
    enable_compression=True,  # Reduce payload size
    retry_backoff_multiplier=1.5  # Gentler backoff
)
```

#### 4. Performance Impact

**Symptoms:**
- Application slowdown
- High CPU usage from logging

**Solutions:**
```python
# Reduce performance monitoring frequency
performance_config = PerformanceThresholds(
    collection_interval=300  # Collect every 5 minutes instead of 1
)

# Enable sampling to reduce volume
sampling_config = SamplingConfig(
    enabled=True,
    default_rate=0.1,
    preserve_errors=True
)

# Use async processing
logger = EnhancedEKSLogger(
    async_processing=True,  # Enable async mode
    buffer_config=buffer_config
)
```

#### 5. Tracing Issues

**Symptoms:**
- Missing correlation IDs
- Broken trace chains

**Solutions:**
```python
# Manual correlation ID handling
correlation_id = request.headers.get('X-Correlation-ID')
if not correlation_id:
    correlation_id = logger.start_trace("manual_operation")

logger.info("Processing request", correlation_id=correlation_id)

# Verify header propagation
logger.debug(f"Headers: {dict(request.headers)}")
```

### Debug Mode

Enable debug mode for detailed troubleshooting:

```python
logger = EnhancedEKSLogger(
    service_name="debug-service",
    log_level=logging.DEBUG,
    debug_mode=True  # Disables sampling, enables verbose logging
)
```

### Log Analysis Commands

```bash
# Check log volume
kubectl logs <pod-name> | grep "ucbl_logger" | wc -l

# Find errors
kubectl logs <pod-name> | grep -i error

# Check sampling statistics
kubectl logs <pod-name> | grep "sampling_stats"

# Monitor buffer usage
kubectl logs <pod-name> | grep "buffer_usage"

# Check health status
kubectl exec <pod-name> -- curl localhost:8080/health
```

### Performance Monitoring

```bash
# Monitor resource usage
kubectl top pod <pod-name>

# Check metrics endpoint
kubectl port-forward <pod-name> 9090:9090
curl localhost:9090/metrics | grep ucbl_logger
```

---

## 🎯 Use Case Examples

The Enhanced UCBLLogger is designed for real-world EKS scenarios. Here are some key use cases covered in our [comprehensive examples](EXAMPLES.md):

### 🔍 GraphRAG Query Processing Service
Complete logging setup for a GraphRAG service that processes user queries with semantic search, including:
- Distributed tracing across query processing steps
- Performance monitoring for embedding generation and vector search
- Intelligent sampling to control costs while preserving critical logs
- Error handling and debugging capabilities

### 🚀 High-Volume Microservice
Configuration for services handling thousands of requests per minute:
- Adaptive sampling that automatically adjusts based on traffic volume
- Cost-optimized CloudWatch delivery with compression and batching
- Performance-aware logging that reduces verbosity under high load
- Preservation of critical business events (payments, security, etc.)

### 📊 Batch Processing Jobs
Comprehensive monitoring for data processing workloads:
- Performance monitoring with resource usage alerts
- Progress tracking with correlation IDs across processing steps
- Memory and CPU optimization recommendations
- Failure recovery and debugging support

### 🔒 Security-Sensitive Applications
Enhanced security logging for applications handling sensitive data:
- Automatic PII redaction (SSN, emails, credit cards, API keys)
- Security event monitoring and alerting
- Audit trails for compliance requirements
- Container security context monitoring

### 🌐 Web Application Integration
Ready-to-use integrations for popular frameworks:
- Flask/Django request tracing with correlation IDs
- Celery task monitoring with performance metrics
- Custom Prometheus metrics integration
- Multi-environment configuration management

**[👉 View All Examples](EXAMPLES.md)** - Complete code examples with detailed explanations

---

## 📚 Additional Resources

### Documentation
- [Configuration Reference](docs/configuration.md)
- [API Documentation](docs/api.md)
- [Deployment Best Practices](docs/deployment-best-practices.md)
- [Security Guide](docs/security.md)

### Examples
- [Basic Usage Examples](examples/)
- [Kubernetes Deployment Examples](deployment/kubernetes/)
- [Monitoring Configuration](deployment/monitoring/)

### Support
- [GitHub Issues](https://github.com/your-org/ucbl-logger/issues)
- [Discussion Forum](https://github.com/your-org/ucbl-logger/discussions)
- [Slack Channel](https://your-org.slack.com/channels/ucbl-logger)

---

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details on:
- Setting up the development environment
- Running tests
- Submitting pull requests
- Code style guidelines

### Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/ucbl-logger.git
cd ucbl-logger

# Install development dependencies
pip install -e ".[dev,eks]"

# Run tests
pytest tests/

# Run integration tests (requires Kubernetes)
pytest tests/integration/
```