import selenium
from selenium import webdriver
import pandas as pd
import time
import math

keyword = "computer science"
i = 1
separator = ' '
output = []
page_num = 0
driver = webdriver.Chrome(executable_path='/Users/masterthesis/Downloads/chromedriver')
driver.get("https://arxiv.org/search/?query=" +
           keyword+"&searchtype=abstract&abstracts=hide&order=-announced_date_first&size=50&start="+str(page_num))
print(driver.title)
num_of_articles = driver.find_element_by_xpath('/html/body/main/div[1]/div[1]/h1').text
num_of_articles = num_of_articles.split()[3]
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
#
for j in range(1, max_page_num + 1):
        driver.get("https://arxiv.org/search/?query=" +
           keyword+"&searchtype=abstract&abstracts=hide&order=-announced_date_first&size=50&start="+str(page_num))
        articles = driver.find_elements_by_css_selector(".is-5")
        for article in articles:
                click = driver.find_element_by_xpath('//*[@id="main-container"]/div[2]/ol/li['+str(i)+']/div/p/a')

                title = driver.find_element_by_xpath('/html/body/main/div[2]/ol/li[' + str(i) + ']/p[1]')
                title_text = title.text
                print(title_text)

                date = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li["+str(i)+"]/p[3]").text
                date_text = separator.join(date.split()[-2:])[:-1]
                print(date_text)

                link = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li["+str(i)+"]/div/p/a").get_attribute('href')
                link_text = link
                print(link_text)

                author_1 = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li[" + str(i) + "]/p[2]/a[1]")
                author_1_text = author_1.text
                print(author_1_text)

                try:
                        author_2 = driver.find_element_by_xpath("/html/body/main/div[2]/ol/li[" + str(i) + "]/p[2]/a[2]")
                        author_2_text = author_2.text
                        print(author_2_text)
                except:
                        author_2 = None
                        author_2_text = None

                click.click()
                time.sleep(10)

                abstract = driver.find_element_by_css_selector('.abstract')
                abstract_text = abstract.text
                print(abstract_text)

                temp = {'Title': title_text,
                        'date': date_text,
                        'author_1': author_1_text,
                        'author_2': author_2_text,
                        'link': link_text,
                        'abstract': abstract_text}
                output.append(temp)

                driver.back()
                time.sleep(10)
                if page_num == 0:
                        print("Page number = ", page_num+1)
                else:
                        print("Page number = ", int((page_num/50)+1))
                print("Total number of articles in this page: ", len(articles))
                print("Scraping article # ", i)
                print("---------------------------------------------------------------------------------------------------")
                if i <= len(articles):
                        i = i + 1
                else:
                        break
        i = 1
        page_num = page_num + 50

output = pd.DataFrame(output)
output['date'] = pd.to_datetime(output['date'])
output.to_excel("output_arxiv.xlsx", index=False)
