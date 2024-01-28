import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import choice
from getpass import getpass


def get_webdriver(typ):
    return webdriver.__getattribute__(typ)()


def wait_for_element(driver, by, value):
    print("....waiting for element ", by, value)
    while True:
        try:
            element = driver.find_element(by, value)
            if element and element.is_displayed():
                return element
        except NoSuchElementException:
            pass
        sleep(0.1)


def get_random_password():
    alpha = "ABCDEFGHIJKLMNOPQRSTUVW"
    return "".join(choice(alpha + alpha.lower() + "1234567890") for _ in range(42))


def login_part_one(driver, email):
    driver.get("https://console.aws.amazon.com/console/home")
    elem = driver.find_element(By.ID, "resolving_input")
    elem.clear()
    elem.send_keys(email)
    elem.send_keys(Keys.RETURN)
    return wait_for_element(driver, By.ID, "password")


def reset_password(driver_typ, email):
    driver = get_webdriver(driver_typ)

    login_part_one(driver, email)
    wait_for_element(driver, By.ID, "root_forgot_password_link").click()
    wait_for_element(driver, By.ID, "password_recovery_done_button").click()
    driver.close()

    recovery_url = input("Recovery requested. Please check your email and paste the recovery URL here:")

    driver = get_webdriver(driver_typ)
    driver.get(recovery_url)
    passwd = get_random_password()
    wait_for_element(driver, By.ID, "new_password").send_keys(passwd)
    driver.find_element(By.ID, "confirm_password").send_keys(passwd)
    driver.find_element(By.ID, "reset_password_submit").click()

    success_link = wait_for_element(driver, By.ID, "success_link")
    if not success_link or not success_link.is_displayed():
        raise Exception("Failed to reset password!")
    driver.close()
    return passwd


def login(driver, email, passwd):
    passwd_element = login_part_one(driver, email)
    passwd_element.send_keys(passwd)
    passwd_element.send_keys(Keys.RETURN)
    wait_for_element(driver, By.ID, "nav-usernameMenu")
    wait_for_element(driver, By.CSS_SELECTOR, "[data-id=awsccc-cb-btn-continue]").click()


def close_account(driver):
    driver.get("https://console.aws.amazon.com/billing/home?#/account")
    wait_for_element(driver, By.CSS_SELECTOR, "[data-testid=close-account-button]")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    driver.find_element(By.CSS_SELECTOR, "[data-testid=close-account-button]").click()
    wait_for_element(driver, By.CSS_SELECTOR, "[data-testid=close-account-modal-confirm]").click()


def main():
    parser = argparse.ArgumentParser(
        description="""
        Close the AWS account identified by the given email, optionally performing a password reset.
        This program requires an installed selenium driver to run.
        It was tested using the selenium driver for firefox 0.30.0
        installed from https://github.com/mozilla/geckodriver/releases .
        The input window waits for you to input any captchas and MFA keys.
    """
    )

    parser.add_argument("email", help="Email associated with the AWS account")
    parser.add_argument("--driver", default="Firefox", help="Selenium driver to use (typical values: Firefox, Chrome)")
    args = parser.parse_args()

    print("WARNING - If you proceed here, you will CLOSE the following AWS Account")
    print()
    print("    ", args.email)
    print()
    print("All resources, data and pets in it will be DELETED")
    print("There will be NO FURTHER WARNINGS")
    print()
    args.password = getpass("Password (empty for password reset):")

    if not args.password or not args.password.strip():
        args.password = reset_password(args.driver, args.email)
        print("Reset Password to '" + args.password + "'")

    driver = get_webdriver(args.driver)
    login(driver, args.email, args.password)
    close_account(driver)
    sleep(1)
    driver.close()
    print("The account has (probably) been CLOSED. You will get an email confirmation if it has been successful.")
