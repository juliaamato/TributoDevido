import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

def main():
    
    driver = defineDriver()
    driver.get('https://www.upwork.com/freelance-jobs/apply/Build-bot-copy-crypto-wallet-address_~021844608955247838835/')
    time.sleep(5)
    # clickJobs(driver)
    pegarInfo(driver)
    
def defineDriver():
    options = webdriver.FirefoxOptions()
    driver = webdriver.Firefox(options=options)
    return driver

def clickJobs(driver):
    elements = driver.find_elements(By.CLASS_NAME, 'job-tile-wrapper')
    actions = ActionChains(driver)

    wait = WebDriverWait(driver, 10)
    close_button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#onetrust-close-btn-container button")))
    close_button.click()
    time.sleep(7)
    # elements[0].click()
    actions.key_down(Keys.CONTROL) \
    .click(elements[0]) \
    .key_up(Keys.CONTROL) \
    .perform()
    driver.switch_to.window(window_name=driver.window_handles[-1])
           
    # for x in elements:
    #     print ("oii")
    #     actions.key_down(Keys.CONTROL) \
    #    .click(x) \
    #    .key_up(Keys.CONTROL) \
    #    .perform()
    #     driver.switch_to.window(window_name=driver.window_handles[-1])
        
def pegarInfo(driver):
    print("pegar info")
    titulo = driver.find_element(By.TAG_NAME, 'h4')
    print (titulo.text)
    aux = titulo.find_element(By.XPATH, '../../..')
    print ("aux foi")
    descricao = driver.find_element(By.CLASS_NAME, 'text-body-sm')
    print (descricao.text)
    infos = aux.find_elements(By.TAG_NAME, 'section')
    infos = infos[1].find_element(By.TAG_NAME, 'ul')
    
    infos = infos.find_elements(By.TAG_NAME, 'li')
    # print("aaaaaaaaaaaaaaaaaaa", infos[3].find_element(By.TAG_NAME, 'strong').text)
    # print(len(infos))
    informacoes = []
    auxiliar = ""
    for x in infos:
        aux = x.find_elements(By.TAG_NAME, 'strong')
        if len(aux)== 1:
            informacoes.append(aux[0].text)
        else:
            for y in aux:
                auxiliar = auxiliar + y.text
            informacoes.append(auxiliar)
            auxiliar = ""
    print("stronggg", informacoes)

    skillsAux = driver.find_element(By.XPATH, '//*[contains(text(),"Skills and Expertise")]/..')
    skillsAux = skillsAux.find_element(By.TAG_NAME, 'div')
    skillsAux = skillsAux.find_elements(By.TAG_NAME, 'span')
    print (len(skillsAux))
    for x in skillsAux:
        print(x.text)
    print("Chegou no final")
      
    
if __name__ == main():
    main()