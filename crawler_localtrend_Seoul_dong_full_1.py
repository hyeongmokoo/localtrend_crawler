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

for i in range (1, 2): #기업 ## 음식점(2). 관광(10)
    
    category_option_xpath = '((//div[@class="analysis_filter"]/div[@class="filter_area"])[1]/div[@class="filter_option scroll_cst"]/ul[@class="option_list _list1"]/li)[' + str(i) + ']'
    driver.find_element_by_xpath(category_option_xpath).click() ## Select a specific category
    time.sleep(1)

    category = driver.find_element_by_xpath(category_option_xpath + '/a').text[0:2] #Get a category name
    print(category)

    area2_option_allpath ='((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[2]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'

    for j in range(2, 27):##종로구(2) 강동구 (26) 
        
        ab10 = 0 ##if dong count is larger than 10, then 1, otherwise 0
        driver.find_element_by_xpath(area2_option_allpath).click() 
        driver.find_element_by_xpath(area2_option_allpath).click() ## Remove a previous selection set (gu)
        
        area2_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[2]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(j) + ']/span/label'
        gu = driver.find_element_by_xpath(area2_option_xpath).text #Get a Gu name
        print(gu)

        driver.find_element_by_xpath(area2_option_xpath).click() #Select a specific Gu
        time.sleep(3)
            
        ##Get dong count
        area3_allselection_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'
            
        try:
            driver.find_element_by_xpath(area3_allselection_xpath).click()
            driver.find_element_by_xpath(area3_allselection_xpath).click() ## Remove a previous selection set (dong)
            ##Select 11th dong
            s = 12
            area3_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(s) + ']/span/label'
            driver.find_element_by_xpath(area3_option_xpath).click()
            driver.find_element_by_xpath(area3_option_xpath).click()
            ab10 = 1
            print("#dong > 10")
        except:
            ab10 = 0
            #print("#dong <= 10")
            
        if ab10 == 0:##if dong count is larger than 10,
            #print ("ab10 = 0")

            filepath = 'res_'+str(category)+"_"+ str(gu)+'.csv' #Output file path
            f = open(filepath, 'w', encoding='utf-8', newline='') #Open output file
            csvfile = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL) #write CSV
            csvfile.writerow(['Do', 'Gu', 'Dong', 'Period', 'category', 'Value', 'Group']) ##Group is for the value recalculation

            k = 1
            group = 0
            
            try:
                while k < 200: ##Try for all dong, so that add the maximum counts of the dongs.
                    ##Deselect all
                    group = group+1
                    driver.find_element_by_xpath(area3_allselection_xpath).click()
                    driver.find_element_by_xpath(area3_allselection_xpath).click() ## Remove a previous selection set (dong)
                    dongcount = 0

                    for l in range(0, 10):  ##Select 10 dongs then compare values later. if dong count is less than 10, it moves to next exception. 
                        k = k+1
                        area3_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(k) + ']/span/label'
                        driver.find_element_by_xpath(area3_option_xpath).click() #Select a specific dong

                        dongcount = dongcount +1 ##Add dong count after click
                        dongnm = driver.find_element_by_xpath(area3_option_xpath).text 
                        print(dongnm)

                    #Click Search
                    driver.find_element_by_xpath(search_btn_xpath).click()
                    time.sleep(6)

                    try:
                        for m in range(1, 58): ##Select graph by week
                            time.sleep(1.5)
                            graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                            driver.find_element_by_xpath(graph_click_xpath).click()
                            period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                            period = str(m)+"_"+period
                                
                            for n in range(1, dongcount+1): ##Get value in each dong
                                category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                                dong = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                                value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value
                                csvfile.writerow([do, gu, dong, period, category, value, group])                       
                               
                    except: ##if dong includes all zero values, just passed.
                        print('no values1')

            except: ##Dong count less than 10
                
                driver.find_element_by_xpath(search_btn_xpath).click() #Click Search
                time.sleep(6)

                try:
                    for m in range(1, 58): ##Select graph by week
                        time.sleep(1.5)
                        graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                        driver.find_element_by_xpath(graph_click_xpath).click()

                        period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                        period = str(m)+"_"+period
                        
                        for n in range(1, dongcount+1): ##Get value in each dong
                            category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                            dong = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                            value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value
                            csvfile.writerow([do, gu, dong, period, category, value, group])
                            
                except: ##if dong includes all zero values, just passed.
                    print('no values2')

            f.close() ##Save data

        else :##if dong count is smaller than 10,
            #Find a dong with the maximum values
            #print ("ab10 = 1")
            area3_allselection_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'
            driver.find_element_by_xpath(area3_allselection_xpath).click()

            #Click Search
            driver.find_element_by_xpath(search_btn_xpath).click()
            time.sleep(6)

