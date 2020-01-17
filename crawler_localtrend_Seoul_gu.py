from selenium import webdriver
import csv
import time

link = 'https://datalab.naver.com/local/trend.naver'
search_btn_xpath = '//a[@class="com_btn_srch"]'

driver = webdriver.Chrome('C:/Gits/localtrend_crawler/chromedriver.exe')
driver.get(link)
time.sleep(5)

##서울 선택(area1)
area1_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[1]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'
driver.find_element_by_xpath(area1_option_xpath).click()
do = '서울'

for i in range (2, 11): ## 음식점(2). 관광(10)
    
    category_option_xpath = '((//div[@class="analysis_filter"]/div[@class="filter_area"])[1]/div[@class="filter_option scroll_cst"]/ul[@class="option_list _list1"]/li)[' + str(i) + ']'
    driver.find_element_by_xpath(category_option_xpath).click() ## Select a specific category
    time.sleep(1)

    category = driver.find_element_by_xpath(category_option_xpath + '/a').text[0:2] #Get a category name
    print(category)

    filepath = 'res_'+str(category)+'_seoul.csv' #Output file path
    f = open(filepath, 'w', encoding='utf-8', newline='') #Open output file
    csvfile = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL) #write CSV
    csvfile.writerow(['Do', 'Gu', 'Period', 'category', 'Value', 'Group']) ##Group is for the value recalculation


    area2_option_allpath ='((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[2]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'
    k = 1
    group = 0
        
    try:
        while k < 200: ##Try for all dong, so that add the maximum counts of the dongs.
            group = group+1
            driver.find_element_by_xpath(area2_option_allpath).click() ## Remove a previous selection set (gu)
            driver.find_element_by_xpath(area2_option_allpath).click()
            gucount = 0
            
            for l in range(0, 10):  ##Select 10 dongs then compare values later. if dong count is less than 10, it moves to next exception. 
                k = k+1
                area2_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[2]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(k) + ']/span/label'
                driver.find_element_by_xpath(area2_option_xpath).click() #Select a specific Gu

                gucount = gucount +1 ##Add dong count after click
                gunm = driver.find_element_by_xpath(area2_option_xpath).text
                print(gunm)
                
            #Click Search
            driver.find_element_by_xpath(search_btn_xpath).click()
            time.sleep(6)
            
            try:
                for m in range(1, 58): ##Select graph by week
                    time.sleep(1.5)
                    graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                    driver.find_element_by_xpath(graph_click_xpath).click()
                    period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                        
                    for n in range(1, gucount+1): ##Get value in each dong
                        category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                        gu = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                        value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value
                        csvfile.writerow([do, gu, period, category, value, group])                       
                       
            except: ##if dong includes all zero values, just passed.
                print('no values1')

    except: ##gu count less than 10
        
        driver.find_element_by_xpath(search_btn_xpath).click() #Click Search
        time.sleep(6)

        try:
            for m in range(1, 58): ##Select graph by week
                time.sleep(1.5)
                graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                driver.find_element_by_xpath(graph_click_xpath).click()

                period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                
                for n in range(1, gucount+1): ##Get value in each dong
                        category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                        gu = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                        value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value
                        csvfile.writerow([do, gu, period, category, value, group])
                    
        except: ##if dong includes all zero values, just passed.
            print('no values2')

    f.close() ##Save data


        
           






