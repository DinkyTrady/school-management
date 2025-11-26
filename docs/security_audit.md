# SIGMA - Security Audit & Vulnerability Assessment

**Assessment Date**: November 26, 2025  
**Risk Level**: 🔴 **CRITICAL** (Multiple security issues require immediate attention)

---

## Executive Summary

The SIGMA project has **4 CRITICAL vulnerabilities** and several HIGH/MEDIUM risk findings that could expose the application and database to unauthorized access, data breaches, and server compromise. **Immediate action is required before any production deployment.**

---

## Critical Issues (🔴 Must Fix Immediately)

### **Issue #1: Hardcoded SECRET_KEY**
**Severity**: 🔴 CRITICAL  
**File**: `config/settings.py` (line 28)  
**Finding**:
```python
SECRET_KEY = 'django-insecure--w+v#_h=@l4nxpnkkw^@9goe!b(o%h63^jp@6&=f$6(6k_ypub'
```

**Risk**: 
- Secret key is committed to public GitHub repository
- Can be used to forge session tokens and CSRF tokens
- Compromises all user sessions

**Remediation**:
```python
# config/settings.py - REMOVE hardcoded key
# DO NOT COMMIT KEYS TO REPO!

# Instead, use environment variable:
SECRET_KEY = env('SECRET_KEY')  # Or use django-environ
```

**.env file**:
```dotenv
SECRET_KEY=your-random-secret-key-here
# Generate one: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

**Effort**: 5 minutes  
**Priority**: 🔴 P0 (Do this FIRST)

---

### **Issue #2: DEBUG=True in .env**
**Severity**: 🔴 CRITICAL  
**File**: `.env`  
**Finding**:
```dotenv
DEBUG=True
```

**Risk**:
- Exception details are shown to users
- Secret configuration leaked in error pages
- Stack traces reveal file paths and code structure
- Tailwind CSS not minified in development

**Remediation**:
```dotenv
# .env (development only)
DEBUG=True

# .env.production (or environment variable in production)
DEBUG=False
```

**settings.py**:
```python
DEBUG = env('DEBUG', default=False)  # Safer default
```

**Production Deployment** (must set):
```bash
export DEBUG=False
```

**Effort**: 2 minutes  
**Priority**: 🔴 P0

---

### **Issue #3: Empty ALLOWED_HOSTS**
**Severity**: 🔴 CRITICAL  
**File**: `config/settings.py` (line 36)  
**Finding**:
```python
ALLOWED_HOSTS = []
```

**Risk**:
- In DEBUG=False, empty ALLOWED_HOSTS rejects ALL requests (500 error)
- Host header injection vulnerabilities possible
- DNS rebinding attacks not prevented

**Remediation**:
```python
# config/settings.py
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

**.env.production**:
```dotenv
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
```

**Effort**: 5 minutes  
**Priority**: 🔴 P0

---

### **Issue #4: .env File Committed to Repository**
**Severity**: 🔴 CRITICAL  
**File**: `.env` in root  
**Finding**:
- Database credentials visible in repo history
- Even if removed, git history retains old versions

**Risk**:
- MySQL credentials: `root:@127.0.0.1:3306/school_management`
- Anyone with repo access has DB access

**Remediation**:

1. **Create `.env.example`** (template without secrets):
```dotenv
DEBUG=False
DATABASE_URL=mysql://user:password@localhost:3306/dbname
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,example.com
```

2. **Add to `.gitignore`**:
```
.env
.env.local
.env.*.local
*.sqlite3
db.sqlite3
.secrets/
```

3. **Remove from git history** (if already public):
```bash
# Remove from all history
git filter-branch --tree-filter 'rm -f .env' HEAD
# Or use BFG Repo-Cleaner (safer)
bfg --delete-files .env
```

4. **Create `.env` locally**:
```bash
cp .env.example .env
# Edit .env with actual credentials
```

**Effort**: 10-15 minutes  
**Priority**: 🔴 P0

---

## High-Risk Issues (🟠 Fix Soon)

### **Issue #5: Missing HTTPS/SSL Settings**
**Severity**: 🟠 HIGH  
**File**: `config/settings.py`  
**Finding**:
- No `HTTPS_ONLY` setting
- No `SECURE_SSL_REDIRECT`
- No `SECURE_HSTS_SECONDS`
- Cookies not marked as secure/httponly in production

**Risk**:
- Man-in-the-middle (MITM) attacks possible
- Session hijacking on unencrypted connections
- Credentials transmitted in plain text

**Remediation**:
```python
# config/settings.py
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
```

**Effort**: 10 minutes  
**Priority**: 🟠 P1 (before production)

---

