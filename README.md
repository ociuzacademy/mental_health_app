# Email Configuration Setup

To enable the email notification system in this project, create a `.env` file in the project root directory (same location as `manage.py`).

## Create `.env` File

Add the following credentials:

```env
EMAIL_HOST_USER=yourgmail@gmail.com
EMAIL_HOST_PASSWORD=your_16_digit_app_password
```

---

# Important Notes

- Use your **real Gmail account**.
- Do **NOT** use fake/demo email credentials.
- Your normal Gmail password will **NOT** work.
- You must use a **Gmail App Password**.

---

# How to Generate Gmail App Password

## Step 1 — Enable 2-Step Verification

Open your Google Account Security settings and enable **2-Step Verification**.

---

## Step 2 — Generate App Password

1. Open **Google App Passwords**
2. Select:
   - App → **Mail**
   - Device → **Windows Computer** (or your device)
3. Google will generate a 16-digit app password.

Example:

```env
EMAIL_HOST_PASSWORD=abcdefghijklmnop
```

---

# Update `settings.py`

Make sure your `settings.py` contains the following configuration:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_USE_TLS = True

EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')

EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

---

# Example Project Structure

```text
mentalHealthcare/
│
├── manage.py
├── .env
├── requirements.txt
├── metalHealthcare/
├── metalhealthapp/
```

---

# Security Warning

Never upload your real `.env` file to GitHub.

Add `.env` to `.gitignore`:

```gitignore
.env
```

---

# Restart Server

After updating `.env`, restart the Django server:

```bash
python manage.py runserver
```

The email notification system should now work correctly.
