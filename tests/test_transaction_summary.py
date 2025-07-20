import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

class TransactionSummaryTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Setup Chrome WebDriver (make sure chromedriver is in PATH)
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run headless for testing
        cls.driver = webdriver.Chrome(options=options)
        cls.base_url = "http://localhost:8000"  # Change if your dev server runs on different port

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_buyairtime_transaction_summary_updates(self):
        driver = self.driver
        driver.get(f"{self.base_url}/mobileTopup/buyairtime/")
        time.sleep(1)

        # Select network
        network_select = driver.find_element(By.ID, "network")
        network_select.click()
        network_select.find_element(By.CSS_SELECTOR, "option[value='mtn']").click()

        # Wait for page to load any dynamic content
        time.sleep(2)

        # Enter amount
        amount_input = driver.find_element(By.ID, "amount")
        amount_input.clear()
        amount_input.send_keys("1000")

        # Enter phone number
        phone_input = driver.find_element(By.ID, "phone-number")
        phone_input.clear()
        phone_input.send_keys("08012345678")

        # Select country code for phone number if exists
        try:
            country_select = driver.find_element(By.ID, "countries")
            country_select.click()
            country_select.find_element(By.CSS_SELECTOR, "option[value='+234']").click()
        except:
            pass

        # Check transaction summary updates
        summary_network = driver.find_element(By.ID, "summary-network").text
        summary_amount = driver.find_element(By.ID, "summary-amount").text
        summary_phone = driver.find_element(By.ID, "summary-phone-number").text

        self.assertEqual(summary_network.lower(), "mtn")
        self.assertIn("1000", summary_amount)
        self.assertEqual(summary_phone, "08012345678")

    def test_billpayment_bills_transaction_summary_updates(self):
        driver = self.driver
        driver.get(f"{self.base_url}/billPayments/bills/")
        time.sleep(1)

        # Select service provider
        service_provider = driver.find_element(By.ID, "service-provider")
        service_provider.click()
        service_provider.find_element(By.CSS_SELECTOR, "option[value='ikeja-electric']").click()

        # Wait for page to load any dynamic content
        time.sleep(2)

        # Enter meter number
        meter_number = driver.find_element(By.ID, "meter-number")
        meter_number.clear()
        meter_number.send_keys("123456789")

        # Select meter type
        meter_type = driver.find_element(By.ID, "meter-type")
        meter_type.click()
        meter_type.find_element(By.CSS_SELECTOR, "option[value='prepaid']").click()

        # Enter phone number
        phone_input = driver.find_element(By.ID, "phone")
        phone_input.clear()
        phone_input.send_keys("08012345678")

        # Enter amount
        amount_input = driver.find_element(By.ID, "amount")
        amount_input.clear()
        amount_input.send_keys("5000")

        # Check transaction summary updates
        summary_service = driver.find_element(By.ID, "summary-service-provider").text
        summary_meter_type = driver.find_element(By.ID, "summary-meter-type").text
        summary_meter_number = driver.find_element(By.ID, "summary-meter-number").text
        summary_phone = driver.find_element(By.ID, "summary-phone-number").text
        summary_amount = driver.find_element(By.ID, "summary-amount").text

        self.assertEqual(summary_service, "ikeja-electric")
        self.assertEqual(summary_meter_type, "prepaid")
        self.assertEqual(summary_meter_number, "123456789")
        self.assertEqual(summary_phone, "08012345678")
        self.assertIn("5000", summary_amount)

if __name__ == "__main__":
    unittest.main()
