import json
import os
from selenium import webdriver
from selenium.webdriver.common.by import By

#Driver options
options = webdriver.FirefoxOptions()

#Profile options
profile = webdriver.FirefoxProfile()

# Set the download directory
download_dir = "./"
profile = {
    "browser.download.dir": download_dir,  # Set download directory
    "browser.download.folderList": 2,  # 2 = use custom location
    "browser.download.manager.showWhenStarting": False,  # Hide the download manager
    "browser.download.useDownloadDir": True,  # Use the download directory
    "pdfjs.disabled": True,  # Disable the built-in PDF viewer (optional)
    "browser.helperApps.neverAsk.saveToDisk": "application/octet-stream,application/pdf"  # (optional) Set MIME types
}

# Apply preferences to options
for key, value in profile.items():
    options.set_preference(key, value)

#options.add_argument("--headless=new")
driver = webdriver.Firefox(options=options)

#Searching each page and adding pool ids to list
def page_search(id_list, all_links_list):
    
    for tourn in id_list:
        #Navigating to pool page
        driver.get("https://fencingtimelive.com/tournaments/eventSchedule/" + tourn)
        
        events = driver.find_elements(By.CLASS_NAME, "clickable-row")
        event_list = []
        for i in events:
            j ="https://fencingtimelive.com" + i.get_attribute("data-href")
            event_list.append(j)

        for event in event_list:
            driver.get(event)
            pools = driver.find_element(By.XPATH, "//ul/li[6]/a")
            pools.click()
            pool_page = driver.current_url

            #Grabbing pool ids and storing in list
            id_store = driver.find_element(By.ID, "mainContent")
            id_store_divs = id_store.find_elements(By.XPATH, ".//div[@id]")
            pool_raw_ids = []
            pool_ids = []
            pool_data_links = []
            for div in id_store_divs:
                pool_raw_ids.append(div.get_attribute("id"))

            #Removing useless information from id
            for raw_id in pool_raw_ids:
                pool_ids.append(raw_id.replace("pool_", ""))

            #Getting links for each pool
            for id in pool_ids:
                link = pool_page + "/" + id
                pool_data_links.append(link.replace("scores","details") + "/data")
    
             #Adding to final list  
            for link in pool_data_links:
                all_links_list.append(link)

           


#Navigating through the website
def advanced_search(tournaments): 
    #Getting Page
    driver.get("https://fencingtimelive.com/tournaments/search/advanced")

    #Running advanced search at fencingtimelive and sorting from oldest to newest 
    tourn_name = driver.find_element(By.ID, "searchTournName")
    search_button = driver.find_element(By.ID, "searchBut")
    date_selector = driver.find_element(By.ID, "searchDateFrom")
    date_selector_year = driver.find_element(By.CLASS_NAME, "picker__select--year")
    date_selector_year_2021 = driver.find_element(By.XPATH, "//option[@value='2024']")
    tourn_name.send_keys("ghsfl")
    date_selector.click()
    date_selector_year.click()
    date_selector_year_2021.click()
    date_selector_month = driver.find_element(By.CLASS_NAME, "picker__select--month")
    date_selector_month_september = driver.find_element(By.XPATH, "//option[@value='8']")
    date_selector_month.click()
    date_selector_month_september.click()
    date_selector_day = driver.find_element(By.XPATH, "//div[@class='picker__day picker__day--infocus'][text()='1']")
    date_selector_day.click()
    search_button.click()
    date_decsending = driver.find_element(By.XPATH, "//th[@data-field='dates']")
    date_decsending.click()


    #Grabbing ids for each tournament and saving them into a list
    tournament_list = driver.find_elements(By.CSS_SELECTOR, "[data-uniqueid]")
    for tournament in tournament_list:
        id = tournament.get_attribute("data-uniqueid")
        tournaments.append(id)
    
    #Removing random tournaments (team tournaments, OGHSFL tournaments)
    tournaments.remove("F3178E6E7331476D8254706DF599802B")
    
    #Removing for testing:
    tournaments.remove("9FC70D54C5424BABA27C3B4398EB7E66")
    tournaments.remove("E17292F26ED34498B9294271547A22C6")
    tournaments.remove("03A87AD193CB488BA2C915887BFFBF16")
    tournaments.remove("AFE026E2CB0B40A69E2210706329D0E8")
    tournaments.remove("B5C99C94CA844528AB836491329DE33E")
    tournaments.remove("28DBA28B39ED4A2C8F40E0E3026F7268")
    tournaments.remove("9447492615584601BFF666E42957BEF1")






