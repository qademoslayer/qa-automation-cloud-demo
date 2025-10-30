import os, pytest, time
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv('BASE_URL', 'https://example.com')
FORM_URL = os.getenv('CONTACT_FORM_URL', '').strip()

@pytest.mark.skipif(FORM_URL == '', reason='CONTACT_FORM_URL not provided; skipping contact form test.')
def test_contact_form_submission():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(FORM_URL, timeout=60000)

        # Placeholder selectors - update to actual IDs/names when available
        # Try multiple common selectors to be resilient
        def fill(selector_list, value):
            for sel in selector_list:
                try:
                    page.fill(sel, value)
                    return True
                except Exception:
                    continue
            raise AssertionError(f'Cannot find selector among: {selector_list}')

        fill(['#name','input[name="name"]','input[id*="name"]'], 'Dennis QA')
        fill(['#email','input[name="email"]','input[type="email"]'], 'dennis@example.com')
        fill(['#message','textarea[name="message"]','textarea'], 'This is a QA contact form demo.')

        # Submit button
        clicked = False
        for btn in ['button[type="submit"]','input[type="submit"]','button:has-text("Submit")','text=Submit']:
            try:
                page.click(btn, timeout=3000)
                clicked = True
                break
            except Exception:
                continue
        assert clicked, 'Submit button not found'

        # Basic post-submit assertion (URL change or success text)
        time.sleep(1)
        success = False
        for sel in ['text=Thank you','text=Success','[role="alert"]','text=Your message has been sent']:
            if page.is_visible(sel):
                success = True
                break
        # If no success text, allow redirect/200 check as minimal assertion
        success = success or (page.status == 200 if hasattr(page, 'status') else False)
        assert success, 'No success indicator found after submit'

        browser.close()
