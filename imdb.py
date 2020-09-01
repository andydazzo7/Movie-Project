from selenium import webdriver 
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
import time
import re
#peopleInolved=[]
ratings = []
#Productions = []
releaseDates  = []
#percentsfull = []
popularities = []
metascores = []
starpowers= [] 
earnings = []
def imdbScrape(movie):
    webdriver = "/Users/andydazzo/Desktop/chromedriver"
    chrome_options = Options()
    #chrome_options.add_argument("--disable-extensions")
   # chrome_options.add_argument("--disable-gpu")
    #chrome_options.add_argument("--no-sandbox) # linux only
    #chrome_options.add_argument("--headless")
    driver2 = Chrome(webdriver, options=chrome_options)
    movie = movie.replace("(2019)", " " )
    movie = movie.replace("(2020)", " " )
    movie = movie.replace(" ", '+')
    movie = movie.replace("&","and" )
    if(movie == 'BIRDS+OF+PREY+(AND+THE+FANTABULOUS+EMANCIPATION+OF+ONE+HARLEY+QUINN)'):
        movie = 'BIRDS+OF+PREY'
    print(movie)
    url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(movie)
    driver2.get(url)
    #time.sleep(10)
    #wait = WebDriverWait(driver2, 10)
    #element = wait.until(EC.visibility_of_eleme
    # nt_located((By.CLASS_NAME, 'result_text')))
    try:
        a = driver2.find_element_by_class_name('result_text')
        link = a.find_element_by_tag_name('a')
        main_window = driver2.current_window_handle
        ActionChains(driver2) \
        .key_down(Keys.COMMAND) \
        .click(link) \
        .key_up(Keys.COMMAND) \
        .perform()
        driver2.switch_to.window(driver2.window_handles[1])
        #time.sleep(10)
        driver2.execute_script("window.scrollTo(0, 1000)")
        rating = driver2.find_element_by_class_name('ratingValue')
        imdbRating = rating.find_element_by_tag_name('span')
        ratings.append(imdbRating.text)
        print('Rating: ' + imdbRating.text)
        summary = driver2.find_elements_by_class_name('credit_summary_item')
        peopleInolve = " "
        for s in summary:
            category = s.find_element_by_tag_name('h4')
            peopleInolve += category.text + ": " 
            print(category.text)
            items = s.find_elements_by_tag_name('a')
            for i in items: 
                peopleInolve += i.text + ", "
                print(i.text)
        #peopleInolved.append(peopleInolve)
        bigDets = driver2.find_element_by_id('titleDetails')
        details = bigDets.find_elements_by_class_name('txt-block')
        prodsBig = " "
        for d in details:
            try:
                budgetcount = 0
                h4 = d.find_element_by_tag_name('h4')
                if(h4.text == 'Gross USA:'):
                    budget = -1
                    budget = d.text
                    if(budget == -1 ):
                        budget = None
                    #for s in showtimes:
                    earnings.append(budget)
                    print( 'budget: ' + budget)
                elif(h4.text == 'Release Date:'):
                    release = d.text
                    #for s in showtimes:
                    releaseDates.append(release)
                    print('release: ' + release)
               # elif(h4.text == 'Production Co:'):
                #    prods = d.find_elements_by_tag_name('a')
                 #   for p in prods:
                  #      prodsBig = ProdsBig + p.text + ", "
                   #     print('Prod: ' + p.text)
                    #for s in showtimes:

                     #   Productions.append(prodsBig)
            
            except:
                pass
        if( len(earnings) < len(releaseDates)):
            earnings.append(0)
        # earnings.append(0)
        barItems = driver2.find_elements_by_class_name('titleReviewBarItem')
        for b in barItems: 
            print b.text
            bsmall = b.text
            if(len(re.findall('Metascore', bsmall)) > 0):
                metascore = -1
                metascore = re.sub('[^0-9]','', bsmall)
                print('meta ' + metascore)
                #for s in showtimes: 
                metascores.append(metascore)
            elif(len(re.findall('Popularity', bsmall)) > 0):
                if ('(') in bsmall:
                    Result = bsmall[:bsmall.find('(') + 1]
                    popRating = re.sub('[^0-9]','', Result)
                else:
                    popRating = re.sub('[^0-9]','', bsmall)
                print('pop:' + popRating)
                #for s in showtimes: 
                popularities.append(popRating)
        if(len(metascores) < len(popularities)):
            metascores.append(0)
        CastList = driver2.find_element_by_class_name('cast_list')
        people = CastList.find_elements_by_class_name('primary_photo')
        StarPower = 0
        for i in range(4):
            link = people[i]
            link1 = link.find_element_by_tag_name('a').get_attribute('href')
            webdriver = "/Users/andydazzo/Desktop/chromedriver"
            driver5 = Chrome(webdriver,options=chrome_options)
            driver5.get(link1)
            try:
                meter = driver5.find_element_by_id('meterHeaderBox')
                rating = meter.find_element_by_tag_name('a').text
            
                if(rating == 'SEE RANK'):
                    rating = 10000
                elif(rating == 'Top 5000'):
                    rating = 5000
                elif(rating == 'Top 500'):
                    rating = 500
                print(rating)
                StarPower+= (int)(rating)
            except:
                StarPower += 20000
            driver5.close()
            #driver2.close()
        #for s in showtimes:
        starpowers.append(StarPower)
        driver2.switch_to_window(main_window)
    except:
        starpowers.append(None)
        popularities.append(None)
        earnings.append(None)
        releaseDates.append(None)
        metascores.append(None)
        ratings.append(None)
        peopleInolved.append(None)
        print("No IMDB DATA FOUND")
    driver2.quit()

if __name__ == "__main__":
    print("started")
    #put movies you want to add
    movies = ['Hope Gap', 'Onward', 'Impractical Jokers the movie', 'The Lodge', 'The Assistant'
    ,'Gretel and Hansel', 'Bloodshot', 'I Still Believe', 'Portrait of A Lady on Fire']
    for m in movies:
        imdbScrape(m)
    data = {
        'Title':movies,
        'IMDB rating': ratings,
        'Earnings': earnings,
        'Release Date': releaseDates,
        'Star Power' : starpowers,
        'Popularity': popularities,
        'MetaCritic Score': metascores
    }
    try:
        df = pd.DataFrame(data)
        print df 
        filename = "IMDBMASTERMARCH.csv"
        #appends to exisitng master file
        df.to_csv(filename, mode = 'a', encoding = 'utf-8')
       
        #automatically upload to google drive, use driveUploader.py
   


    except:
        print("csv failed")

