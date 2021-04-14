import selenium
from selenium import webdriver
import pandas as pd
import time
import math

keyword = "computer science"  # the keyword which is searched in ACM digital library
i = 1
output = []
page_num = 0
driver = webdriver.Chrome(executable_path='/Users/masterthesis/Downloads/chromedriver-2')  # setting up the google driver to make it automatic

# ACM digital library URL and the keyword which is searched for
driver.get(
"https://dl.acm.org/action/doSearch?fillQuickSearch=false&ContentItemType=research-article&expand=dl&AllField=Keyword%3A%28"
+ keyword + "%29+AND+Abstract%3A%28" + keyword + "%29&pageSize=50&startPage=" + str(page_num) + "&AvailableFormat=lit%3Apdf")
print(driver.title)

# finding out how many pages in total we can crawl
num_of_articles = driver.find_element_by_class_name("hitsLength").text
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



######################################################### CRAWLER PART ###############################################################

for j in range(1, max_page_num + 1):
        driver.get(
                "https://dl.acm.org/action/doSearch?fillQuickSearch=false&ContentItemType=research-article&expand=dl&AllField=Keyword%3A%28"
                + keyword + "%29+AND+Abstract%3A%28" + keyword + "%29&pageSize=50&startPage=" + str(page_num) + "&AvailableFormat=lit%3Apdf")

        articles = driver.find_elements_by_class_name("issue-item__content-right")
        for article in articles:

                # crawling the title of each article in each page
                try:
                        # XPATH of the titles in each page
                        title = driver.find_element_by_xpath('//*[@id="pb-page-content"]/div/main/div[1]/div/div[2]/div/ul/li['
                                                             + str(i) + ']/div/div[2]/div/h5/span/a')
                        title_text = title.text
                        print(title_text)

                        title.click()  # click on the title and open each article in ACM digital library
                        time.sleep(3)  # wait 3 seconds for the page to get opened
                except:
                        title = None   # if there is no title do nothing!



                abstract = driver.find_element_by_css_selector('.abstractInFull p') # CSS tag of the abstract
                abstract_text = abstract.text
                print(abstract_text)

                try:
                        # XPATH of the downloads number
                        downloads = driver.find_element_by_xpath(
                                '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[5]/div/div[1]/div/ul/li[2]/span/span')
                        downloads_text = downloads.text
                        print(downloads_text)
                except:
                        # another XPATH of downloads number --> sometimes this one works sometimes the other one
                        downloads = driver.find_element_by_xpath(
                                '/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[6]/div/div[1]/div/ul/li[2]/span/span')
                        downloads_text = downloads.text
                        print(downloads_text)

                try:
                        # XPATH of the citations number
                        citations = driver.find_element_by_xpath(
                                '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[5]/div/div[1]/div/ul/li[1]/span/span[1]')
                        citations_text = citations.text
                        print(citations_text)
                except:
                        # if there is no citations put zero
                        citations = "0"
                        citations_text = citations

                # XPATH of the date taht article was published
                date = driver.find_element_by_xpath(
                        '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[4]/div/span[2]/span')
                date_text = date.text
                print(date_text)

                # XPATH of the type of the articles --> here, we only filtered for research article but it could be also poster, journal, etc.
                type = driver.find_element_by_xpath(
                        "/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[1]/span[1]")
                type_text = type.text
                print(type_text)

                try:
                        # XPATH of the first author
                        author_1 = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[3]/div/ul/li[2]/a/span/div/span/span")
                        author_1_text = author_1.text
                        print(author_1_text)
                except:
                        # if there is no author put null
                        author_1 = None

                try:
                        # XPATH of the second author if available
                        author_2 = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[3]/div/ul/li[3]/a/span/div/span/span")
                        author_2_text = author_2.text
                        print(author_2_text)
                except:
                        # if there is no second author put null
                        author_2 = None
                        author_2_text = None

                try:
                        # XPATH of the link of the article in ACM digital Library
                        link = driver.find_element_by_xpath(
                                '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[4]/div/span/a')
                        link_text = link.text
                        print(link_text)
                except:
                        # if there is no link out null
                        link = None

                # making a dictionary out of the crawled data
                temp = {'Title': title_text,
                        'type': type_text,
                        'total_downloads': downloads_text,
                        'total_citations': citations_text,
                        'date': date_text,
                        'author_1': author_1_text,
                        'author_2': author_2_text,
                        'link': link_text,
                        'abstract': abstract_text}
                output.append(temp)  # append informations crawled for each articles together

                driver.back()  # go back to the main page in ACM digital library
                time.sleep(3)  # wait 3 seconds for the page to be loaded
                print("Page number = ", page_num+1)
                print("Total number of articles in this page: ", len(articles))
                print("Scraping article # ", i)
                print("---------------------------------------------------------------------------------------------------")
                if i <= len(articles):
                        i = i + 1  # going to the next article
                else:
                        break
        i = 1
        page_num = page_num + 1  # going to the next page in ACM digital library

# putting everything together and make a table and export it as excel
output = pd.DataFrame(output)
output['date'] = output.date.str.replace(',', '')
output['date'] = pd.to_datetime(output['date'])
output['total_citations'] = output.total_citations.str.replace(',', '')
output['total_citations'] = output['total_citations'].astype('int')
output['total_downloads'] = output.total_downloads.str.replace(',', '')
output['total_downloads'] = output['total_downloads'].astype('int')
output.to_excel("ACM_output.xlsx", index=False)
