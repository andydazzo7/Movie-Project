from selenium.webdriver import Chrome
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import time
from selenium.webdriver.common.by import By

earnings = []
peopleInolved=[]
ratings = []
Productions = []
releaseDates  = []
def imdbScrape(movie, showtimes):
    webdriver = "/Users/andydazzo/Desktop/chromedriver"
    driver2 = Chrome(webdriver)
    movie = movie.replace("(2019)", " " )
    movie = movie.replace(" ", '+')
    print(movie)
    url = "https://www.imdb.com/find?q={}&ref_=nv_sr_sm".format(movie)
    driver2.get(url)
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
    driver2.close()
    driver2.switch_to_window(main_window)
    driver2.quit()

    

#add path for local machine
webdriver = "/Users/andydazzo/Desktop/chromedriver"
#print("hi")
driver = Chrome(webdriver)
url = "https://www.fandango.com/amc-mountainside-10-aaaug/theater-page?mode=general&q=07090&date=2019-12-27"
driver.get(url)
movies = driver.find_elements_by_class_name('fd-movie')
times = []
titles = []
prices = []
RRGs= []
amenitiesBig = []
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
            #select = Select(driver3.find_element_by_class_name('qtyDropDown'))
            #select.select_by_visible_text('1')
            #button = driver3.find_element_by_id('NewCustomerCheckoutButton')
            ##button.click()
            #seats = driver3.find_element_by_id('frmSeatPicker')
            #print(seats.text)
            #x = seats.find_element_by_id('seatPickerContainer')
            #print(x)
            #try:
                #element = WebDriverWait(driver3, 10).until( EC.visibility_of_element_located(By.ID, 'A3'))
            #finally:
             #   driver3.quit()
            
            #openSeats = seats.find_element_by_class_name('standard availableSeat')      
            #openCount = 0
            #for x in openSeats:
             #   openCount+=1
            #closedSeats = driver3.find_elements_by_class_name('standard reservedSeat')
            #closedCount = 0
            #for x in closedSeats:
             #   closedSeats+=1
            driver3.close()
            #print("percent full " + str(openCount/closedCount))
           
            
            
        except:
            #driver3.close()
            times.append(None)
            amenitiesBig.append(None)
            prices.append(None)

            pass
        #driver.back()
data = {
    'title' : titles,
    'Rating Runtime Genre': RRGs,
    'time': times,
    'amenities' : amenitiesBig,
    'price' :prices,
    'earnings': earnings,
    'peopleInolved':  peopleInolved,
    'IMDB rating': ratings,
    'Release Date': releaseDates
}
df = pd.DataFrame(data)
print df 
df.to_csv("MovieProjectTest1.csv", sep='\t', encoding = 'utf-8')


    
        
   
   

