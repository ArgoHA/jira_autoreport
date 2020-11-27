import sys, os, requests, datetime, json, time, yaml
from requests.auth import HTTPBasicAuth
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


# Логинимся в AppDynamics
def login_apd():
    driver.get('http://link.ru')
    time.sleep(5)

    write_login = driver.find_element_by_xpath('//*[@id="userNameInput"]')
    write_login.send_keys(login)

    write_password = driver.find_element_by_xpath('//*[@id="passwordInput"]')
    write_password.send_keys(password)

    enter = driver.find_element_by_xpath('//*[@id="submitInput"]')
    enter.click()
    time.sleep(3)


# Проходим по ссылке и делаем скрин шот нужного элемента
def get_a_screenshot():
    driver.get(url_apd)
    time.sleep(wait_for_dash)
    element = driver.find_element_by_xpath(xpath)
    element.screenshot(image_path)


event_name_raw = sys.argv[7][1:-1] # избавляемся от кавычек

event_names_to_fire = ['rule_1', 'rulu_2'] # Список правил, при срабатывании которых нужно звести задачу в jira

if event_name_raw in event_names_to_fire:
    event_name = 'template_1'
else:
    print('Incorrect rule name')
    sys.exit()

config_file_name = sys.argv[0].replace('py', 'yml') # универсальная ссылка на настроечный файл
with open(config_file_name, encoding='utf8') as f:
    full_data = yaml.safe_load(f)

###################   Получаю данные из настроечного файла
project_name = full_data[event_name]['project_name']
priority = full_data[event_name]['priority']
issue_type = full_data[event_name]['issue_type']
watcher = full_data[event_name]['watcher']
assignee = full_data[event_name]['assignee']
subject = full_data[event_name]['subject']
text = full_data[event_name]['text']
lable = full_data[event_name]['lable']

url_apd = full_data[event_name]['url_apd']
wait_for_dash = full_data[event_name]['wait_for_dash']
xpath = full_data[event_name]['xpath']

login = full_data['auth']['appdynamics'][0]['login']
password =  full_data['auth']['appdynamics'][1]['password']
image_path = os.path.dirname(os.path.abspath(sys.argv[0])) + "/image.png"
####################

try:
    # создаем виртуальный браузер
    options = webdriver.ChromeOptions()
    options.add_argument('window-size=2100x1440')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.headless = True
    driver = webdriver.Chrome(options=options)

    login_apd() # логинимся
    get_a_screenshot() # получаем скрин шот

    date = datetime.datetime.now().date()

    headers = {"X-Atlassian-Token": "nocheck"}

    data = {
        "fields": {
        "project":
        {
            "key": project_name
        },
        "summary": subject,
        "description": text,
        "duedate": str(date),
        "labels":  [
                lable
            ],
            "priority": {
            "name": priority
            },
            "customfield_11005": [{
            "name": watcher}
            ],
        "assignee":{
            "name": assignee
        },
        "issuetype": {
            "name": issue_type
        }
    }
    }

    # готовим фотку
    files = {'file': open(image_path, 'rb')}

    # создаем задачу
    response = requests.post('http://link/rest/api/2/issue/', json = data, headers = headers, auth=HTTPBasicAuth('login', 'password')).json()

    # получаем id задачи
    issue_id = response['id']
    issue_url = f'http://link/rest/api/2/issue/{issue_id}/attachments'

    # прикрепляем картинку
    attach_img = requests.post(issue_url, files=files, headers = headers, auth=HTTPBasicAuth('login', 'password'))

finally:
    driver.quit() # Закрываем браузер, убиваем процессы
