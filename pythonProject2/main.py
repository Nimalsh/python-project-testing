import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Setup the WebDriver
os.environ['PATH'] += "C:\\selenium"
driver = webdriver.Chrome()
driver.maximize_window()

# Open the job application form page
driver.get("https://demoqa.com/automation-practice-form")


def test_valid_form_submission():
    try:
        # Fill in the form fields
        driver.find_element(By.ID, "firstName").send_keys("John")
        driver.find_element(By.ID, "lastName").send_keys("Doe")
        driver.find_element(By.ID, "userEmail").send_keys("johndoe@example.com")
        driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']").click()
        driver.find_element(By.ID, "userNumber").send_keys("1234567890")

        # Wait for the date of birth field to be clickable and click it
        date_of_birth_input = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "dateOfBirthInput"))
        )
        date_of_birth_input.click()

        # Select the date of birth
        driver.find_element(By.CSS_SELECTOR, ".react-datepicker__month-select").send_keys("March")
        driver.find_element(By.CSS_SELECTOR, ".react-datepicker__year-select").send_keys("1990")
        driver.find_element(By.CSS_SELECTOR, ".react-datepicker__day--001").click()

        # Subjects
        subjects_field = driver.find_element(By.ID, "subjectsInput")
        subjects_field.send_keys("Maths")
        subjects_field.send_keys("\n")  # Press Enter to select the subject

        # Hobbies
        driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']").click()  # Sports
        driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-2']").click()  # Reading
        driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-3']").click()  # Music

        # Address
        driver.find_element(By.ID, "currentAddress").send_keys("123 Main Street, Anytown, USA")

        # State and City
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # Ensure dropdowns are visible
        state_dropdown = driver.find_element(By.ID, "state")
        state_dropdown.click()
        driver.find_element(By.CSS_SELECTOR, "div[id*='react-select'][id$='-option-0']").click()  # Select "NCR"

        city_dropdown = driver.find_element(By.ID, "city")
        city_dropdown.click()
        driver.find_element(By.CSS_SELECTOR, "div[id*='react-select'][id$='-option-0']").click()  # Select "Delhi"

        # Submit the form
        driver.find_element(By.ID, "submit").click()

        # Verify form submission
        success_message = WebDriverWait(driver, 6).until(
            EC.presence_of_element_located((By.ID, "example-modal-sizes-title-lg"))
        )
        assert success_message.text == "Thanks for submitting the form"
        print("Test Case 1: Passed - Valid form submission.")

    except Exception as e:
        print(f"Test Case 1: Failed - {e}")



# Test Case 2: Form submission with blank fields
def test_form_submission_with_blank_fields():
    try:
        print("Starting Test Case 2: Form submission with blank fields")

        # Refresh the page to reset form state
        driver.refresh()

        # Submit the form without filling out any mandatory fields
        driver.find_element(By.ID, "submit").click()

        # Wait for validation to apply (explicit wait for fields to show red border)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "is-invalid"))
        )

        # Verify that the required fields have the "is-invalid" class (red border) applied
        required_fields = driver.find_elements(By.CSS_SELECTOR, "input[required]")

        invalid_fields = []
        for field in required_fields:
            # Check if the "is-invalid" class is in the field's class list
            if "is-invalid" in field.get_attribute("class"):
                invalid_fields.append(field)

        # Assert that at least one mandatory field has the "is-invalid" class
        assert len(invalid_fields) > 0, "Test Failed - No mandatory fields have a red border (validation error)."

        print("Test Case 2: Passed - Blank mandatory fields handled.")

    except Exception as e:
        print(f"Test Case 2: Failed - {e}")

# Test Case 3: Invalid email format validation
def test_invalid_email_validation():
    driver.refresh()
    driver.find_element(By.ID, "firstName").send_keys("John")
    driver.find_element(By.ID, "lastName").send_keys("Doe")
    driver.find_element(By.ID, "userEmail").send_keys("invalid-email")
    driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']").click()
    driver.find_element(By.ID, "userNumber").send_keys("1234567890")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    driver.find_element(By.ID, "submit").click()

    # Wait for invalid email to appear
    try:
        # Wait for the email field to show the "is-invalid" class after submitting an invalid email
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#userEmail.is-invalid"))
        )
        print("Test Case 3: Passed - Invalid email validation.")
    except Exception as e:
        print(f"Test Case 3: Failed - {e}")

# Run the tests
test_valid_form_submission()
test_form_submission_with_blank_fields()
test_invalid_email_validation()

# Close the browser
driver.quit()