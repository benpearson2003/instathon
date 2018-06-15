import webbrowser, sys, re, selenium, os, time, shutil
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

def run(uploadDirectory, daily_limit):

    mobile_emulation = {
    	#"deviceName": "Apple iPhone 3GS"
    	#"deviceName": "Apple iPhone 4"
    	#"deviceName": "Apple iPhone 5"
    	#"deviceName": "Apple iPhone 6"
    	#"deviceName": "Apple iPhone 6 Plus"
    	#"deviceName": "BlackBerry Z10"
    	#"deviceName": "BlackBerry Z30"
    	#"deviceName": "Google Nexus 4"
    	"deviceName": "Google Nexus 5"
    	#"deviceName": "Google Nexus S"
    	#"deviceName": "HTC Evo, Touch HD, Desire HD, Desire"
    	#"deviceName": "HTC One X, EVO LTE"
    	#"deviceName": "HTC Sensation, Evo 3D"
    	#"deviceName": "LG Optimus 2X, Optimus 3D, Optimus Black"
    	#"deviceName": "LG Optimus G"
    	#"deviceName": "LG Optimus LTE, Optimus 4X HD"
    	#"deviceName": "LG Optimus One"
    	#"deviceName": "Motorola Defy, Droid, Droid X, Milestone"
    	#"deviceName": "Motorola Droid 3, Droid 4, Droid Razr, Atrix 4G, Atrix 2"
    	#"deviceName": "Motorola Droid Razr HD"
    	#"deviceName": "Nokia C5, C6, C7, N97, N8, X7"
    	#"deviceName": "Nokia Lumia 7X0, Lumia 8XX, Lumia 900, N800, N810, N900"
    	#"deviceName": "Samsung Galaxy Note 3"
    	#"deviceName": "Samsung Galaxy Note II"
    	#"deviceName": "Samsung Galaxy Note"
    	#"deviceName": "Samsung Galaxy S III, Galaxy Nexus"
    	#"deviceName": "Samsung Galaxy S, S II, W"
    	#"deviceName": "Samsung Galaxy S4"
    	#"deviceName": "Sony Xperia S, Ion"
    	#"deviceName": "Sony Xperia Sola, U"
    	#"deviceName": "Sony Xperia Z, Z1"
    	#"deviceName": "Amazon Kindle Fire HDX 7″"
    	#"deviceName": "Amazon Kindle Fire HDX 8.9″"
    	#"deviceName": "Amazon Kindle Fire (First Generation)"
    	#"deviceName": "Apple iPad 1 / 2 / iPad Mini"
    	#"deviceName": "Apple iPad 3 / 4"
    	#"deviceName": "BlackBerry PlayBook"
    	#"deviceName": "Google Nexus 10"
    	#"deviceName": "Google Nexus 7 2"
    	#"deviceName": "Google Nexus 7"
    	#"deviceName": "Motorola Xoom, Xyboard"
    	#"deviceName": "Samsung Galaxy Tab 7.7, 8.9, 10.1"
    	#"deviceName": "Samsung Galaxy Tab"
    	#"deviceName": "Notebook with touch"

    	# Or specify a specific build using the following two arguments
    	#"deviceMetrics": { "width": 360, "height": 640, "pixelRatio": 3.0 },
        #"userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
	}

    options = webdriver.ChromeOptions()
    options.add_experimental_option("mobileEmulation", mobile_emulation)
    browser = webdriver.Chrome(chrome_options=options)
    browser.set_window_size(200,200)

    i = 0
    try:
        for filename in os.listdir(uploadDirectory):
            i += 1
            if i > daily_limit:
                break

            browser.get('https://www.instagram.com')

            try:
                emailElem = browser.find_element_by_id('ap_email')
                userEmail = input('Enter your email: ')
                userPass = input('Enter your password: ')
                emailElem.send_keys(userEmail)
                passwordElem = browser.find_element_by_id('ap_password')
                passwordElem.send_keys(userPass)
                passwordElem.submit()
            except:
                pass

            #wait to get past login screen, either by automatic login or by user logging in
            WebDriverWait(
                        browser, 90
                ).until(EC.presence_of_element_located((By.ID, 'data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-AjaxInput')))

            #upload file
            browser.find_element_by_id("data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-AjaxInput").send_keys(os.getcwd()+"/"+s['file'])

            try:
                print("waiting for processing message to appear")
                WebDriverWait(
                        browser, 60
                ).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '#data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-uploading-message.a-hidden')))

                print("waiting for processing message to disappear")
                WebDriverWait(
                        browser, 60
                ).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#data-draft-tshirt-assets-front-image-asset-cas-shirt-art-image-file-upload-uploading-message.a-hidden')))

                time.sleep(4)

                print("clicking continue")
                browser.find_element_by_id("save-and-continue-upload-art-announce").click()
            except:
                print("timed out looking")

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-draft-list-prices-marketplace-1-amount')))
            #new we must set price, shirt type, fit type, and colors
            #set Price
            priceElem = browser.find_element_by_id("data-draft-list-prices-marketplace-1-amount")
            priceElem.clear()
            priceElem.send_keys(s['price'])

            #fit type
            fits = s['fit'].split(",")
            fits = [x.strip(' ') for x in fits]

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-shirt-configurations-fit-type-men')))
            #men and women selected by default, do opposite
            if not any(f in fits for f in ["MEN","MENS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-men").send_keys(selenium.webdriver.common.keys.Keys.SPACE)
            if not any(f in fits for f in ["WOMEN","WOMENS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-women").send_keys(selenium.webdriver.common.keys.Keys.SPACE)
            if any(f in fits for f in ["YOUTH","YOUTHS","KID","KIDS"]):
                browser.find_element_by_id("data-shirt-configurations-fit-type-youth").send_keys(selenium.webdriver.common.keys.Keys.SPACE)

            #do colors
            colors = s['color'].split(",")
            colors = [x.strip().replace(" ","_").replace("-","_").lower() for x in colors]

            #selected by default, remove
            browser.find_element_by_id("gear-checkbox-silver").click()

            for c in colors:
                browser.find_element_by_id("gear-tshirt-image").click()
                time.sleep(.25)
                n = c.lower()

                browser.find_element_by_id("gear-checkbox-"+n).click()

            #continue
            browser.find_element_by_id("save-and-continue-choose-variations-announce").click()

            WebDriverWait(
                        browser, 20
                ).until(EC.visibility_of_element_located((By.ID, 'data-draft-brand-name')))

            #text details
            browser.find_element_by_id('data-draft-brand-name').send_keys(s['brand'])
            browser.find_element_by_id('data-draft-name-en-us').send_keys(s['title'])
            browser.find_element_by_id('data-draft-bullet-points-bullet1-en-us').send_keys(s['feat1'])
            browser.find_element_by_id('data-draft-bullet-points-bullet2-en-us').send_keys(s['feat2'])
            browser.find_element_by_id('data-draft-description-en-us').send_keys(s['desc'])
            browser.find_element_by_id("save-and-continue-announce").click()

            WebDriverWait(
                        browser, 20
                ).until(EC.presence_of_element_located((By.ID, 'publish-announce')))

            #review and submit
            browser.find_element_by_xpath("//*[contains(text(), 'Sell - Public on Amazon')]").click()
            time.sleep(4)
            browser.find_element_by_id("publish-announce").click()
            time.sleep(4)
            browser.execute_script("document.getElementById('publish-confirm-button-announce').click();")

            WebDriverWait(
                        browser, 60
                ).until(EC.presence_of_element_located((By.ID, 'landing-page')))

    finally:
        browser.close()
