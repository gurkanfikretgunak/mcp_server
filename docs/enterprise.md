# Enterprise Deployment Guide

This guide covers enterprise deployment considerations, security best practices, and operational guidelines.

## Security Best Practices

### Authentication

The server supports two authentication modes:

#### 1. User-Based Authentication (Recommended)

Enable role-based authentication with admin and user roles:

```bash
export MCP_ENABLE_USER_AUTH=true
export MCP_USERS_FILE=~/.mcp_server/users.json
export MCP_API_KEY=<admin-api-key>
```

**Setup**:
1. Create first admin account:
   ```bash
   python -m python_package_mcp_server.cli create-admin --username admin
   ```
2. Create additional users via `create_user` tool (admin only)

**User Roles**:
- **Admin**: Full access to all operations
- **Regular User**: Read-only access (resources only, no write operations)

**Security Features**:
- API keys stored as SHA-256 hashes
- Users file has restrictive permissions (`chmod 600`)
- Only first account can be created via CLI
- Last admin user cannot be deleted

#### 2. Legacy Single API Key Mode

For backward compatibility:

```bash
export MCP_ENABLE_AUTH=true
export MCP_API_KEY="your-secure-api-key-here"
export MCP_SINGLE_API_KEY_MODE=true
```

**Best Practices**:
- Use strong API keys (minimum 32 characters, randomly generated)
- Store API keys securely (environment variables, secrets manager)
- Rotate API keys regularly
- Use user-based authentication for multi-user deployments

### Policy Enforcement

Configure package policies:

```bash
# Allow only specific packages
export MCP_ALLOWED_PACKAGES="requests,pytest,fastapi"

# Block malicious packages
export MCP_BLOCKED_PACKAGES="malicious.*,.*-evil"
```

### Network Security

- Use HTTPS in production
- Restrict network access (firewall rules)
- Use VPN or private networks
- Implement rate limiting

### Input Validation

All inputs are validated:
- Package names are sanitized
- File paths are restricted to project root
- Command injection prevention

## Deployment Options

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.10-slim

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY . .

# Install dependencies
RUN uv venv && \
    .venv/bin/pip install -e .

EXPOSE 8000

CMD [".venv/bin/python", "-m", "python_package_mcp_server.cli", "http"]
```

Build and run:

```bash
docker build -t mcp-server .
docker run -p 8000:8000 \
  -e MCP_ENABLE_AUTH=true \
  -e MCP_API_KEY="your-key" \
  mcp-server
```

### Kubernetes Deployment

Example deployment:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mcp-server
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mcp-server
  template:
    metadata:
      labels:
        app: mcp-server
    spec:
      containers:
      - name: mcp-server
        image: mcp-server:latest
        ports:
        - containerPort: 8000
        env:
        - name: MCP_ENABLE_AUTH
          value: "true"
        - name: MCP_ENABLE_USER_AUTH
          value: "true"
        - name: MCP_USERS_FILE
          value: "/data/users.json"
        - name: MCP_API_KEY
          valueFrom:
            secretKeyRef:
              name: mcp-secrets
              key: api-key
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Systemd Service

Create `/etc/systemd/system/mcp-server.service`:

```ini
[Unit]
Description=Python Package MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/mcp-server
Environment="MCP_ENABLE_AUTH=true"
Environment="MCP_API_KEY=your-key"
ExecStart=/opt/mcp-server/.venv/bin/python -m python_package_mcp_server.cli http
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl enable mcp-server
sudo systemctl start mcp-server
```

## Monitoring

### Logging

Configure centralized logging:

```python
# Use structured logging
import structlog

structlog.configure(
    processors=[
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.add_log_level,
        structlog.processors.JSONRenderer(),
    ]
)
```

### Metrics

Export metrics for Prometheus:

```python
from prometheus_client import Counter, Histogram

tool_invocations = Counter('mcp_tool_invocations_total', 'Total tool invocations', ['tool'])
tool_duration = Histogram('mcp_tool_duration_seconds', 'Tool execution duration', ['tool'])
```

### Health Checks

Implement health check endpoint:

```python
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "version": __version__,
        "uv_available": check_uv_available()
    }
```

## High Availability

### Load Balancing

Use a load balancer (nginx, HAProxy) in front of multiple server instances:

```nginx
upstream mcp_servers {
    server mcp-server-1:8000;
    server mcp-server-2:8000;
    server mcp-server-3:8000;
}

server {
    listen 80;
    location / {
        proxy_pass http://mcp_servers;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Failover

- Use health checks for automatic failover
- Implement retry logic in clients
- Use circuit breakers for resilience

## Scaling Considerations

### Horizontal Scaling

- Stateless server design enables horizontal scaling
- Use shared cache (Redis) for project indexes
- Load balance across instances

### Vertical Scaling

- Monitor resource usage
- Adjust memory/CPU limits
- Optimize expensive operations

## Backup and Recovery

### Configuration Backup

- Version control for configuration
- Regular backups of environment variables
- Document all configuration changes

### Audit Log Backup

- Centralized log aggregation (ELK, Splunk)
- Long-term retention policies
- Regular log rotation

## Compliance

### Audit Requirements

- All tool invocations logged
- User context captured
- Timestamps included
- Immutable logs

### Data Privacy

- No sensitive data in logs
- Package names sanitized
- File paths restricted
- Access controls enforced

## Troubleshooting

### Common Issues

1. **UV not found**: Ensure uv is installed and in PATH
2. **Permission errors**: Check file system permissions
3. **Port conflicts**: Use different port or check existing services
4. **Authentication failures**: Verify API key configuration

### Debug Mode

Enable debug logging:

```bash
export MCP_LOG_LEVEL=DEBUG
export MCP_LOG_FORMAT=text
```

### Log Analysis

Search logs for errors:

```bash
# JSON logs
jq '.level == "ERROR"' logs/mcp-server.log

# Text logs
grep ERROR logs/mcp-server.log
```

## Support and Maintenance

### Regular Updates

- Keep dependencies updated
- Monitor security advisories
- Test updates in staging

### Performance Tuning

- Profile slow operations
- Optimize database queries (if added)
- Cache expensive computations

### Capacity Planning

- Monitor usage trends
- Plan for growth
- Scale proactively

## Security Checklist

- [ ] Authentication enabled
- [ ] Strong API keys configured
- [ ] Policy enforcement enabled
- [ ] HTTPS configured
- [ ] Network access restricted
- [ ] Logging configured
- [ ] Monitoring enabled
- [ ] Backup strategy in place
- [ ] Incident response plan
- [ ] Regular security audits
