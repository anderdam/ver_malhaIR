import os

import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# Get the absolute path of the directory where your code is located
code_dir = os.path.abspath(os.path.dirname(__file__))

# Create the path for the screenshots directory
screenshots_dir = os.path.join(code_dir, 'screenshots')

# Create the screenshots directory if it doesn't exist
if not os.path.exists(screenshots_dir):
    os.makedirs(screenshots_dir)

options = webdriver.EdgeOptions()
options.add_argument('--incognito')
# options.add_argument('--headless')

driver_path = os.path.join(code_dir, 'edgedriver')
driver = webdriver.Edge(options=options)

ecac = 'https://cav.receita.fazenda.gov.br/autenticacao/login'

# Read the CSV file into a pandas DataFrame with the desired changes
df = pd.read_csv('PROCESSAMENTOS.csv', header=0, na_values=['NaN'], dtype={'CPF': str, 'STATUS': str, 'NOME': str, 'CÓDIGO': str, 'SENHA': str})
df = df.fillna('')

# Print the first 5 rows of the DataFrame
# print(df)

driver.get(ecac)
print('ok ecac')
df.to_excel('processamentos.xlsx', engine='xlsxwriter', index=False)

# Loop over the rows of the DataFrame
for index, row in df.iterrows():
    # Check if the value in the fourth column of the current row is empty
    if row[3] == '':
        print(f"{row[4]} = '' and was skipped.")
    else:
        # If it's not empty, use the value as a key in Selenium
        key = row[3]
        # Use the key to interact with the webpage using Selenium
        cpf = driver.find_element(by='id', value='NI')
        cpf.send_keys(df['CPF'][index])
        print(f"Checkpoint: {df['CPF'][index]}")
        code = driver.find_element(by='id', value='CodigoAcesso')
        code.send_keys(df['CÓDIGO'][index])
        print(f"Checkpoint: {df['CÓDIGO'][index]}")
        passwd = driver.find_element(by='id', value='Senha')
        passwd.send_keys(df['SENHA'][index])
        print(f"Checkpoint: {df['SENHA'][index]}")
        submit = driver.find_element(by='xpath', value='//input[@class="submit"]')
        submit.submit()
        print('Checkpoint: Avançar')
        driver.implicitly_wait(2)
        if driver.find_element(By.CLASS_NAME, "login-caixa-erros-validacao"):
            print('Algo de errado não está certo!!!')
            print('Cheque os dados e tente novamente')
            print('-' * 50)

            driver.find_element(by='id', value='NI').clear()
            driver.find_element(by='id', value='CodigoAcesso').clear()
            driver.find_element(by='id', value='Senha').clear()
        else:
            continue

meu_imposto_link = driver.find_element(by='xpath', value='//a[@href="https://irpf.cav.receita.fazenda.gov.br/portalmir/ecac"]')
meu_imposto_link.click()
print('Checkpoint: meu imposto')

driver.switch_to.window(driver.window_handles[-1])
driver.implicitly_wait(2)

screenshot_name = f"{df['NOME']}.png"
screenshot_path = os.path.join(screenshots_dir, screenshot_name)
driver.save_screenshot(screenshot_path)
print('Checkpoint: screenshot')

status = driver.find_element(By.CLASS_NAME, 'situacao')
status_2023 = status.text
print(status_2023)
