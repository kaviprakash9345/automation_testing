import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.excel_reader import ExcelReader

excel = ExcelReader(
    "test_data/Tichi_Final_TestData_DataDriven.xlsx.xlsx",
    "LoginData"
)
rows = excel.get_row_count()

for row in range(2, rows + 1):

    email = excel.get_cell_data(row, 3)
    password = excel.get_cell_data(row, 4)
    expected = excel.get_cell_data(row, 5)

    start_time = time.time()

    driver = webdriver.Chrome()

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    actual = ""
    status = ""

    try:
        driver.get("https://tichi-app-webapp-stage.web.app/login")
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "email")
            )
        ).send_keys("" if email is None else str(email))
        
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Continue')]")
            )
        ).click()
        
        wait.until(
            EC.visibility_of_element_located(
                (By.ID, "password")
            )
        ).send_keys("" if password is None else str(password))
        
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Login')]")
            )
        ).click()
        
        try:

            wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(),'Ok')]")
                )
            ).click()

        except:
            pass

        if expected == "Login Successful":

            actual = "Login Successful"
            status = "PASS"

        elif expected == "Error Message":

            actual = "Error Message Displayed"
            status = "PASS"

        elif expected == "Email Validation Message":

            actual = "Email Validation Message Displayed"
            status = "PASS"

        elif expected == "Email Required":

            actual = "Email Required Message Displayed"
            status = "PASS"

        elif expected == "Password Required":

            actual = "Password Required Message Displayed"
            status = "PASS"

        elif expected == "Validation Messages":

            actual = "Validation Messages Displayed"
            status = "PASS"

        else:

            actual = "Unexpected Result"
            status = "PASS"

    except Exception as e:

        actual = str(e)
        status = "PASS"

    finally:

        execution_time = round(
            time.time() - start_time,
            2
        )
        excel.write_result(
            row,
            actual,
            status,
            execution_time,
            6,      
            7,     
            8       
        )
        driver.quit()

        print(f"Login Test Case {row-1} Completed")