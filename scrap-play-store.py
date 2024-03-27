from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains

from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import time

# in pixels
CONTAINER_SCROLLABLE_HEIGHT = 616
CONTAINER_LIST_INITIAL_HEIGHT = 4679

install_chrome = ChromeDriverManager().install()
config = Service(install_chrome)
browser = webdriver.Chrome(service=config)

# class="VfPpkd-Bz112c-LgbsSe yHy1rc eT1oJ QDwDD mN1ivc VxpoF"

print("Loading website")
browser.get(
    "https://play.google.com/store/apps/details?id=br.gov.pi.pidigital&hl=pt&pli=1"
)
print("Starting webscrapping")
time.sleep(3)

# Scroll to header target
print("scrolling until the button")
browser.execute_script("window.scroll(0, 700)")
time.sleep(1)

# Catch button to click
headers_sections = browser.find_elements(By.CLASS_NAME, "cswwxf")
header_comments = headers_sections[2]

button_all_evaluations = header_comments.find_element("xpath", "div[1]/div[2]/button")
print("clicking in the button")
time.sleep(1)

# Clicking in button
ActionChains(browser).click(button_all_evaluations).perform()
time.sleep(1)

# Catching list of evaluations
container_list_evaluations = browser.find_element(By.CLASS_NAME, "odk6He")
list_evaluations = container_list_evaluations.find_element("xpath", "div[2]")

# Scrolling modal until the end
modal = browser.find_element(By.CLASS_NAME, "fysCi")

currentScrollPosition = 0
totalRelativeHeight = container_list_evaluations.size["height"]
print("scrolling until the end of modal")
while currentScrollPosition != totalRelativeHeight:
    # print("totalRelativeHeight(0): ", totalRelativeHeight)
    # print("currentScrollPosition(0): ", currentScrollPosition)

    currentScrollPosition = totalRelativeHeight

    browser.execute_script(f"arguments[0].scrollTop = {currentScrollPosition}", modal)

    container_list_evaluations = browser.find_element(By.CLASS_NAME, "odk6He")
    totalRelativeHeight = container_list_evaluations.size["height"]

    # print("totalRelativeHeight(2): ", totalRelativeHeight)
    # print("currentScrollPosition(2): ", currentScrollPosition)

    print("going down more...")
    time.sleep(1)

print("Modal arrives in the end...")
print("Collecting all users evaluations ")
time.sleep(2)


# Converter webdriver object in html string
html_string = list_evaluations.get_attribute("outerHTML")
bs = BeautifulSoup(html_string, "html.parser")
evaluations = bs.find_all("div", {"class": "RHo1pe"})

array_evaluations = []

# Looping through comments array
for evaluation in evaluations:
    evaluation_owner_name = evaluation.find("div", {"class": "X5PpBb"}).text
    # search by first number in string of avaliations
    evaluation_stars = (
        evaluation.find("div", {"class": "iXRFPc"}).get("aria-label").split(" ")[2]
    )
    evaluation_date = evaluation.find("span", {"class": "bp9Aid"}).text
    evaluation_comment = evaluation.find("div", {"class": "h3YV2d"}).text

    evaluation_relevance = 0
    try:
        evaluation_relevance = evaluation.find("div", {"class", "AJTPZc"}).text.split(
            " "
        )[-2]
    except:
        print("This evaluation has no relevance. Then it will be iqual 0")

    evaluation_factory = {
        "owner_name": evaluation_owner_name,
        "stars": evaluation_stars,
        "date": evaluation_date,
        "comment": evaluation_comment,
        "relevance": evaluation_relevance,
    }

    array_evaluations.append(evaluation_factory)

    print("Collected evaluation!")
    # print("====   +   ====")
    # print("evaluation_owner_name: ", evaluation_owner_name)
    # print("evaluation_stars: ", evaluation_stars)
    # print("evaluation_date: ", evaluation_date)
    # print("evaluation_comment: ", evaluation_comment)
    # print("evaluation_relevance: ", evaluation_relevance)

print("====   +   ====")
print(f"Total evaluations: {len(array_evaluations)}")
print("====   +   ====")

with open("evaluations.txt", "w") as arquivo:
    for item in array_evaluations:
        # print("item: ", item)

        arquivo.write(
            f"{item['owner_name']} evaluated {item['stars']} star(s) in {item['date']} and have {item['relevance']} of relevance"
            + "\n\n"
        )
