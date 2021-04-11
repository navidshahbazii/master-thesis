import selenium
from selenium import webdriver
import pandas as pd
import time
import math

keyword = "computer science"
i = 1
output = []
page_num = 0
driver = webdriver.Chrome(executable_path='/Users/masterthesis/Downloads/chromedriver')
driver.get(
        "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=Keyword&text1=" +
        keyword + "&field2=Abstract&text2=" + keyword + "&startPage="
        + str(page_num) + "&pageSize=50")
print(driver.title)
num_of_articles = driver.find_element_by_class_name("hitsLength").text
num_of_articles = num_of_articles.replace(',', '')
max_page_num = math.ceil(int(num_of_articles)/50)
max_page_num_temp = max_page_num
print("Total # of pages = ", max_page_num)
if max_page_num > 20:
    max_page_num = 20
print("# of pages will be crawled = ", max_page_num)
if max_page_num_temp > 20:
        print('# of articles will be crawled = 1000')
else:
        print('# of articles will be crawled = ', num_of_articles)
print("---------------------------------------------------------------------------------------------------")

for j in range(1, max_page_num + 1):
        driver.get(
                "https://dl.acm.org/action/doSearch?fillQuickSearch=false&expand=dl&field1=Keyword&text1=" +
                keyword + "&field2=Abstract&text2=" + keyword + "&startPage="
                + str(page_num) + "&pageSize=50")
        articles = driver.find_elements_by_class_name("issue-item__content-right")
        for article in articles:
                try:
                        title = driver.find_element_by_xpath('//*[@id="pb-page-content"]/div/main/div[1]/div/div[2]/div/ul/li['
                                                             + str(i) + ']/div/div[2]/div/h5/span/a')
                        title_text = title.text
                        print(title_text)

                        title.click()
                        time.sleep(3)
                except:
                        title = None



                abstract = driver.find_element_by_css_selector('.abstractInFull p')
                abstract_text = abstract.text
                print(abstract_text)

                downloads = driver.find_element_by_xpath(
                        '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[5]/div/div[1]/div/ul/li[2]/span/span')
                downloads_text = downloads.text
                print(downloads_text)

                citations = driver.find_element_by_xpath(
                        '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[5]/div/div[1]/div/ul/li[1]/span/span[1]')
                citations_text = citations.text
                print(citations_text)

                date = driver.find_element_by_xpath(
                        '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[4]/div/span[2]/span')
                date_text = date.text
                print(date_text)

                type = driver.find_element_by_xpath(
                        "/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[1]/span[1]")
                type_text = type.text
                print(type_text)

                try:

                        author_1 = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[3]/div/ul/li[2]/a/span/div/span/span")
                        author_1_text = author_1.text
                        print(author_1_text)
                except:
                        author_1 = None

                try:

                        author_2 = driver.find_element_by_xpath("/html/body/div[1]/div/main/div[2]/article/div[1]/div[2]/div/div[3]/div/ul/li[3]/a/span/div/span/span")
                        author_2_text = author_2.text
                        print(author_2_text)
                except:
                        author_2 = None
                        author_2_text = None

                try:
                        link = driver.find_element_by_xpath(
                                '//*[@id="pb-page-content"]/div/main/div[2]/article/div[1]/div[2]/div/div[4]/div/span/a')
                        link_text = link.text
                        print(link_text)
                except:
                        link = None

                temp = {'Title': title_text,
                        'type': type_text,
                        'total_downloads': downloads_text,
                        'total_citations': citations_text,
                        'date': date_text,
                        'author_1': author_1_text,
                        'author_2': author_2_text,
                        'link': link_text,
                        'abstract': abstract_text}
                output.append(temp)

                driver.back()
                time.sleep(3)
                print("Page number = ", page_num+1)
                print("Total number of articles in this page: ", len(articles))
                print("Scraping article # ", i)
                print("---------------------------------------------------------------------------------------------------")
                if i <= len(articles):
                        i = i + 1
                else:
                        break
        i = 1
        page_num = page_num + 1

output = pd.DataFrame(output)
output['date'] = output.date.str.replace(',', '')
output['date'] = pd.to_datetime(output['date'])
output['total_citations'] = output.total_citations.str.replace(',', '')
output['total_citations'] = output['total_citations'].astype('int')
output['total_downloads'] = output.total_downloads.str.replace(',', '')
output['total_downloads'] = output['total_downloads'].astype('int')
output.to_excel("output.xlsx", index=False)
