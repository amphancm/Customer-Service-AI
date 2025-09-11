from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Navigate to the application
        page.goto("http://localhost:5173/")

        # 2. Log in
        page.get_by_label("Username").fill("admin")
        page.get_by_label("Password").fill("admin")
        page.get_by_role("button", name="Login").click()

        # 3. Wait for navigation to the chat page
        page.wait_for_url("http://localhost:5173/", timeout=60000)
        page.screenshot(path="jules-scratch/verification/after_login_screenshot.png")

        # 4. Send a message
        page.get_by_placeholder("Input Here......").fill("Hello, world!")
        page.get_by_label("Send message").click()

        # 5. Take a screenshot
        page.screenshot(path="jules-scratch/verification/verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
