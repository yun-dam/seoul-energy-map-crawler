# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 18:20:48 2023

@author: YUNDAM
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import json

class seoulEnergyMap():
    
    def __init__(self, outcomeType = 'energy', sourceType = 'electricity', guList = ['Gangnam'] , howManyPreviousYears = 3, howManyMonths = 12):
        
        self.driver = webdriver.Chrome('C:/Users/USER/Downloads/chromedriver')
        self.url="https://energyinfo.seoul.go.kr/portalMap/gis/page?menu-id=Z040400&menuFlag=analysis"
        self.driver.get(self.url)
    
        self.outcomeType = outcomeType
        self.sourceType = sourceType    
        self.howManyPreviousYears = howManyPreviousYears
        self.howManyMonths = howManyMonths
        
    def dataCrawling(self):
        
        if self.outcomeType == 'energy':
            
            self.label = 'analysis'
            self.outcomeNum = 1
            
            if self.sourceType == 'electricity':
                
                sourceNum = 1
                
            elif self.sourceType == 'natural_gas':
            
                sourceNum = 2
                
            elif self.sourceType == 'district_heat':
            
                sourceNum = 3  
            
        elif self.outcomeType == 'greenhouse_gas':
            
            self.label = 'gas'
            self.outcomeNum = 2
            
            if self.sourceType == 'total':
                
                sourceNum = 1
        
            elif self.sourceType == 'electricity':
                
                sourceNum = 2
                
            elif self.sourceType == 'natural_gas':
            
                sourceNum = 3
                
            elif self.sourceType == 'district_heat':
            
                sourceNum = 4  
                
                
        # Get into the energy or greenhouse gas tab 
        labelSelect = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'label.' + self.label + '[for="' + self.label + '"]')))
        labelSelect.click()
        time.sleep(3)            

        # Get into energy source
        source = self.driver.find_element(By.XPATH, '//*[@id="navigation"]/div/div[1]/div[2]/div[' + str(self.outcomeNum) + ']/div[1]/div[1]/span[' + str(sourceNum) + ']') # span[1~4]
        source.click()
        time.sleep(3)

        # Click datepicker
        dataLabel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='datepicker-" + self.label + "']")))
        dataLabel.click()
        time.sleep(3)

        # Click the month
        monthElement = self.driver.find_element(By.XPATH, "//td[text()='" + '1월' + "']")
        monthElement.click()
        time.sleep(3)

        # Select 30 per page
        guPageElement = self.driver.find_element(By.ID, "use-pager-gu-" + self.label + "_center")
        guSelectElement = guPageElement.find_element(By.TAG_NAME, "select")
        guPageSelect = Select(guSelectElement)
        guPageSelect.select_by_value("30")
        time.sleep(3)    
    
        dongPageElement = self.driver.find_element(By.ID, "use-pager-dong-" + self.label + "_center")
        dongSelectElement = dongPageElement.find_element(By.TAG_NAME, "select")
        dongPageSelect = Select(dongSelectElement)
        dongPageSelect.select_by_value("30")
        time.sleep(3)

        # Get into Gu of Interest
        gangnamGu = self.driver.find_element(By.ID, "selector-" + self.label + "-gu")
        gangnamGu.click()
        gangnamSelect = Select(gangnamGu)
        gangnamSelect.select_by_value('11680')
        time.sleep(3)

        # List the names of all districts 
        gu = self.driver.find_elements("xpath", '//td[@aria-describedby="use-grid-gu-' + self.label + '_SIGUNGU_NM"]')
        self.guValues = [x.text for x in gu]
               
        dong = self.driver.find_elements("xpath", '//td[@aria-describedby="use-grid-dong-' + self.label + '_BJDONG_NM"]')
        self.dongValues = [x.text for x in dong]
        
        monthName = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        year = ['2022', '2021', '2020']
        
        for y in range(self.howManyPreviousYears): 
                
            # Click datepicker
            dataLabel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='datepicker-" + self.label + "']")))
            dataLabel.click()
            time.sleep(3)
            
            # Click the previous year 
            prev_year_button = self.driver.find_element(By.CSS_SELECTOR, "button.tui-calendar-btn-prev-year")
            prev_year_button.click()
            time.sleep(3)    
        
            # Click the month
            monthElement = self.driver.find_element(By.XPATH, "//td[text()='" + '1월' + "']")
            monthElement.click()
            time.sleep(3)
            
            self.toCrawlGuData = pd.DataFrame(data = None, index=self.guValues, columns=monthName[:self.howManyMonths])
            self.toCrawlDongData = pd.DataFrame(data = None, index=self.dongValues, columns=monthName[:self.howManyMonths])
            
            for k in range(self.howManyMonths): # Jan ~ ?
            
                month = str(k+1) + '월'
        
                # Click datepicker
                dataLabel = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "label[for='datepicker-" + self.label + "']")))
                dataLabel.click()
                time.sleep(3)
                
                # Click the month
                monthElement = self.driver.find_element(By.XPATH, "//td[text()='" + month + "']")
                monthElement.click()
                time.sleep(3)
            
                # Select 30 per page
                guPageElement = self.driver.find_element(By.ID, "use-pager-gu-" + self.label + "_center")
                guSelectElement = guPageElement.find_element(By.TAG_NAME, "select")
                guPageSelect = Select(guSelectElement)
                guPageSelect.select_by_value("30")
                time.sleep(3)    
            
                dongPageElement = self.driver.find_element(By.ID, "use-pager-dong-" + self.label + "_center")
                dongSelectElement = dongPageElement.find_element(By.TAG_NAME, "select")
                dongPageSelect = Select(dongSelectElement)
                dongPageSelect.select_by_value("30")
                time.sleep(3)
                
                
                # Crwal the target data
                guTargetData = self.driver.find_elements("xpath", '//td[@aria-describedby="use-grid-gu-' + self.label + '_VAL"]')
                guDataValues = [x.text for x in guTargetData]
                
                dongTargetData = self.driver.find_elements("xpath", '//td[@aria-describedby="use-grid-dong-' + self.label + '_VAL"]')
                dongDataValues = [x.text for x in dongTargetData]
                
                self.toCrawlGuData[monthName[k]] = guDataValues
                self.toCrawlDongData[monthName[k]] = dongDataValues
                
            
            self.guDict = self.toCrawlGuData.to_dict(orient='index')
            self.dongDict = self.toCrawlDongData.to_dict(orient='index')
            
            if y == 0:
                
                newGuDict ={}
                
                for a in self.guValues:
                    
                    addGuDict = { a: {year[y]: self.guDict[a] } }
                    newGuDict.update(addGuDict)
                
            else: 
                for a in self.guValues:
        
                    newGuDict[a][year[y]] = self.guDict[a]
                    
                    
            self.guDict = self.toCrawlGuData.to_dict(orient='index')
            
            if y == 0:
                
                newDongDict ={}
                
                for a in self.dongValues:
                    
                    addDongDict = { a: {year[y]: self.dongDict[a] } }
                    newDongDict.update(addDongDict)
                
            else: 
                for a in self.dongValues:
        
                    newDongDict[a][year[y]] = self.dongDict[a]            
                    
            # data save
            
            with open('./guEnergyMapData.json','w') as f:
                json.dump(self.guDict, f, ensure_ascii=False, indent=4)    
                
            with open('./dongEnergyMapData.json','w') as f:
                json.dump(self.dongDict, f, ensure_ascii=False, indent=4)    
                