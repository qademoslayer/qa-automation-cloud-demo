# QA Automation Cloud-Ready Demo v2 (Allure + Slack + Contact Form)

## What's new
- Allure report generation & deployment to GitHub Pages
- Slack notification (set `SLACK_WEBHOOK_URL` secret)
- UI test for Contact Form (set `CONTACT_FORM_URL` in GitHub Actions Variables)

## How to use
1) Push repo to GitHub (branch: main)
2) In Settings → Secrets and variables:
   - Secrets: `SLACK_WEBHOOK_URL`
   - Variables: `BASE_URL` (optional), `CONTACT_FORM_URL` (contact form URL)
3) Open Actions → run the workflow
4) Artifacts: `reports/*`, `allure-results/*`, `allure-report/*`
5) GitHub Pages will publish the Allure static report for `main` branch

## Local run
pip install -r requirements.txt
python tests/validation/nea_validate.py
pytest tests/api --alluredir=allure-results
pytest tests/ui --alluredir=allure-results
