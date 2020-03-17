from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome(executable_path = "C:/Users/noaim/Downloads/chromedriver_win32 (1)/chromedriver.exe")  # initiating a web browser session
driver.get("https://www.instagram.com")
driver.maximize_window()

wait = WebDriverWait(driver,5) ## wait of 5 seconds 

# 1. logging into instagram

def login(usname,passwd):
    
    log_in_btn = wait.until(EC.presence_of_element_located((By.XPATH,"//p[@class = 'izU2O']/a")))
    log_in_btn.click()
    time.sleep(2)
    
    username = driver.find_element_by_name("username")
    password = driver.find_element_by_name("password")
    
    username.send_keys(usname)
    password.send_keys(passwd)
    
    enter = driver.find_element_by_xpath("//button[contains(@class,'sqdOP')]/div")
    enter.click()
    
    
    # handling the turn on notifications message
    
    not_now = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"HoLwm")))
    not_now.click()
login("SAMPLE USERNAME","SAMPLE PASSWORD")

# 2. getting names of instagram handles on searching

def insta_handles(name):
    
    search = driver.find_element_by_xpath("//input[contains(@class,'XTCLo')]")
    search.clear()
    search.send_keys(name)
    time.sleep(2)
    food_handles = driver.find_elements_by_xpath("//div[contains(@class,'g9vPa')]/span/img") # ignores hashtags and locations
    for i in food_handles:
        print(i.get_attribute("alt").split("'")[0])

insta_handles("food") ## eg.: finding list of insta handles related to food


# 3. Searching and opening of insta handles

def searching_opening(profile_name):
    search = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'XTCLo')]")))
    search.clear()
    search.send_keys(profile_name)
    profile = wait.until(EC.presence_of_element_located((By.XPATH,"//a[contains(@class,'yCE8d  ')]")))
    profile.click()
    return

searching_opening("food") ## eg. 

# 4. Following and unfollowing of given handle

def follow_unfollow(profile_name):
    
    searching_opening(profile_name)
    follow = wait.until(EC.presence_of_element_located((By.XPATH,"//button[contains(@class,'_5f5mN')]")))
    if follow.get_attribute("innerHTML") == "Following":
        print("Already following")
    else:
        follow.click()
        print("Followed")
    time.sleep(2)
    follow.click() # to unfollow 
    unfollow = driver.find_element_by_xpath("//button[contains(@class,'aOOlW')]") # gives the first occurence which is of unfollow button
    unfollow.click()
    print("Now unfollowed")
    driver.back()

    return

follow_unfollow("So Delhi") ## following/unfollowing of So Delhi

# 5.1 & 5.2 : liking/unliking posts of an instagram handle

def like_unlike(profile_name):
    searching_opening(profile_name)
    post = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_9AhH0")))
    post.click()
    for i in range(30):
        
        button = wait.until(EC.presence_of_element_located((By.XPATH,"//span[contains(@class,'glyphsSpriteHeart__')]")))
        if button.get_attribute("aria-label") == "Like":
            button.click()
            print("Liked post ",i+1,)
        else:
            print("Post ",i+1," is already liked")
        
        next_button = driver.find_element_by_link_text("Next")
        next_button.click()
    close = driver.find_element_by_class_name("ckWGn")
    close.click()    
    post = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_9AhH0")))
    post.click()
    for i in range(30):
        button = wait.until(EC.presence_of_element_located((By.XPATH,"//span[contains(@class,'glyphsSpriteHeart__')]")))
        if button.get_attribute("aria-label") == "Unlike":
            button.click()
            print("Unliked the post ",i+1)
        else:
            print("Post ",i+1," is already unliked")
            
        next_button = driver.find_element_by_link_text("Next")
        next_button.click()            
    close = driver.find_element_by_xpath("//button[@class='ckWGn']")
    close.click()
    back = wait.until(EC.presence_of_element_located((By.XPATH,"//img[contains(@class,'s4Iyt')]")))
    back.click()


like_unlike("dilsefoodie") # liking and unliking the first 30 posts of dilsefoodie

# 6 : Extract list of followers
# 6.1 : extracting user names of first 500 followers of given instagram handles