#Creating JSON file with default information for each fencer
def calc(pools, store, matchlist):

    for pool in pools:
        driver.get(pool)
        pool_table = driver.find_element(By.XPATH, "//table/tbody")
        pool_matches = pool_table.find_elements(By.TAG_NAME, "tr")
        fencer_1 = ""
        fencer_2 = ""
        fencer_1_score = ""
        fencer_2_score = ""
        score_1_clean = ""
        score_2_clean = ""
        elo_fencer_1 = 0
        elo_fencer_2 = 0
        elo_change = 0
        k = 30
        expected = 0;
        fencer_1_win = True
        fencer_2_win = True
        addfen1 = True
        addfen2 = True
        matchname = ""
        winner = ""

        for m in pool_matches:
            match_results = m.find_elements(By.TAG_NAME, "td")
            for i in range(0,len(match_results)):
                if i == 1:
                    fencer_1 = match_results[i].text
                elif i == 4: 
                    fencer_2 = match_results[i].text
                elif i == 2:
                    fencer_1_score = match_results[i].text
                elif i == 3:
                    fencer_2_score = match_results[i].text
            if "V" in fencer_1_score:
                fencer_1_win = True
                fencer_2_win = False
                winner = fencer_1
                score_1_clean = fencer_1_score.replace("V", "")
                score_1_clean = int(score_1_clean)
                score_2_clean = fencer_2_score.replace("D", "")
                score_2_clean = int(score_2_clean)
            elif "D" in fencer_1_score:
                score_1_clean = fencer_1_score.replace("D", "")
                score_1_clean = int(score_1_clean)
                score_2_clean = fencer_2_score.replace("V", "")
                score_2_clean = int(score_2_clean)
                fencer_1_win = False
                fencer_2_win = True
                winner = fencer_2


            matchname = fencer_1 + " VS " + fencer_2 + " " + fencer_1_score + " " + fencer_2_score

            fen1 = {
                "name": fencer_1,
                "team": "",
                "rating": 1000,
                "wins": 0,
                "losses": 0,
                "Average Indicator": 0,
                "Average Seeding": 0,
                "Average Final Ranking": 0,
                "points earned": 0,
                "points lossed": 0
            }

            fen2 = {
                "name": fencer_2,
                "team": "",
                "rating": 1000,
                "wins": 0,
                "losses": 0,
                "Average Indicator": 0,
                "Average Seeding": 0,
                "Average Final Ranking": 0,
                "points earned": 0,
                "points lossed": 0
            }
            
            fenmatch = {
                "match": matchname,
                "Fencer 1": fencer_1,
                "Fencer 1 Score": score_1_clean,
                "Fencer 2": fencer_2,
                "Fencer 2 Score": score_2_clean,
                "Winning Fencer": winner 

            }

            for dict in store:
                if fen1["name"] == dict["name"]:
                    addfen1 = False
                if fen2["name"] == dict["name"]:
                    addfen2 = False;
            matchlist.append(fenmatch) 
            if addfen1:
                store.append(fen1)
            if addfen2:
                store.append(fen2)
            


#Grab events from every tournaments
def get_events(t_list, e_list):
    for t in t_list:
        driver.get("https://www.fencingtimelive.com/tournaments/eventSchedule/" + t)
        event_elements = driver.find_elements(By.XPATH, "//tr[@id]")
        for event_element in event_elements:
            event_value = event_element.get_attribute("id")
            event_value = event_value.replace("ev_", "")
            e_list.append(event_value) 
        

def tourn_results(e_list):
    for e in e_list:
        driver.get("https://www.fencingtimelive.com/events/results/" + e)
        t_name = driver.find_element(By.CLASS_NAME, "desktop tournName")
        e_name = driver.find_element(By.CLASS_NAME, "desktop eventName")
        download_button = driver.find_element(By.ID, "butDownload")
        f_name = t_name + e_name
        download_button.click()
        os.rename("eventResults.csv", f_name + ".csv") 
        



#Main Code
tournaments = []
events = []
pool_links = []
data = []
add = True
matchdata = []
addmatch = True

advanced_search(tournaments)
get_events(tournaments, events)
tourn_results(events)

# page_search(tournaments, pool_links)
# calc(pool_links, data, matchdata)
#
# driver.quit()
#
# with open("./fencingdata.json", "r") as f:
#     jsondata = json.load(f)
#
#
# for i in data:
#     for j in jsondata:
#         if i["name"] == j["name"]:
#             add = False;
#             break
#         add = True;
#     if add:
#         jsondata.append(i)
#
# with open("./fencingdata.json", 'w') as f:
#     json.dump(jsondata, f, indent=4)
#
#
# with open("./fencingmatches.json", "r") as z:
#     jsondatam = json.load(z)
#
#
# for i in matchdata:
#     jsondatam.append(i)
#
# with open("./fencingmatches.json", "w") as z:
#     json.dump(jsondatam, z, indent=4)
