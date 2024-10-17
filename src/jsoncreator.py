import json
from selenium import webdriver
from selenium.webdriver.common.by import By

#Driver options
options = webdriver.FirefoxOptions()
#options.add_argument("--headless=new")
driver = webdriver.Firefox(options=options)

#Searching each page and adding pool ids to csv
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

           

def advanced_search(tournaments): 
    #Getting Page
    driver.get("https://fencingtimelive.com/tournaments/search/advanced")

    #Running advanced search: Name = ghsfl, Date From = 09/01/2021 
    tourn_name = driver.find_element(By.ID, "searchTournName")
    search_button = driver.find_element(By.ID, "searchBut")
    date_selector = driver.find_element(By.ID, "searchDateFrom")
    date_selector_year = driver.find_element(By.CLASS_NAME, "picker__select--year")
    date_selector_year_2021 = driver.find_element(By.XPATH, "//option[@value='2021']")
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


    #Grabbing ids for each tournament and saving into list
    #tournament_list = driver.find_elements(By.XPATH, "//tr[@data-uniqueid]")
    tournament_list = driver.find_elements(By.CSS_SELECTOR, "[data-uniqueid]")


    for tournament in tournament_list:
        id = tournament.get_attribute("data-uniqueid")
        tournaments.append(id)

    tournaments.remove("21CEC915D69E44AD83EC2EE07B8658D7")
    tournaments.remove("811A37B6B92D4F888BE89AB44ED55EAA")
    tournaments.remove("EF37C1B278B54EDEAAF95945078A297A")
    tournaments.remove("AA23F529886A4F5E87D30F3C953C8B64")
    tournaments.remove("F26265754D814DE2BC3A495DB8E5F441")
    tournaments.remove("DD826DDF04954E6C8277023CB3F272C8")
    tournaments.remove("222068A192194E658E14FBEA29913EF1")
    tournaments.remove("D08B3F155FF64386B07F6F6F4EA8CE02")
    tournaments.remove("608294FD43BE44BDA6A7EFB815C50DFA")
    tournaments.remove("273F355ED62E4D8BAF4F5E35459FA8F6")
    tournaments.remove("0DE3EA33DCF846FEBD67D26D9B02ECBF")
    tournaments.remove("7D5C6A04D81B41AFB03AF08E451194FF")
    tournaments.remove("B8E4E3309DF143EF8F585835F1F1444C")
    tournaments.remove("E40D29AB56014B87BF0A9C9F49B25B26")
    tournaments.remove("A4B90FCD9BA5434396C5BE4D9E15118E")
    tournaments.remove("B2B647667E61440C990D3733E938C152")
    tournaments.remove("F31345B625AC4139A18C000A2FBCA8E9")
    tournaments.remove("6B3BC0D004094AEF90C461F8A296A0C0")


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
                "rating": 1000,
                "wins": 0,
                "losses": 0,
                "points earned": 0,
                "points lossed": 0
            }
            fen2 = {
                "name": fencer_2,
                "rating": 1000,
                "wins": 0,
                "losses": 0,
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
            

            #print(fencer_1, fencer_1_score, fencer_2_score, fencer_2, fencer_1_win, fencer_2_win)
 



list1 = []
list2 = []
data = []
add = True

matchdata = []
addmatch = True

advanced_search(list1)
page_search(list1, list2)
calc(list2, data, matchdata)

driver.quit()



with open("./fencingdata.json", "r") as f:
    jsondata = json.load(f)


for i in data:
    for j in jsondata:
        if i["name"] == j["name"]:
            add = False;
            break
        add = True;
    if add:
        jsondata.append(i)

with open("./fencingdata.json", 'w') as f:
    json.dump(jsondata, f, indent=4)


with open("./fencingmatches.json", "r") as z:
    jsondatam = json.load(z)


for i in matchdata:
    jsondatam.append(i)

with open("./fencingmatches.json", "w") as z:
    json.dump(jsondatam, z, indent=4)