### **Issue #6: Missing CSRF Token Validation**
**Severity**: 🟠 HIGH  
**File**: `templates/` (all POST forms)  
**Finding**:
- Templates appear to use Django forms (which include CSRF)
- But custom search endpoint (`search_permissions`) returns HTML without CSRF context
- Any AJAX-based mutations must include CSRF token

**Risk**:
- Cross-site request forgery attacks possible
- Third-party sites can submit forms on behalf of users

**Remediation**:
```html
<!-- All forms must include CSRF token -->
<form method="POST">
    {% csrf_token %}
    <!-- form fields -->
</form>

<!-- AJAX requests must include CSRF token in header -->
<script>
document.addEventListener('htmx:configRequest', (event) => {
    event.detail.headers['X-CSRFToken'] = document.querySelector('[name=csrfmiddlewaretoken]').value;
});
</script>
```

**Check**: Verify all forms in templates include `{% csrf_token %}`

**Effort**: 15 minutes (review + add if missing)  
**Priority**: 🟠 P1

---

### **Issue #7: Weak Password Validation**
**Severity**: 🟠 HIGH  
**File**: `config/settings.py` (lines 93-102)  
**Finding**:
```python
AUTH_PASSWORD_VALIDATORS = [
    'UserAttributeSimilarityValidator',
    'MinimumLengthValidator',        # Default: 8 characters
    'CommonPasswordValidator',
    'NumericPasswordValidator',
]
```
- Only 8-character minimum (weak for admin/sensitive accounts)
- No uppercase, lowercase, number, special char requirements

**Risk**:
- Weak passwords easy to brute-force
- Student/teacher passwords vulnerable

**Remediation**:
```python
# If using default: increase minimum length
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}  # Increase to 12+
    },
    # ... other validators
]

# Or use django-password-validators for stronger rules
# Example: requires uppercase, lowercase, number, special char
```

**Effort**: 5 minutes  
**Priority**: 🟠 P1

---

### **Issue #8: No Rate Limiting**
**Severity**: 🟠 HIGH  
**File**: Not implemented  
**Finding**:
- No protection against brute-force login attempts
- Account enumeration possible via password reset
- No API rate limiting

**Risk**:
- Accounts compromised via password guessing
- Denial of service via login spam

**Remediation**:
```bash
# Install django-ratelimit
pip install django-ratelimit
```

```python
# config/settings.py
INSTALLED_APPS += ['django_ratelimit']
```

```python
# apps/users/views.py
from django_ratelimit.decorators import ratelimit

@ratelimit(key='ip', rate='5/m', method='POST')
def login_view(request):
    # Login view with rate limiting
    ...
```

**Effort**: 1-2 hours  
**Priority**: 🟠 P1 (for production)

---

### **Issue #9: SQL Injection via Raw Queries**
**Severity**: 🟠 HIGH  
**Finding**:
- App uses Django ORM exclusively (✅ GOOD)
- No raw SQL queries detected
- Risk is LOW for SQL injection

**Verification**:
```bash
grep -r "raw(" apps/ config/  # Should return nothing
grep -r "cursor.execute(" apps/ config/  # Should return nothing
```

**Status**: ✅ PASS - No raw SQL detected

---

## Medium-Risk Issues (🟡 Should Fix)

### **Issue #10: Missing Input Validation on File Uploads**
**Severity**: 🟡 MEDIUM  
**Finding**:
- No file upload functionality in current views
- If adding student photos/documents: missing file type validation

**Risk** (if implemented without checks):
- Arbitrary file upload → RCE
- Malware distribution
- Storage exhaustion

**Remediation** (when adding file uploads):
```python
# Example: Safe file upload
from django.core.validators import FileExtensionValidator

class StudentProfile(models.Model):
    photo = models.ImageField(
        upload_to='students/%Y/%m/',
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],
        max_length=200
    )
    
    def clean(self):
        if self.photo:
            # Check file size
            if self.photo.size > 5 * 1024 * 1024:  # 5MB limit
                raise ValidationError("File too large (max 5MB)")
```

**Effort**: N/A (not yet implemented, but plan ahead)  
**Priority**: 🟡 P2

---

### **Issue #11: No Audit Logging**
**Severity**: 🟡 MEDIUM  
**Finding**:
- No logs of who created/edited/deleted records
- Admin actions not tracked
- Difficult to investigate security incidents

**Risk**:
- Unauthorized data changes go undetected
- Cannot audit compliance (if school is regulated)
- Incident response difficult

**Remediation**:
```bash
# Option 1: Use django-audit-log
pip install django-audit-log

# Option 2: Implement custom signals
# apps/core/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import AuditLog

@receiver(post_save, sender=Akun)
def audit_akun_save(sender, instance, created, **kwargs):
    AuditLog.objects.create(
        model='Akun',
        object_id=instance.id,
        action='CREATE' if created else 'UPDATE',
        user=None,  # Can set to request.user if available
        timestamp=timezone.now()
    )
```

