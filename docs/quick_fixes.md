# SIGMA - Quick Fixes & Security Patches

**Status**: Ready to apply  
**Priority**: 🔴 CRITICAL  
**Estimated Time**: 30 minutes

---

## Quick Fix #1: Move SECRET_KEY to Environment Variable

**Issue**: Hardcoded SECRET_KEY in `config/settings.py` is a security vulnerability.

**Current Code** (UNSAFE):
```python
# config/settings.py line 28
SECRET_KEY = 'django-insecure--w+v#_h=@l4nxpnkkw^@9goe!b(o%h63^jp@6&=f$6(6k_ypub'
```

**Fixed Code**:
```python
# config/settings.py line 28
SECRET_KEY = env('SECRET_KEY')
```

**Generate New Secret Key**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
# Output: 'example-new-secret-key-here-64-characters-long'
```

**Update .env File**:
```dotenv
DEBUG=True
DATABASE_URL=mysql://root:@127.0.0.1:3306/school_management
SECRET_KEY=your-new-secret-key-from-above
```

**Create .env.example** (no secrets):
```dotenv
DEBUG=False
DATABASE_URL=mysql://user:password@host:3306/dbname
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1,example.com
```

**Add to .gitignore**:
```gitignore
# Environment variables (MUST NOT commit)
.env
.env.local
.env.*.local
.secrets/

# Database files
*.sqlite3
db.sqlite3

# Cache
__pycache__/
*.py[cod]
*$py.class
```

---

## Quick Fix #2: Fix DEBUG Setting for Production

**Issue**: `DEBUG=True` is set in .env, exposing sensitive information in error pages.

**Current .env**:
```dotenv
DEBUG=True
```

**Fixed settings.py**:
```python
# config/settings.py line 32
DEBUG = env('DEBUG', default=False)  # Default to False for safety
```

**For Production** (set environment variable):
```bash
export DEBUG=False
# Or in .env:
DEBUG=False
```

**For Development** (.env):
```dotenv
DEBUG=True  # Only in development!
```

---

## Quick Fix #3: Configure ALLOWED_HOSTS

**Issue**: Empty ALLOWED_HOSTS will cause 400 errors in production.

**Current Code** (UNSAFE):
```python
# config/settings.py line 36
ALLOWED_HOSTS = []
```

**Fixed Code**:
```python
# config/settings.py line 36
ALLOWED_HOSTS = env('ALLOWED_HOSTS', default='localhost,127.0.0.1').split(',')
```

**.env.example**:
```dotenv
ALLOWED_HOSTS=localhost,127.0.0.1
```

**.env.production**:
```dotenv
ALLOWED_HOSTS=example.com,www.example.com,api.example.com
```

**Verification**:
```bash
python manage.py check --deploy  # Will report ALLOWED_HOSTS issues
```

---

## Quick Fix #4: Add HTTPS/Security Headers (Production Only)

**Issue**: No HTTPS enforcement or security headers.

**Add to config/settings.py** (after DEBUG check):
```python
# config/settings.py - after line 36
if not DEBUG:
    # HTTPS Enforcement
    SECURE_SSL_REDIRECT = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Cookie Security
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    
    # Additional Security Headers
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_CONTENT_SECURITY_POLICY = {
        'default-src': ("'self'",),
        'script-src': ("'self'", "'unsafe-inline'"),  # Needed for Tailwind
        'style-src': ("'self'", "'unsafe-inline'"),   # Needed for Tailwind
    }
```

---

## Quick Fix #5: Remove .env from Git History

**If .env is already committed**:

**Option 1: Using BFG Repo Cleaner** (Recommended, fastest):
```bash
# Install BFG
brew install bfg  # macOS
# or download from https://rtyley.github.io/bfg-repo-cleaner/

# Clean from history
bfg --delete-files .env

# Force push (only if you control the repo!)
git reflog expire --expire=now --all
git gc --prune=now --aggressive
git push origin --force --all
git push origin --force --tags
```

**Option 2: Using git filter-branch** (Standard but slower):
```bash
git filter-branch --tree-filter 'rm -f .env' HEAD

git reflog expire --expire=now --all
git gc --prune=now --aggressive

git push origin --force --all
```

**Option 3: Using git filter-repo** (Newer tool):
```bash
pip install git-filter-repo

