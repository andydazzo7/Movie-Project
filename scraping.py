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
earnings = []
peopleInolved=[]
ratings = []
Productions = []
releaseDates  = []
percentsfull = []
def imdbScrape(movie, showtimes):
    webdriver = "/Users/andydazzo/Desktop/chromedriver"
    driver2 = Chrome(webdriver)
    movie = movie.replace("(2019)", " " )
    movie = movie.replace(" ", '+')
    print(movie)
    url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(movie)
    driver2.get(url)
    time.sleep(10)
    #wait = WebDriverWait(driver2, 10)
    #element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, 'result_text')))
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
    driver2.switch_to_window(main_window)
    driver2.quit()

    

#add path for local machine
webdriver = "/Users/andydazzo/Desktop/chromedriver"
driver = Chrome(webdriver)
url = "https://www.fandango.com/amc-kabuki-8-aadas/theater-page?date=2020-01-05"
driver.get(url)
movies = driver.find_elements_by_class_name('fd-movie')
times = []
titles = []
prices = []
RRGs= []
amenitiesBig = []
timesTaken = []
for m in movies:
    title = m.find_element_by_class_name("dark")
    print(title.text)
    RatingRuntimeGenre = m.find_element_by_class_name("fd-movie__rating-runtime")
    print(RatingRuntimeGenre.text)
    showtimes = m.find_elements_by_class_name("fd-movie__btn-list-item")
    imdbScrape(title.text, showtimes)
    count = 0
    for s in showtimes:
        count = count + 1
        try:
            timesTaken.append(time.strftime)
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
                else:
                    percentsfull.append(len(closedSeats) / totalSeats)
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
    'percent full': percentsfull
}
df = pd.DataFrame(data)
print df 
df.to_csv("MovieProjectTest5-SanFrancisco.csv", encoding = 'utf-8')


    
        
   
   