**Effort**: 4-8 hours  
**Priority**: 🟡 P2

---

### **Issue #12: No Logging/Error Tracking**
**Severity**: 🟡 MEDIUM  
**Finding**:
- Application has no structured logging
- No error tracking (Sentry, Rollbar, etc.)
- Exceptions lost in production

**Risk**:
- Cannot diagnose production issues
- Security incidents missed
- Performance degradation undetected

**Remediation**:
```python
# config/settings.py
import logging

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
}

# Sentry integration
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://your-sentry-key@sentry.io/project",
    integrations=[DjangoIntegration()],
    environment='production' if not DEBUG else 'development'
)
```

**Effort**: 1-2 hours  
**Priority**: 🟡 P2

---

## Low-Risk Issues (🟢 Nice to Have)

### **Issue #13: Missing Content Security Policy (CSP)**
**Severity**: 🟢 LOW  
**Finding**:
- No CSP headers
- Vulnerable to XSS if user input not escaped (currently OK, all via Django templates)

**Risk**:
- XSS attacks possible if templates not properly escaped
- Inline scripts/styles if allowed

**Remediation**:
```bash
pip install django-csp
```

```python
# config/settings.py
MIDDLEWARE += ['csp.middleware.CSPMiddleware']

CSP_DEFAULT_SRC = ("'self'",)
CSP_SCRIPT_SRC = ("'self'", "'unsafe-inline'")  # Unsafe if using inline JS
CSP_STYLE_SRC = ("'self'", "'unsafe-inline'")  # Tailwind needs inline
```

**Priority**: 🟢 P3 (nice to have)

---

### **Issue #14: Missing Security Headers**
**Severity**: 🟢 LOW  
**Finding**:
- No X-Frame-Options (clickjacking)
- No X-Content-Type-Options
- No Referrer-Policy

**Remediation**:
```python
# config/settings.py
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
    }
```

**Effort**: 10 minutes  
**Priority**: 🟢 P3

---

## Summary Table

| Issue | Severity | Fix Effort | Priority | Status |
|-------|----------|-----------|----------|--------|
| Hardcoded SECRET_KEY | 🔴 Critical | 5 min | P0 | ❌ OPEN |
| DEBUG=True | 🔴 Critical | 2 min | P0 | ❌ OPEN |
| Empty ALLOWED_HOSTS | 🔴 Critical | 5 min | P0 | ❌ OPEN |
| .env in repo | 🔴 Critical | 15 min | P0 | ❌ OPEN |
| Missing HTTPS settings | 🟠 High | 10 min | P1 | ❌ OPEN |
| CSRF token check | 🟠 High | 15 min | P1 | ⚠️ VERIFY |
| Weak password validation | 🟠 High | 5 min | P1 | ❌ OPEN |
| No rate limiting | 🟠 High | 2h | P1 | ❌ OPEN |
| Input validation (future) | 🟡 Medium | 2h | P2 | ℹ️ PLAN |
| No audit logging | 🟡 Medium | 8h | P2 | ❌ OPEN |
| No error tracking | 🟡 Medium | 2h | P2 | ❌ OPEN |
| Missing CSP headers | 🟢 Low | 1h | P3 | ℹ️ NICE |
| Missing security headers | 🟢 Low | 0.5h | P3 | ℹ️ NICE |

---

## Immediate Action Plan (Before Production)

**Phase 1 (Now)** - 30 minutes:
1. ✅ Remove `SECRET_KEY` from settings.py
2. ✅ Add to `.gitignore`: `.env`, `*.sqlite3`
3. ✅ Create `.env.example` template
4. ✅ Set `DEBUG=False` in settings

**Phase 2 (Before Deployment)** - 2 hours:
1. ✅ Fix all Critical issues
2. ✅ Add HTTPS settings
3. ✅ Configure ALLOWED_HOSTS
4. ✅ Verify CSRF tokens in all forms
5. ✅ Increase password minimum length

**Phase 3 (Soon After)** - 8 hours:
1. ✅ Add rate limiting to login
2. ✅ Implement audit logging
3. ✅ Setup error tracking (Sentry)
4. ✅ Add security headers

---

## Testing Security

```bash
# Check for hardcoded secrets
grep -r "SECRET_KEY\s*=" config/
grep -r "PASSWORD\s*=" . --include="*.py"

# Verify settings
python manage.py check --deploy

# Run security tests
python manage.py test --tag=security

# Scan dependencies for vulnerabilities
pip install safety
safety check -r requirements.txt
```

---

**Next Steps**: See `docs/quick_fixes.patch` for automated remediation code snippets.
