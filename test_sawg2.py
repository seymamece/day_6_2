from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from Constants import globalConstants
from pathlib import Path
from datetime import date
import pytest



class Test_Sauce:
    def setup_method(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install())
        self.driver.maximize_window()
        self.driver.get(globalConstants.URL)
        self.folderPath = str(date.today())
        Path(self.folderPath).mkdir(exist_ok=True)

    def teardown_method(self):
        self.driver.quit()
    
    def waitForElementVisible(self,locator,timeout=10):
        WebDriverWait(self.driver,timeout).until(ec.visibility_of_element_located(locator))

    def test_login(self):
        self.waitForElementVisible((By.ID, globalConstants.login_id))
        loginBtn = self.driver.find_element(By.ID, globalConstants.login_id)
        loginBtn.click()
        self.waitForElementVisible((By.XPATH, globalConstants.error_msg_box_full_path))
        
        errorMessage = self.driver.find_element(By.XPATH, globalConstants.error_msg_box_full_path)
        self.driver.save_screenshot(f"{self.folderPath}/test-empty-login.png")
        assert errorMessage.text == globalConstants.just_clik_message

    @pytest.mark.parametrize("username", ["Meryem", "standard_user", "problem_user"])
    def test_empty_password_login(self, username):
        self.waitForElementVisible((By.ID, globalConstants.user_id))
        usernameInput = self.driver.find_element(By.ID, globalConstants.user_id)
        usernameInput.send_keys(username)
        self.waitForElementVisible((By.ID, globalConstants.login_id))
        loginBtn = self.driver.find_element(By.ID, globalConstants.login_id)
        loginBtn.click()
        
        errorMessage = self.driver.find_element(By.XPATH, globalConstants.error_msg_box_full_path)
        self.driver.save_screenshot(f"{self.folderPath}/test-empty-password-{username}-login.png")
        assert errorMessage.text == globalConstants.only_username_message

    @pytest.mark.parametrize("username, password", [("Halil", "123"), ("Sema", "567"),("Sumeyra", "158")])
    def test_invalid_login(self,username,password):
        self.waitForElementVisible((By.ID, globalConstants.user_id))
        usernameInput = self.driver.find_element(By.ID, globalConstants.user_id)
        passwordInput = self.driver.find_element(By.ID, globalConstants.password_id)
        loginBtn = self.driver.find_element(By.ID, globalConstants.login_id)

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, username)
        actions.send_keys_to_element(passwordInput, password)
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()
        
        self.driver.save_screenshot(f"{self.folderPath}/test-invalid-{username}-{password}-login.png")
        assert globalConstants.unmatched_username_password_text == self.driver.find_element(By.XPATH, globalConstants.error_msg_box_full_path).text
    
    def test_icon_login(self):
        self.waitForElementVisible((By.ID, globalConstants.login_id))
        loginBtn = self.driver.find_element(By.ID, globalConstants.login_id)
        loginBtn.click()

        errorBtn = self.driver.find_element(By.CLASS_NAME, globalConstants.error_btn_id)
        errorBtn.click()

        errorIcon = len(self.driver.find_elements(By.CLASS_NAME, globalConstants.error_icon_class_name))
        self.driver.save_screenshot(f"{self.folderPath}/test-icon-login.png")

        assert errorIcon == 0

    def test_valid_login(self):
        self.waitForElementVisible((By.ID, globalConstants.user_id))
        usernameInput = self.driver.find_element(By.ID, globalConstants.user_id)
        passwordInput = self.driver.find_element(By.ID, globalConstants.password_id)
        loginBtn = self.driver.find_element(By.ID, globalConstants.login_id)

        actions = ActionChains(self.driver)
        actions.send_keys_to_element(usernameInput, "standard_user")
        actions.send_keys_to_element(passwordInput, "secret_sauce")
        actions.send_keys_to_element(loginBtn, Keys.ENTER)
        actions.perform()

        
        self.driver.save_screenshot(f"{self.folderPath}/test-succes-login.png")
        assert 6 == len(self.driver.find_elements(By.CLASS_NAME, globalConstants.item_class_name))


    def test_add_remove(self):
        usernameInput = self.driver.find_element(By.ID,globalConstants.user_id)
        usernameInput.send_keys("standard_user")
        passwordInput = self.driver.find_element(By.ID,globalConstants.password_id)
        passwordInput.send_keys("secret_sauce")
        loginBtn = self.driver.find_element(By.ID,globalConstants.login_id)
        loginBtn.click()

        self.waitForElementVisible((By.XPATH,"/html/body/div/div/div/div[2]/div/div/div/div[2]/div[2]/div[1]/a/div"))
        bikeLightAdd = self.driver.find_element(By.ID,globalConstants.add_cart_btn_id)
        bikeLightAdd.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add1-remove.png")
        
        bikeLightRemove = self.driver.find_element(By.ID,globalConstants.remove_cart_btn_id)
        bikeLightRemove.click()
        self.driver.save_screenshot(f"{self.folderPath}/test-add-remove2.png")
        addtoCart = self.driver.find_element(By.XPATH,globalConstants.add_cart_full_path)

        assert addtoCart.text == "Add to cart"

    

    

   