from selenium.webdriver.common.keys import Keys

def correct(number_of_followers):
        
    a = number_of_followers.split(',')
    ans = '0'
    for i in a:
        ans += i
    else:
        return int(ans)
    
def usernames(profile_name):
    
    searching_opening(profile_name)
    followers = wait.until(EC.presence_of_element_located((By.XPATH,"//a[@class='-nal3 ']")))
    followers.click()
    cnt = 1
    total_followers = correct((driver.find_elements_by_xpath("//span[@class='g47SY ']")[1].get_attribute("title")))
    usnames = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@class,'notranslate')]")))
    index = 0
    if total_followers<500:
        limit = total_followers
    else:
        limit = 500
    l = [] # list for containig usernames of the followers
    loaded_till_now = len(usnames)
    while cnt<=limit:
        for i in range(index,len(usnames)):
            #print(usnames[i].get_attribute("innerHTML"))
            l.append(usnames[i].get_attribute("innerHTML")) # appending the usernames of followers into the list l
            cnt = cnt + 1
            if cnt >= limit:
                break
        #if len(usnames) == total_followers:
         #   break
        usnames[loaded_till_now-1].location_once_scrolled_into_view
        driver.execute_script("arguments[0].focus();", usnames[loaded_till_now-1])
        driver.find_element_by_tag_name('body').send_keys(Keys.END) #triggers AJAX request to load more users. observed that loading 10 users at a time.        
        prev_names = usnames
        usnames = driver.find_elements_by_xpath("//a[contains(@class,'FPmhX notranslate _0imsa ')]")
        index = len(usnames) - len(prev_names) -1
       
    close = driver.find_element_by_xpath("//button[@class='wpO6b ']") # closing the list of followers
    close.click() 
    insta = driver.find_element_by_xpath("//img[@class='s4Iyt']")
    insta.click() # going back to the main insta page
    return l


# 6.1 (contd) printing the usernames of first 500 followers of foodtalkindia and So Delhi

print("First 500 followers of foodtalkindia\n")
l = usernames("foodtalkindia")
for i in l:
    print(i)
print("\n-------------------------------------------------\n")
print("First 500 followers of So Delhi\n")
l = usernames("So Delhi")
for i in l:
    print(i)

my_followers = usernames("SAMPLE USERNAME") # finding my own list of followers

len(my_followers)

# 6.2 finding list of followers on Insta handle I am following but they don't follow me

def func(profile_name,my_followers):
    searching_opening(profile_name)
    try:
        ff = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"tc8A9")))
        ff.click()
        see_all = wait.until(EC.presence_of_element_located((By.LINK_TEXT,"See All Followers")))
        see_all.click()
        a = driver.find_elements_by_xpath("//button[contains(@class,'sqdOP  L3NKy    _8A5w5    ')]")
        usnames = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@class,'FPmhX notranslate _0imsa ')]")))
        n = len(a)
        for i in range(n):
            name = usnames[i].get_attribute("innerHTML")
            if name not in my_followers:
                print(name)
    except:
        print("None of the people I follow follow this page")

func("foodtalkindia",my_followers)

# 7. Checking the story of coding.ninjas

wait = WebDriverWait(driver,17) # maximum limit set to 17sec as the maximum duration of an insta story is 17 sec (if video) and 7 sec (if photo)
import time
def check_story(profile_name):
    
    searching_opening(profile_name)
    cl = driver.find_element_by_xpath("//img[@class='_6q-tv']") 
    thing = driver.find_element_by_xpath("//canvas[contains(@class,'CfWVH')]")
    top = int(thing.get_attribute("style").split(";")[1][-3])
    width = thing.get_attribute("style").split(";")[3][8:11]
    if width == '150':
        print("No story")
    elif width == '166':
        print("Story present but already seen")
    elif width == '168':
        print("Story present and not seen yet")
        cl.click()
        print("Now seen the story")
        while True:
            try:
                next = wait.until(presence_of_element_located((By.XPATH,"//div[@class='coreSpriteRightChevron']")))
                next.click()
            except:
                break # ie. clicks on next until it is present, when not present, error will come and then it will come to except part and break
    driver.back()
    
check_story("coding.ninjas")