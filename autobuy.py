from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def order_product(upi_id, pin_code, product_url):
    chrome_user_data_path = r"C:\Users\vivek\AppData\Local\Google\Chrome\User Data"

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument(f"user-data-dir={chrome_user_data_path}")
    chrome_options.add_argument("--profile-directory=Default")

    driver = webdriver.Chrome(options=chrome_options)

    try:
        # Open product URL
        driver.get(product_url)

        time.sleep(random.randint(3, 5))

        # Maximize window
        driver.maximize_window()

        # Enter pincode and click check
        pincode_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "pincodeInputId"))
        )
        pincode_input.clear()
        pincode_input.send_keys(pin_code)

        check_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "i40dM4"))
        )
        check_button.click()

        time.sleep(5)

        # Click buy now button
        buy_now_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, 'vslbG+') and contains(@class, '_3Yl67G') and contains(@class, '_7Pd1Fp')]"))
        )
        buy_now_button.click()

        time.sleep(3)

        # Click Deliver Here button
        deliver_here_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='Deliver Here']"))
        )
        deliver_here_button.click()

        time.sleep(2)

        # Click Continue button
        continue_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[text()='CONTINUE']"))
        )
        continue_button.click()

        try:
            # Click Accept & Continue button if it appears
            accept_continue_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[text()='Accept & Continue']"))
            )
            accept_continue_button.click()
        except:
            print("No agreement found")

        time.sleep(8)

        # Select payment method
        payment_div_elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, 'Pg+ADy') and contains(@class, 'SC+loY')]"))
        )
        upi_input = payment_div_elements[1].find_element(By.XPATH, ".//label")
        upi_input.click()
        time.sleep(3)

        try:
            upi_id_radio = WebDriverWait(driver, 10).until(
                EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@class, '_9-suWS')]"))
            )[2]
            upi_id_inner_tag = upi_id_radio.find_elements(By.XPATH, ".//div[contains(@class, 'jIbgdC')]")
            upi_id_tag = upi_id_inner_tag[1]
            upi_id_tag.click()
        except:
            upi_id_div = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'jIbgdC') and contains(text(), 'Your UPI ID')]"))
            )
            upi_id_div.click()

        time.sleep(3)

        # Input UPI ID
        upi_input_tag = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@name='upi-id' and contains(@class, 'v2VFa-') and contains(@class, 'z2D4XG')]"))
        )
        upi_input_tag.send_keys(upi_id)

        # Click Verify button
        verify_upi = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'L0cDUo') and contains(text(), 'Verify')]"))
        )
        verify_upi.click()
        time.sleep(5)

        # Click Pay button
        pay_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'QqFHMw') and contains(@class, 'cLLuYN') and contains(@class, '_7Pd1Fp') and contains(text(), 'PAY')]"))
        )
        pay_button.click()

        # Wait for completion
        time.sleep(5 * 60)

    finally:
        time.sleep(5)
        driver.quit()