##Find highest dong
            dongcount = 10
            highestdongnm = ""
            m = 0
            while highestdongnm == "":
                m = m +1 
                time.sleep(1.5)
                graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                driver.find_element_by_xpath(graph_click_xpath).click()
                    
                for n in range(1, dongcount+1): ##Get value in each dong
                    category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                    value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value
                    if value == str(100):
                        highestdongnm = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname

            #print("#1 highest dong is "+ highestdongnm)
            driver.find_element_by_xpath(area3_allselection_xpath).click() ##Remove all selection
            
##Find index of highest dong
            k=2
            area3_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(k) + ']/span/label'
            dongnm = driver.find_element_by_xpath(area3_option_xpath).text

            while dongnm != highestdongnm:
                k=k+1
                area3_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(k) + ']/span/label'
                dongnm = driver.find_element_by_xpath(area3_option_xpath).text

            maxidx = k
            #print("#2 highest dong is "+ str(dongnm))

            filepath = 'res_'+str(category)+"_"+ str(gu)+'.csv' #Output file path
            f = open(filepath, 'w', encoding='utf-8', newline='') #Open output file
            csvfile = csv.writer(f, quotechar='"', quoting=csv.QUOTE_MINIMAL) #write CSV
            csvfile.writerow(['Do', 'Gu', 'Dong', 'Period', 'category', 'Value', 'Group']) ##Group is for the value recalculation

            k = 1
            area3_allselection_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[1]/span/label'
            group = 0
            
            try:
                while k < 200: ##Try for all dong, so that add the maximum counts of the dongs.
                    ##Deselect all
                    group = group+1
                    driver.find_element_by_xpath(area3_allselection_xpath).click()
                    driver.find_element_by_xpath(area3_allselection_xpath).click() ## Remove a previous selection set (dong)

                    area3_highest_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(maxidx) + ']/span/label'
                    driver.find_element_by_xpath(area3_highest_xpath).click() #Select a highest dong
                            
                    dongcount = 0

                    while dongcount < 9:
                        k = k+1
                        if k != maxidx:
                            area3_option_xpath = '((//div[@class="analysis_step v2"]/div[@class="analysis_filter"]/div[@class="filter_area"])[3]/div[@class="filter_option scroll_cst"]/ul/li)[' + str(k) + ']/span/label'
                            driver.find_element_by_xpath(area3_option_xpath).click() #Select a specific dong
                            dongcount = dongcount +1 ##Add dong count after click
                            dongnm = driver.find_element_by_xpath(area3_option_xpath).text 
                            print(dongnm)

                    #Click Search
                    driver.find_element_by_xpath(search_btn_xpath).click()
                    time.sleep(6)

                    try:
                        for m in range(1, 58): ##Select graph by week
                            time.sleep(1.5)
                            graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                            driver.find_element_by_xpath(graph_click_xpath).click()
                            period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                            period = str(m)+"_"+period
                                
                            for n in range(1, dongcount+2): ##Get value in each dong + the maximum dong
                                category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                                dong = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                                value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value

                                if(group == 1):
                                    print(dong)
                                    csvfile.writerow([do, gu, dong, period, category, value, group])
                                else:
                                    if(dong != highestdongnm):
                                        print(dong)
                                        csvfile.writerow([do, gu, dong, period, category, value, group])

                                    
                               
                    except: ##if dong includes all zero values, just passed.
                        print('no values1')

            except: ##Dong count less than 9
                
                driver.find_element_by_xpath(search_btn_xpath).click() #Click Search
                time.sleep(6)

                try:
                    for m in range(1, 58): ##Select graph by week
                        time.sleep(1.5)
                        graph_click_xpath = '(//div[@class="section_graph"]/div[@class="com_box_inner"]/div[@class="graph_area"]/div[@class="inner_graph_area _trend_graph bb"]/*[name()="svg"]/*[name()="g"]/*[name()="g" and @class="bb-chart"]/*[name()="g" and @class="bb-event-rects bb-event-rects-single"]/*[name()="rect"])[' + str(m) + ']'
                        driver.find_element_by_xpath(graph_click_xpath).click()

                        period = driver.find_element_by_xpath('//div[@class="tooltip_period"]').text
                        period = str(m)+"_"+period
                        
                        for n in range(1, dongcount+2): ##Get value in each dong
                            category_xpath = '(//div[@class="graph_tooltip"]/div[@class="tooltip"])[' + str(n) + ']'
                            dong = driver.find_element_by_xpath(category_xpath + '/span[@class="info"]').text #get dongname
                            value = driver.find_element_by_xpath(category_xpath + '/span[@class="value"]').text #get value

                            if(group == 1):
                                print(dong)
                                csvfile.writerow([do, gu, dong, period, category, value, group])
                            else:
                                if(dong != highestdongnm):
                                    print(dong)
                                    csvfile.writerow([do, gu, dong, period, category, value, group])
                            
                except: ##if dong includes all zero values, just passed.
                    print('no values2')

            f.close() ##Save data

            
        
           






