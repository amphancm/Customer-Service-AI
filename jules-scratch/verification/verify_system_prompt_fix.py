from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Navigate to the application and log in
        page.goto("http://localhost:5173/")
        page.get_by_label("Username").fill("admin")
        page.get_by_label("Password").fill("admin")
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("http://localhost:5173/", timeout=60000)

        # 2. Navigate to the system prompt page and update the system prompt
        page.goto("http://localhost:5173/system_prompt")
        page.wait_for_selector("h4:has-text('Parameters')")
        system_prompt_textarea = page.locator('textarea')
        original_prompt = system_prompt_textarea.input_value()
        new_prompt = original_prompt + " - updated"
        system_prompt_textarea.fill(new_prompt)
        page.get_by_role("button", name="Save").click()

        # 3. Navigate to the chat page and send a message
        page.goto("http://localhost:5173/")
        page.get_by_placeholder("Input Here......").fill("What is the system prompt?")
        page.get_by_label("Send message").click()

        # 4. Verify that the new system prompt is used
        # (We can't directly verify the system prompt used by the model,
        # but we can check if the chat is still functional after the change)
        expect(page.locator(".assistant")).to_be_visible()

        # 5. Take a screenshot
        page.screenshot(path="jules-scratch/verification/system_prompt_fix_verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
