import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from backend import insert, connect, disconnect


project_data = {
    "payment": None,
    "payment_method": None,
    "contract": None,
    "experience": None,
    "project": None,
    "work": None,
    "tags": [],
    "description": None
}

def main():
    
    driver = defineDriver()
    #driver.get('https://www.upwork.com/freelance-jobs/apply/Build-bot-copy-crypto-wallet-address_~021844608955247838835/')
    #driver.get('https://www.upwork.com/freelance-jobs/apply/Development-Mega-Personals-Verification-Bot_~021844749363071525510/')
    driver.get('https://www.upwork.com/freelance-jobs/apply/Spring-Boot-Python-Developer-with-PowerBI-API-Experience_~021847314575476327641/')
    time.sleep(5)
    conn = connect()
    
    insert(conn, getInfo(driver))
    
    disconnect(conn)

    driver.close()
    
def defineDriver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    return driver

        
def getInfo(driver):

    title = driver.find_element(By.TAG_NAME, 'h4')
    aux = title.find_element(By.XPATH, '../../..')
    infos = aux.find_elements(By.TAG_NAME, 'section')
    infos = infos[1].find_element(By.TAG_NAME, 'ul')
    infos = infos.find_elements(By.TAG_NAME, 'li')

    skillsAux = driver.find_element(By.XPATH, '//h5[contains(text(),"Skills and Expertise")]/..')
    driver.execute_script("arguments[0].style.display = 'block';", driver.find_element(By.ID, "popper_1"))
    project_data["tags"] = [x.text for x in skillsAux.find_elements(By.XPATH, ".//span[@slot='reference']") if x.text]
    project_data["description"] = driver.find_element(By.CLASS_NAME, 'text-body-sm').text

    setJson(infos)

    return project_data 
   

def setJson(infos):

    infoList= []
    aux = ""

    for x in infos:
        type_elements = x.find_elements(By.CLASS_NAME, 'description')
        strong_elements = x.find_elements(By.TAG_NAME, 'strong')

        if len(strong_elements) == 1:
            infoList.append(strong_elements[0].text)
        else:
            aux = " - ".join([y.text for y in strong_elements if y.text != ""])
            infoList.append(aux)

        if type_elements:
            description_text = type_elements[0].text
            if "Experience Level" in description_text:
                project_data["experience"] = strong_elements[0].text if strong_elements else ""
            elif "Duration" in description_text:
                project_data["contract"] = strong_elements[0].text if strong_elements else ""
            elif any(keyword in description_text for keyword in ["Hourly", "Fixed-price"]):
                if project_data["payment"] is None:
                    project_data["payment"] = strong_elements[0].text if strong_elements else ""
                else:
                    project_data["payment_method"] = project_data["payment"]
                    project_data["payment"] = strong_elements[0].text if strong_elements else ""
            elif "Project Type" in description_text:
                project_data["project"] = strong_elements[0].text if strong_elements else ""
        else:
            project_data["work"] = strong_elements[0].text if strong_elements else ""

    
      
    
if __name__ == main():
    main()