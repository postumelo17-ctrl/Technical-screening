# Technical Screening Deliverables

## 1. CI/CD Checklist

- ✅ **Automated Testing**: Run pytest on every push and PR with coverage reporting (coverage threshold: 80%)
- ✅ **Docker Build**: Build and cache Docker images using Buildx, push to registry on main branch
- ✅ **Code Quality**: Integrate linting (flake8/black) and security scanning (bandit) in pipeline
- ✅ **Deploy to Staging**: Automated deployment to staging after successful build with smoke tests
- ✅ **Notifications**: Send Slack/email notifications on pipeline success/failure for visibility

### Staging Deployment Flow
The CI/CD pipeline automatically deploys to staging when code is merged to main:
1. Tests pass and coverage threshold met
2. Docker image built and tagged with commit SHA
3. Image pushed to ECR/Docker Hub
4. ECS/K8s deployment updated with new image
5. Health checks and smoke tests run against staging endpoint
6. Deployment status reported to team

**No credentials are stored in workflow files** - use GitHub Secrets and OIDC federation for AWS/registry authentication.

---

## 2. AI Code Review: SQL Injection Fix

**Original Code (Security Issue - SQL Injection):**
```python
def get_user(id):
    user = db.query("SELECT * FROM users WHERE id = %s" % id)
    return user
```

**Issues Identified:**
- **SQL Injection Vulnerability**: String formatting with `%` concatenates user input directly into SQL
- **Missing Error Handling**: No exception handling for database failures
- **Type Safety**: Parameter type not validated before query

**Fixed Code:**
```python
def get_user(id: int):
    try:
        # Use parameterized query to prevent SQL injection
        user = db.query("SELECT * FROM users WHERE id = ?", (id,))
        if not user:
            return {"error": "User not found"}, 404
        return user, 200
    except ValueError:
        return {"error": "Invalid user ID"}, 400
    except Exception as e:
        logger.error(f"Database error: {e}")
        return {"error": "Database error"}, 500
```

**Tests to Add:**
```python
def test_get_user_sql_injection_prevention():
    # Ensure SQL injection attempts are safely handled
    result = get_user("1; DROP TABLE users;--")
    assert result[1] == 400  # Should reject invalid input

def test_get_user_not_found():
    result = get_user(99999)
    assert result[1] == 404

def test_get_user_invalid_type():
    result = get_user("invalid")
    assert result[1] == 400

def test_get_user_success():
    result = get_user(1)
    assert result[1] == 200
    assert "id" in result[0]
```

---

## 3. Integration Testing Plan: External Payment Service API

**Objective**: Test payment processing workflow with external service integration

**Test Case 1: Successful Payment Processing**
- Mock payment service returns `{status: "success", transaction_id: "TXN123"}`
- API receives payment request, calls external service
- Verify: Response contains transaction_id, database records payment, customer notified

**Test Case 2: Payment Failure & Retry Logic**
- Mock service returns error on first call (network timeout), succeeds on retry
- Verify: Exponential backoff retry mechanism triggered, max 3 retries attempted
- Verify: Failure logged, customer receives retry notification

**Test Case 3: Concurrent Payment Requests (Idempotency)**
- Send two identical payment requests simultaneously with same idempotency key
- Verify: Only one payment processed despite duplicate requests
- Verify: Both requests return same transaction_id (no duplicate charges)

**Mocking Strategy**:
- Use `unittest.mock.patch` to mock external payment service HTTP calls
- Define fixture responses for success/failure scenarios
- Use `responses` library or `httpx` mock for HTTP interception
- Implement circuit breaker pattern to catch cascading failures
- Store request/response details for audit logging in tests

**Test Execution**: Pytest with `pytest-vcr` for recording/replaying HTTP interactions, reducing external dependencies during CI/CD runs.

---

## 4. Infrastructure & Telephony

**EC2 GPU Instance Family**:
The `p3.2xlarge` (NVIDIA V100) is ideal for ML inference; for training use `g4dn.12xlarge` (NVIDIA T4). Consider **auto-scaling policy**: scale horizontally when GPU utilization >70% for 2+ minutes, using CloudWatch metrics to trigger ASG actions based on inference queue depth.

**FreeSWITCH SIP Carrier Onboarding**:
The key initial step is configuring SIP gateway credentials in the dial plan XML (`/etc/freeswitch/sip_profiles/external/`) and creating inbound route matching the carrier's IP/domain, then validating connectivity with OPTIONS ping and test calls to confirm audio codec negotiation.
