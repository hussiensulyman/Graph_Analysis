from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import time

path = "C:/Program Files/chromedriver.exe"
service = Service(path)

driver = webdriver.Chrome(service=service)
driver.get("https://scholar.google.com/citations?view_op=search_authors&hl=en&mauthors=mit&btnG=")
time.sleep(3)

search_words = ['University of Oxford', 'Harvard University', 'Stanford University', 'University of Cambridge',
                'Massachusetts Institute of Technology (MIT)',
                'California Institute of Technology', 'Princeton University', 'University of California, Berkeley',
                'Yale University', 'Imperial College']
doctors = []

for search_word in search_words:
    search_box = driver.find_element(By.ID, 'gs_hdr_tsi')
    search_box.clear()
    search_box.send_keys(search_word)
    search_box.send_keys('\n')
    time.sleep(10)

    for page in range(21):
        element = driver.find_element(By.ID, 'gsc_sa_ccl')
        sub_div = element.find_elements(By.CLASS_NAME, "gs_ai_t")

        for i in sub_div:
            university = i.find_element(By.CLASS_NAME, 'gs_ai_aff').text
            name = i.find_element(By.CLASS_NAME, 'gs_ai_name').text
            specializations = []
            try:
                specialization_elements = i.find_elements(By.CSS_SELECTOR, 'div.gs_ai_int a')
                for element in specialization_elements:
                    specializations.append(element.text)
            except:
                pass
            doctors.append({'Search Word': search_word, 'University': university, 'Name': name,
                            'Specializations': ", ".join(specializations)})

        try:
            next_page_btn = driver.find_element(By.CSS_SELECTOR,
                                                "button.gs_btnPR.gs_in_ib.gs_btn_half.gs_btn_srt.gsc_pgn_pnx")
            next_page_btn.click()
            time.sleep(7)
        except:
            break

df = pd.DataFrame(doctors)
df.to_csv('doctors.csv', index=False)

driver.quit()