git filter-repo --path .env --invert-paths
```

**After cleaning**:
1. Notify all team members to rebase
2. Change database password (if exposed in DATABASE_URL)
3. Generate new SECRET_KEY (already done in Fix #1)
4. Verify no secrets in commit history: `git log --all --oneline | grep .env`

---

## Quick Fix #6: Implement Password Strength Requirements

**Issue**: Minimum password length is only 8 characters.

**Update settings.py**:
```python
# config/settings.py - Update AUTH_PASSWORD_VALIDATORS section
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {'min_length': 12}  # Increased from 8
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]
```

**Testing**:
```bash
python manage.py changepassword testuser
# Will now enforce 12-character minimum
```

---

## Quick Fix #7: Add Rate Limiting to Login

**Issue**: No protection against brute-force login attempts.

**Step 1: Install package**:
```bash
pip install django-ratelimit
```

**Step 2: Add to settings.py**:
```python
# config/settings.py
INSTALLED_APPS += ['django_ratelimit']
```

**Step 3: Protect login view** (If using Django's built-in):
```python
# config/urls.py - wrap the login URL

from django_ratelimit.decorators import ratelimit
from django.contrib.auth import views as auth_views
from functools import wraps

# Custom wrapped login view
def rate_limited_login(request):
    decorated = ratelimit(
        key='ip',
        rate='5/m',  # 5 attempts per minute per IP
        method='POST'
    )(auth_views.LoginView.as_view(template_name='registration/login.html'))
    
    return decorated(request)

# In urlpatterns:
path('users/auth/login/', rate_limited_login, name='login'),
```

**Testing**:
```bash
# Try login 6 times in quick succession
# Should get 429 Too Many Requests on 6th attempt
```

---

## Quick Fix #8: Create .env.example Template

**File: `.env.example`** (commit this to repo):
```dotenv
# Database Configuration
DATABASE_URL=mysql://user:password@127.0.0.1:3306/school_management

# Django Settings
DEBUG=False
SECRET_KEY=generate-a-new-key-and-paste-here
ALLOWED_HOSTS=localhost,127.0.0.1,example.com

# Optional: Email Configuration (if adding email features)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# Optional: Sentry Error Tracking
SENTRY_DSN=https://your-sentry-key@sentry.io/project-id
```

**Instructions for developers** (in README.md):
```markdown
## Setup

1. Clone repository:
   \`\`\`bash
   git clone https://github.com/DinkyTrady/school-management.git
   cd school-management
   \`\`\`

2. Copy .env template:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

3. Edit .env with your configuration:
   \`\`\`bash
   nano .env
   # OR
   code .env
   \`\`\`

4. Generate SECRET_KEY:
   \`\`\`bash
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   # Copy output and paste into .env SECRET_KEY field
   \`\`\`

5. Install and run:
   \`\`\`bash
   python -m pip install -r requirements.txt
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   \`\`\`
```

---

## Patch Summary

**Total Time to Apply**: ~30 minutes

**Changes Required**:
1. ✅ 1 line change: SECRET_KEY (line 28)
2. ✅ 1 line change: DEBUG default (line 32)
3. ✅ 1 line change: ALLOWED_HOSTS (line 36)
4. ✅ 10 lines: HTTPS/Security settings (new)
5. ✅ 3 lines: Password validator (update)
6. ✅ 1 file: Create .env.example
7. ✅ 1 file: Update .gitignore
8. ✅ 1 line: git history cleanup (if needed)

**Verification Checklist**:
```bash
# After applying patches:

# 1. Check for security issues
python manage.py check --deploy

# 2. Verify SECRET_KEY is in .env (not in code)
grep "SECRET_KEY\s*=" config/settings.py  # Should return nothing or env()

# 3. Verify DEBUG is configurable
grep "DEBUG\s*=" config/settings.py  # Should show env() call

# 4. Test login locally
python manage.py runserver
# Visit http://localhost:8000/users/auth/login/
# Try login with admin account

# 5. Verify .env is in .gitignore
cat .gitignore | grep ".env"  # Should show .env

# 6. Commit changes
git add config/settings.py .env.example .gitignore
git commit -m "Security: Move secrets to env variables, add HTTPS headers"
```

---

## Production Deployment Checklist

After applying patches, before deploying:

- [ ] `DEBUG=False` in production environment
- [ ] `SECRET_KEY` is random and not shared
- [ ] `ALLOWED_HOSTS` configured for your domain
- [ ] HTTPS certificate installed (Let's Encrypt is free)
- [ ] Database password is strong and not in code
- [ ] `.env` file is NOT committed to repo
- [ ] Database backup strategy in place
- [ ] Error monitoring (Sentry) configured
- [ ] Run `python manage.py check --deploy`
- [ ] All tests passing
- [ ] Static files collected: `python manage.py collectstatic`

---

**IMPORTANT**: These patches are MANDATORY before any production deployment. Failure to apply them leaves the system vulnerable to attack.

For detailed explanation of each issue, see `docs/security_audit.md`.
