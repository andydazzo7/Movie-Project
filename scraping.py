from __future__ import division
from selenium.webdriver import Chrome
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By
import re
from datetime import date
earnings = []
peopleInolved=[]
ratings = []
Productions = []
releaseDates  = []
percentsfull = []
popularities = []
metascores = []
starpowers= [] 
datesTaken = []
moneyMissed = []
def imdbScrape(movie, showtimes):
    webdriver = "/Users/andydazzo/Desktop/chromedriver"
    driver2 = Chrome(webdriver)
    movie = movie.replace("(2019)", " " )
    movie = movie.replace(" ", '+')
    movie.replace(' & ',' and ' )
    print(movie)
    url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(movie)
    driver2.get(url)
    time.sleep(10)
    #wait = WebDriverWait(driver2, 10)
    #element = wait.until(EC.visibility_of_eleme
    # nt_located((By.CLASS_NAME, 'result_text')))
    a = driver2.find_element_by_class_name('result_text')
    link = a.find_element_by_tag_name('a')
    main_window = driver2.current_window_handle
    ActionChains(driver2) \
    .key_down(Keys.COMMAND) \
    .click(link) \
    .key_up(Keys.COMMAND) \
    .perform()
    driver2.switch_to.window(driver2.window_handles[1])
    rating = driver2.find_element_by_class_name('ratingValue')
    imdbRating = rating.find_element_by_tag_name('span')
    for s in showtimes:
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
    for s in showtimes:
        peopleInolved.append(peopleInolve)
    bigDets = driver2.find_element_by_id('titleDetails')
    details = bigDets.find_elements_by_class_name('txt-block')
    prodsBig = " "
    for d in details:
        try:
            budgetcount = 0
            h4 = d.find_element_by_tag_name('h4')
            if(h4.text == 'Gross USA:'):
                budget = d.text
                for s in showtimes:
                    earnings.append(budget)
                print( 'budget: ' + budget)
            elif(h4.text == 'Release Date:'):
                release = d.text
                for s in showtimes:
                    releaseDates.append(release)
                print('release: ' + release)
            elif(h4.text == 'Production Co:'):
                prods = d.find_elements_by_tag_name('a')
                for p in prods:
                    prodsBig = ProdsBig + p.text + ", "
                    print('Prod: ' + p.text)
                for s in showtimes:

                    Productions.append(prodsBig)
           
        except:
            pass
    if( len(earnings) < len(releaseDates)):
        for s in showtimes:
            earnings.append(0)
    barItems = driver2.find_elements_by_class_name('titleReviewBarItem')
    for b in barItems: 
        print b.text
        bsmall = b.text
        if(len(re.findall('Metascore', bsmall)) > 0):
            metascore = re.sub('[^0-9]','', bsmall)
            print('meta ' + metascore)
            for s in showtimes: 
                metascores.append(metascore)
        elif(len(re.findall('Popularity', bsmall)) > 0):
            if ('(') in bsmall:
                Result = bsmall[:bsmall.find('(') + 1]
                popRating = re.sub('[^0-9]','', Result)
            else:
                popRating = re.sub('[^0-9]','', bsmall)
            print('pop:' + popRating)
            for s in showtimes: 
                popularities.append(popRating)
    CastList = driver2.find_element_by_class_name('cast_list')
    people = CastList.find_elements_by_class_name('primary_photo')
    StarPower = 0
    for i in range(5):
        link = people[i]
        link1 = link.find_element_by_tag_name('a').get_attribute('href')
        webdriver = "/Users/andydazzo/Desktop/chromedriver"
        driver5 = Chrome(webdriver)
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
    for s in showtimes:
        starpowers.append(StarPower)
    driver2.switch_to_window(main_window)
    driver2.quit()

    

#add path for local machine
webdriver = "/Users/andydazzo/Desktop/chromedriver"
driver = Chrome(webdriver)
url = "https://www.fandango.com/amc-lincoln-square-13-aabqi/theater-page"
driver.get(url)
movies = driver.find_elements_by_class_name('fd-movie')
times = []
titles = []
prices = []
RRGs= []
amenitiesBig = []
timesTaken = []
for i in range(8):
    title = movies[i].find_element_by_class_name("dark")
    print(title.text)
    RatingRuntimeGenre = movies[i].find_element_by_class_name("fd-movie__rating-runtime")
    print(RatingRuntimeGenre.text)
    showtimes = movies[i].find_elements_by_class_name("fd-movie__btn-list-item")
    imdbScrape(title.text, showtimes)
    count = 0
    for s in showtimes:
        count = count + 1
        try:
            t = time.localtime()
            current_time = time.strftime("%H:%M:%S", t)
            d = date.today()
            datesTaken.append(d)
            print(current_time)
            timesTaken.append(current_time)
            titles.append(title.text + str(count))
            RRGs.append(RatingRuntimeGenre.text)
            showtime = s.find_element_by_tag_name('a')
            print(showtime.text)
            times.append(showtime.text)
            url = showtime.get_attribute('href')
            driver3 = Chrome(webdriver)
            driver3.get(url)
            amenities = driver3.find_elements_by_class_name('amenityPopup')
            amenities1 = " "
            for a in amenities:
                amenities1 += a.text + ", "
                print(a.text)
            amenitiesBig.append(amenities1)
            price = driver3.find_element_by_class_name('pricePerTicket')
            print(price.text)
            prices.append(price.text)
            select = Select(driver3.find_element_by_class_name('qtyDropDown'))
            select.select_by_visible_text('1')
            button = driver3.find_element_by_id('NewCustomerCheckoutButton')
            button.click()
            try:
                seats = driver3.find_element_by_id('frmSeatPicker')
                #print(seats.get_attribute('innerHTML'))
                x = seats.find_element_by_id('svg-Layer_1')
                #driver.execute_script('arguments[0].click();', x)
                y = x.get_attribute('innerHTML')
                openSeats= []
                openSeats = re.findall('availableSeat', y)
                closedSeats = re.findall('reservedSeat' , y)
                totalSeats = len(openSeats) + len(closedSeats)
                if(totalSeats == 0):
                    percentsfull.append(0.0)
                    moneyMissed.append(0.0)
                else:
                    percentsfull.append(len(closedSeats) / totalSeats)
                    moneyMissed.append(prices[len(prices) -1 ] * openSeats)
                    print('money missed ' + prices[len(prices) -1 ] * openSeats)
            except:
                percentsfull.append(0.0)
            #print(len(closedSeats) / totalSeats)


            driver3.close()
           
            
            
        except:
           # driver3.close()
            times.append(None)
            amenitiesBig.append(None)
            prices.append(None)
            percentsfull.append(None)
            moneyMissed.append(None)
            pass
        #driver.back()
data = {
    'title' : titles,
    'Rating Runtime Genre': RRGs,
    'time': times,
    'amenities' : amenitiesBig,
    'price' :prices,
    'peopleInolved':  peopleInolved,
    'IMDB rating': ratings,
    'Earnings': earnings,
    'Release Date': releaseDates,
    'percent full': percentsfull,
    'Star Power' : starpowers,
    'Popularity': popularities,
    'MetaCritic Score': metascores,
    'Time Taken': timesTaken
}
df = pd.DataFrame(data)
print df 
df.to_csv("MovieProjectTest10-ChicagoFull.csv", encoding = 'utf-8')


    
        
   
   

