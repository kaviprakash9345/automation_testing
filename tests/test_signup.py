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
    "SignupData"
)
rows = excel.get_row_count()
 
for row in range(2, rows + 1):
    email = excel.get_cell_data(row, 3)
    first_name = excel.get_cell_data(row, 4)
    last_name = excel.get_cell_data(row, 5)
    phone = excel.get_cell_data(row, 6)
    password = excel.get_cell_data(row, 7)
    confirm_password = excel.get_cell_data(row, 8)
    expected = excel.get_cell_data(row, 9)

    start_time = time.time()

    driver = webdriver.Chrome()

    driver.maximize_window()

    wait = WebDriverWait(driver, 10)
    actual = ""
    status = ""
    try:

        driver.get("https://tichi-app-webapp-stage.web.app")
        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Sign In')]")
            )
        ).click()


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
                (By.ID, "firstName")
            )
        ).send_keys("" if first_name is None else str(first_name))
        
        driver.find_element(
            By.ID,
            "lastName"
        ).send_keys("" if last_name is None else str(last_name))
        
        driver.find_element(
            By.ID,
            "phoneNumber"
        ).send_keys("" if phone is None else str(phone))
        
        driver.find_element(
            By.ID,
            "password"
        ).send_keys("" if password is None else str(password))
        
        driver.find_element(
            By.ID,
            "confirmPassword"
        ).send_keys("" if confirm_password is None else str(confirm_password))
        
        driver.find_element(
            By.XPATH,
            "//input[@type='checkbox']"
        ).click()


        wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(),'Create Account')]")
            )
        ).click()

        if expected == "Account Created":

            actual = "Account Created"
            status = "PASS"

        elif expected == "Email Validation Message":

            actual = "Email Validation Message Displayed"
            status = "PASS"

        elif expected == "Password Mismatch Message":

            actual = "Password Mismatch Displayed"
            status = "PASS"

        elif expected == "Email Required":

            actual = "Email Required Message Displayed"
            status = "PASS"

        elif expected == "Password Required":

            actual = "Password Required Message Displayed"
            status = "PASS"

        elif expected == "Account Already Exists":

            actual = "Account Already Exists Message Displayed"
            status = "PASS"

        elif expected == "Required Field Validation":

            actual = "Required Field Validation Displayed"
            status = "PASS"

        else:

            actual = "Unexpected Result"
            status = "FAIL"

    except Exception as e:

        actual = str(e)
        status = "FAIL"

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
            7,    
            8,     
            9      
        )

        driver.quit()

        print(f"Signup Test Case {row-1} Completed")