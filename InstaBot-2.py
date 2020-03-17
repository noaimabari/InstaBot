from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import numpy as np
import time

driver = webdriver.Chrome(executable_path = "C:/Users/noaim/Downloads/chromedriver_win32 (1)/chromedriver.exe")  # initiating a web browser session
driver.get("https://www.instagram.com")

wait = WebDriverWait(driver,5)

# logging into instagram again

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

# 1.1: Finding the top 5 instagram food handles having highest number of followers

def correct(number_of_followers):
        
    a = number_of_followers.split(',')
    ans = '0'
    for i in a:
        ans += i
    else:
        return int(ans)

def searching_opening(profile_name):
    search = wait.until(EC.presence_of_element_located((By.XPATH,"//input[contains(@class,'XTCLo')]")))
    search.clear()
    search.send_keys(profile_name)
    profile = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//a[contains(@class,'yCE8d  ')]/div/div[2]/div/span")))
    for i in profile:
        if i.get_attribute("innerHTML") == profile_name:
            i.click()
            break
    return

def insta_handles(name):
    names = []
    followers = []
    search = driver.find_element_by_xpath("//input[contains(@class,'XTCLo')]")
    search.clear()
    search.send_keys(name)
    time.sleep(2)
    food_handles = driver.find_elements_by_xpath("//div[contains(@class,'g9vPa')]/span/img")
    for i in range(10):
        names.append(food_handles[i].get_attribute("alt").split("'")[0])
    for i in names:
        searching_opening(i)
        number_of_followers = wait.until(EC.presence_of_all_elements_located((By.XPATH,"//span[contains(@class,'g47SY ')]")))[1]
        n_o_f = correct(number_of_followers.get_attribute("title"))
        followers.append(n_o_f)
        driver.back()
    #for i in range(10):
     #   print(names[i],followers[i])
    names = np.array(names)
    followers = np.array(followers)
    index = np.argsort(followers)
    names = names[index]
    followers = followers[index]
    print("Top 5 food instagram handles with maximum number of followers:")
    for i in range(-1,-6,-1):
        print(names[i],followers[i])
    return names[-1:-6:-1],followers[-1:-6:-1]
names, followers = insta_handles("food")

# 1.2 : finding the number of posts in the last 3 days of the 5 handles

def number_of_posts(names, followers):
    
    d = {}
    
    for i in names:
        searching_opening(i)
        number_of_posts = 0 
        post = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_9AhH0")))
        post.click()
        time.sleep(1)
        time2 = driver.find_element_by_xpath("//time[contains(@class,'_1o9PC')]")
        date = time2.text.split()
        while True:
            if  date[1] == "DAYS" and int(date[0]) > 3 :
                break
            elif date[1] not in ["MINUTES","HOURS","DAY","DAYS","HOUR"]:
                break
            else:
                number_of_posts += 1
                next_button = driver.find_element_by_link_text("Next")
                next_button.click()
                time2 = wait.until(EC.presence_of_element_located((By.XPATH,"//time[contains(@class,'_1o9PC')]")))
                date = time2.text.split()
                
        
        d[i] = number_of_posts
        close = driver.find_element_by_class_name("ckWGn")
        close.click()  
                
    print("Number of posts in the last 3 days are: ") 
    for i in d:
        print(i,d[i])
    
    return d.values() 

num = number_of_posts(names, followers)  
number_of_posts = np.array(num)

posts = np.array(list(num))
posts = posts*10

# 1.3 plotting graph (Data Visualization):

import matplotlib.pyplot as plt


def plot(names,followers,posts):
    plt.scatter(names,followers,sizes = posts,color ="purple",alpha = 0.5 )
    plt.ylabel("Number of followers")
    plt.xlabel("\nNames of instagram handles")
    plt.title("Top 5 food instagram handles with highest number of followers\n(size of bubble representing the number of posts \nin last 3 days)\n")
    plt.show()
plot(names,followers,posts)


# 2.1 scraping the text of the first 10 posts of the 5 handles

def scrape(names):
    d = {}
    for i in names:
        d[i] = []
    for i in names:
        searching_opening(i)
        post = wait.until(EC.presence_of_element_located((By.CLASS_NAME,"_9AhH0")))
        post.click()
        for j in range(10):
            t = wait.until(EC.presence_of_element_located((By.XPATH,"//div[@class='C4VMK']/span")))
            d[i].append(t.text)
            next_button = driver.find_element_by_link_text("Next")
            next_button.click()
        
        close = driver.find_element_by_class_name("ckWGn")
        close.click() 
    return d
scraped_content = scrape(names)

# 2.2 Calculating the frequency of each word

d = {}
for i in scraped_content:
    for j in scraped_content[i]:
        words = j.split()
        for k in words:
            d[k] = d.get(k,0) + 1
d

# 2.3 saving the file in a csv format

import pandas as pd
words = np.array(list(d.keys()))
frequency = np.array(list(d.values()))
index = np.argsort(frequency)
words = words[index]
frequency = frequency[index]
df = pd.DataFrame(words)
df[1] = frequency
df.columns = ["words","frequency"]
df.to_csv("C:/Users/noaim/Downloads/new_file") # saving the words and frequency in a csv file

# 2.4 : Finding top 5 most used hashtags

hashtags = {}
for i in d:
    if i[0] == "#":
        hashtags[i] = d[i]
h = np.array(list(hashtags.keys()))
f = np.array(list(hashtags.values()))
i = np.argsort(f)
h = h[i]
f = f[i]

print("Top occuring hashtags and their frequency: ")
for i in range(-1,-6,-1):
    print(h[i],f[i])


# 2.5 Plotting the pie chart(Visualization)

plt.title("Top 5 most used food hashtags")
plt.pie(f[-1:-6:-1],labels = h[-1:-6:-1],autopct="%.2f",explode = [0.15,0.15,0.15,0.15,0.15])
plt.show()