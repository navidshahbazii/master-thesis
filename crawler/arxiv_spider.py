import selenium
from selenium import webdriver
import pandas as pd
import time
import math

# the keyword which is searched in Arxiv digital library
keyword = "computer science"
i = 1
separator = ' '
output = []
page_num = 0
driver = webdriver.Chrome(executable_path='/Users/masterthesis/Downloads/chromedriver-2') # setting up the google driver to make it automatic

# Arxiv digital library URL and the keyword which is searched for

driver.get("https://arxiv.org/search/?query=" +
           keyword+"&searchtype=abstract&abstracts=hide&order=-announced_date_first&size=50&start="+str(page_num))
print(driver.title)
# XPATH for crawling number of articles for that particular keyword
num_of_articles = driver.find_element_by_xpath('/html/body/main/div[1]/div[1]/h1').text
num_of_articles = num_of_articles.split()[3]
num_of_articles = num_of_articles.replace(',', '')
max_page_num = math.ceil(int(num_of_articles)/50)
max_page_num_temp = max_page_num
print("Total # of pages = ", max_page_num)
if max_page_num > 20:
    max_page_num = 20  # specify how many page you want to crawl. please be aware that each page contains 50 papers
print("# of pages will be crawled = ", max_page_num)
if max_page_num_temp > 20:
        print('# of articles will be crawled = 1000')
else:
        print('# of articles will be crawled = ', num_of_articles)
print("---------------------------------------------------------------------------------------------------")

########################################################## CRAWLER PART ###############################################################

for j in range(1, max_page_num + 1):
        driver.get("https://arxiv.org/search/?query=" +
           keyword+"&searchtype=abstract&abstracts=hide&order=-announced_date_first&size=50&start="+str(page_num))
        articles = driver.find_elements_by_css_selector(".is-5")
        for article in articles:
                # putting each article's link inside a varible in order to click later and crawl the abstract from there
                click = driver.find_element_by_xpath('//*[@id="main-container"]/div[2]/ol/li['+str(i)+']/div/p/a')

                # crawling the title
                title = driver.find_element_by_xpath('/html/body/main/div[2]/ol/li[' + str(i) + ']/p[1]')
                title_text = title.text
                print(title_text)

                # crawling the date of pbulish
                date = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li["+str(i)+"]/p[3]").text
                date_text = separator.join(date.split()[-2:])[:-1]
                print(date_text)

                # crawling the link of the article in arxiv digital library
                link = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li["+str(i)+"]/div/p/a").get_attribute('href')
                link_text = link
                print(link_text)

                # crawling the first author
                author_1 = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li[" + str(i) + "]/p[2]/a[1]")
                author_1_text = author_1.text
                print(author_1_text)

                try:
                        # carwling the secon author if available
                        author_2 = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li[" + str(i) + "]/p[2]/a[2]")
                        author_2_text = author_2.text
                        print(author_2_text)
                except:
                        # if there is no second author put null
                        author_2 = None
                        author_2_text = None

                click.click()  # clicking on the article's link
                time.sleep(3)  # wait 3 seconds for the page to be loaded

                # CSS tag for abstract
                abstract = driver.find_element_by_css_selector('.abstract')
                abstract_text = abstract.text
                print(abstract_text)

                # putting everthing in a dictionary
                temp = {'Title': title_text,
                        'date': date_text,
                        'author_1': author_1_text,
                        'author_2': author_2_text,
                        'link': link_text,
                        'abstract': abstract_text}
                output.append(temp)  # append each record to another

                driver.back()  # go back in the browser
                time.sleep(3)  # wait 3 seconds for the page to load
                if page_num == 0:
                        print("Page number = ", page_num+1)
                else:
                        print("Page number = ", int((page_num/50)+1))
                print("Total number of articles in this page: ", len(articles))
                print("Scraping article # ", i)
                print("---------------------------------------------------------------------------------------------------")
                if i <= len(articles):
                        i = i + 1  # go to the next article
                else:
                        break
        i = 1
        page_num = page_num + 50  # go to the next page
# putting the results into excel
output = pd.DataFrame(output)
output['date'] = pd.to_datetime(output['date'])
output.to_excel("output_arxiv.xlsx", index=False)
