from playwright.sync_api import sync_playwright, Page, expect

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()

    try:
        # 1. Navigate to the system prompt page
        page.goto("http://localhost:5173/system_prompt")
        page.wait_for_selector("h4:has-text('Parameters')")

        # 2. Update the system prompt
        system_prompt_textarea = page.locator('textarea')
        original_prompt = system_prompt_textarea.input_value()
        new_prompt = original_prompt + " - updated by test"
        system_prompt_textarea.fill(new_prompt)
        page.get_by_role("button", name="Save").click()

        # 3. Get the systemPromptStore from the window object and check the state
        store_state = page.evaluate("() => window.pinia.state.value.systemPromptStore.systemPrompts")
        expect(store_state['content']).to_equal(new_prompt)

        # 4. Take a screenshot
        page.screenshot(path="jules-scratch/verification/system_prompt_store_verification.png")

    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
