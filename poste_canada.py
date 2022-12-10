import re
import time
import pyautogui
from PyQt5.QtWidgets import QInputDialog
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from webdriver_manager.chrome import ChromeDriverManager

pyautogui.PAUSE = 1
pyautogui.FAILSAFE = True
gran_pause = 3
search_time = 20

std_dim1 = "19.5"
std_dim2 = "25.5"
std_dim3 = "1"
std_weight = "17.5"

name_ship = "Luc Plouffe"
email_ship = "guil.lvsq@gmail.com"
adress_ship = "133 Rue Lapointe, Lachute, QC J8H 4L8"
PO_ship = "D22091865-1"
type_ship = "S"

label_path = "C:/Users/g-lev/My Drive/Dragar Inc/ventes et achats/factures recues/shipping labels/"

def poste_can(
        client_email,
        client_name,
        client_adr,
        client_order_id,
        std_sm,
        self,
        dim1_in=std_dim1,
        dim2_in=std_dim2,
        dim3_in=std_dim3,
        weight_lbs=std_weight):
    # startup
    time.sleep(gran_pause)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.canadapost-postescanada.ca/cpc/en/")
    driver.maximize_window()

    # functions
    def click_button_when_appears(xpath):
        WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).click()

    def click_if_exists(xpath):
        if WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, xpath))):
            driver.find_element(By.XPATH, xpath).click()

    def get_value_when_appears(xpath):
        WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        return driver.find_element(By.XPATH, xpath).get_attribute("innerHTML")

    def get_value_if_exists(xpath):
        if WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, xpath))):
            return driver.find_element(By.XPATH, xpath).get_attribute("innerHTML")
        return -1

    def type_when_appears(xpath, text):
        WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, xpath)))
        driver.find_element(By.XPATH, xpath).send_keys(text)

    def is_present(xpath):
        return len(driver.find_elements(By.XPATH, xpath)) > 0

    # connect
    time.sleep(gran_pause)

    # click_button_when_appears('//*[@id="freLangSelector"]')
    click_button_when_appears('//*[@id="engLangSelector"]')
    click_button_when_appears('//*[@id="signinModalLarge"]')

    user = "guillaumelevesque"
    passw = "po194HAX$"
    popup_user_field = '//*[@id="usernameLarge"]'
    popup_pw_field = '//*[@id="passwordLarge"]'
    page_user_field = '//*[@id="f-username"]'
    page_pw_field = '//*[@id="f-password"]'
    waiting_for_login = True
    while waiting_for_login:
        if is_present(popup_user_field):
            type_when_appears(popup_user_field, user)
            type_when_appears(popup_pw_field, passw)
            driver.find_element(By.XPATH, popup_pw_field).submit()
            waiting_for_login = False
        if is_present(page_user_field):
            type_when_appears(page_user_field, user)
            type_when_appears(page_pw_field, passw)
            driver.find_element(By.XPATH, page_pw_field).submit()
            # dropdown menu
            click_button_when_appears('//*[@id="mainNav"]/div[1]/nav/div[1]/section/ul/li[4]/a[1]')
            click_button_when_appears('//*[@id="mainNav"]/div[1]/nav/div[1]/section/ul/li[4]/ul/li[1]/a')
            waiting_for_login = False

    # open tool (and double factor check)
    time.sleep(gran_pause)
    double_factor = '//*[@id="cpc-app-main"]/div/cpc-mfa-opt-in/cpc-phone-number-form/div/div/a[2]'
    open_tool_btn = '/html/body/div[1]/div[2]/cpc-footer/div[2]/div/div[2]/a'
    checking_for_double_factor = True
    while checking_for_double_factor:
        if is_present(double_factor):
            click_button_when_appears(double_factor)
            checking_for_double_factor = False
        if is_present(open_tool_btn):
            checking_for_double_factor = False

    click_button_when_appears(open_tool_btn)

    # créer une etiquette d'expedition
    create_shipping_label = '/html/body/div[1]/cpc-app-root/div[2]/section/div/cpc-home-page/div[2]/div/section[2]/div/cpc-parcel-shipment-card/div[3]/button[1]'
    click_if_exists(create_shipping_label)

    click_button_when_appears('//*[@id="createShipmentFromEmptyCart"]')

    # expediteur
    time.sleep(gran_pause)
    if std_sm == "S":
        max_ship_from = '/html/body/div[1]/div/main/div/div/app-root/app-shipment/div/div[1]/mat-accordion/mat-expansion-panel[1]/div/div/app-from-container/div/div/app-from/div/form/div[2]/div[2]/div[2]'
        click_button_when_appears(max_ship_from)
    else:
        pa_ship_from = '/html/body/div[1]/div/main/div/div/app-root/app-shipment/div/div[1]/mat-accordion/mat-expansion-panel[1]/div/div/app-from-container/div/div/app-from/div/form/div[2]/div[2]/div[1]'
        click_button_when_appears(pa_ship_from)
    time.sleep(gran_pause)
    WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="sendDeliveryUpdate"]')))
    driver.find_element(By.XPATH, '//*[@id="sendDeliveryUpdate"]').click()
    WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="fromNext"]')))
    driver.find_element(By.XPATH, '//*[@id="fromNext"]').click()

    # destinataire
    time.sleep(gran_pause)
    WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="destinationName"]')))
    driver.find_element(By.XPATH, '//*[@id="destinationName"]').send_keys(client_name)
    driver.find_element(By.XPATH, '//*[@id="destination-address-complete-line-1"]').send_keys(client_adr + "X")
    driver.find_element(By.XPATH, '//*[@id="destination-address-complete-line-1"]').send_keys(Keys.BACKSPACE)
    time.sleep(gran_pause)
    WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="Address Complete_results_item0"]')))
    driver.find_element(By.XPATH, '//*[@id="Address Complete_results_item0"]').click()
    WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="additionalEmail"]')))
    driver.find_element(By.XPATH, '//*[@id="additionalEmail"]').click()
    WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="additionalInfo2"]')))
    driver.find_element(By.XPATH, '//*[@id="additionalInfo2"]').send_keys(client_email)
    time.sleep(gran_pause)
    WebDriverWait(driver, search_time).until(ec.element_to_be_clickable((By.XPATH, '//*[@id="toNext"]')))
    driver.find_element(By.XPATH, '//*[@id="toNext"]').click()

    # Paquet
    time.sleep(gran_pause)
    click_button_when_appears('//*[@id="cdk-accordion-child-2"]/div/app-package-container/div/div/app-package/div/form/div/div[3]/app-package-item/div/div/div[2]/label')
    click_button_when_appears('//*[@id="packageSwitchToImperial"]')
    WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, '//*[@id="boxLength"]')))
    driver.find_element(By.XPATH, '//*[@id="boxLength"]').send_keys(dim1_in)
    driver.find_element(By.XPATH, '//*[@id="boxWidth"]').send_keys(dim2_in)
    driver.find_element(By.XPATH, '//*[@id="boxHeight"]').send_keys(dim3_in)
    driver.find_element(By.XPATH, '//*[@id="boxWeight"]').send_keys(weight_lbs)
    time.sleep(gran_pause)
    click_button_when_appears('//*[@id="packageNext"]')

    # expedition
    time.sleep(gran_pause)
    prodDesc = '//*[@id="servicePanel_productDesciption0"]'
    # criss = '//*[@id="servicePanel_Colisaccélérés_optionCheckbox7"]'
    criss = '//*[@id="servicePanel_ExpeditedParcel_optionCheckbox7"]'
    # esti = '//*[@id="servicePanel_Colisaccélérés_COV"]'
    esti = '//*[@id="servicePanel_ExpeditedParcel_COV"]'
    click_button_when_appears(prodDesc)
    click_button_when_appears(criss)
    WebDriverWait(driver, search_time).until(ec.visibility_of_element_located((By.XPATH, esti)))
    driver.find_element(By.XPATH, esti).send_keys("100")
    click_button_when_appears('//*[@id="serviceNext"]')

    # get shipping price
    shipping_price_brut = get_value_when_appears('//*[@id="totalPrice"]')
    try:
        shipping_price_moins_brut = re.match(r"\d*,\d*", shipping_price_brut).group()

    except:
        shipping_price_moins_brut = re.match(r"\d*.\d*", shipping_price_brut).group()

    shipping_price = re.sub(r"\,", ".", shipping_price_moins_brut)
    print("paiement à faire")
    pyautogui.hotkey('alt', 'tab')

    # todo: afficher l'adresse et prix sur le popup
    text, ok = QInputDialog.getText(self, "Input", "Enter security digits")
    print("Text: ", text)
    print("Ok: ", ok)

    # todo: automatiser les boutons pour paiement avec le security code,
    #  jusqu'au screen de payment complete

    # screen de payment complete
    print("10 sec pour retourner à la page de confirmation")
    time.sleep(10)
    click_button_when_appears('//*[@id="printLabel"]')

    time.sleep(15)
    pyautogui.hotkey('ctrl', 'p')
    time.sleep(10)
    pyautogui.press(['enter'])
    time.sleep(10)
    ship_file_name = client_order_id + " - shipping label"
    pyautogui.write(ship_file_name)
    time.sleep(2)
    pyautogui.hotkey('alt', 'd')
    time.sleep(2)
    pyautogui.write(label_path)
    time.sleep(2)
    pyautogui.press(['enter'])
    time.sleep(2)
    pyautogui.hotkey('alt', 's')
    time.sleep(10)
    full_ship_path = label_path + ship_file_name + ".pdf"
    return [full_ship_path, shipping_price]


# test eh
if __name__ == "__main__":
    poste_can(email_ship, name_ship, adress_ship, PO_ship, type_ship)