import argparse
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from time import sleep
from random import choice
from getpass import getpass


def wait_for_element(driver, by, value):
    print("Waiting for Element ", by, value)
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


def reset_password(email):
    driver = webdriver.Firefox()

    login_part_one(driver, email)
    wait_for_element(driver, By.ID, "root_forgot_password_link").click()
    wait_for_element(driver, By.ID, "password_recovery_done_button").click()
    driver.close()

    recovery_url = input("Paste Recovery URL:")

    driver = webdriver.Firefox()
    driver.get(recovery_url)
    passwd = get_random_password()
    print(passwd)
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
    customize_cookies(driver)


def customize_cookies(driver):
    wait_for_element(driver, By.CSS_SELECTOR, "[data-id=awsccc-cb-btn-customize]").click()
    wait_for_element(driver, By.CSS_SELECTOR, "[data-id=awsccc-u-cb-performance-container]").click()
    driver.find_element(By.CSS_SELECTOR, "[data-id=awsccc-cs-btn-save]").click()


def close_account(driver):
    driver.get("https://console.aws.amazon.com/billing/home?#/account")
    wait_for_element(driver, By.CSS_SELECTOR, "[data-testid=aws-billing-account-form-button-close-account]")
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
    for testid in [
        "aws-billing-account-form-input-is-closing-account",
        "aws-billing-account-form-input-is-second-closing-account",
        "aws-billing-account-form-input-is-third-closing-account",
        "aws-billing-account-form-input-is-fourth-closing-account",
    ]:
        driver.find_element(By.CSS_SELECTOR, f"[data-testid={testid}]").click()
    driver.find_element(By.CSS_SELECTOR, "[data-testid=aws-billing-account-form-button-close-account]").click()
    wait_for_element(driver, By.CSS_SELECTOR, "[data-testid=aws-billing-account-modal-button-close-account]").click()


def main():
    parser = argparse.ArgumentParser(
        description="""
        Close the AWS account identified by the email, optionally performing a password reset.
        This program requires an installed selenium driver to run.
        It was tested using the selenium driver for firefox 0.30.0
        installed from https://github.com/mozilla/geckodriver/releases .
        The input window waits for you to input any captchas and possibly MFA Keys (not tested yet)
    """
    )

    parser.add_argument("email", help="Email associated with the AWS account")
    args = parser.parse_args()
    args.password = getpass("Password (empty for password reset):")

    if not args.password or not args.password.strip():
        args.password = reset_password(args.email)

    driver = webdriver.Firefox()
    login(driver, args.email, args.password)
    close_account(driver)
    sleep(1)
    driver.close()
