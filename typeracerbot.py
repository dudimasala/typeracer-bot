from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common import exceptions
import time


class TyperacerBot:
    def __init__(self):
        #gets user's words per minute(wpm) input, and checks if it's an integer. 
        user_wpm = 60
        while True:
            try:
                user_wpm = int(input("How many wpm?(not fully accurate) \n>"))
            
            except ValueError:
                print("sorry, you didn 't enter an integer. Please try again.")
                continue
            
            if user_wpm <= 0:
                print("You must enter a positive integer. Please try again")
             
            else:
                break    
        #inits driver    
        self.driver = webdriver.Chrome('/Users/amitrajpal/Downloads/Instagram_bot/chromedriver')    
        #accesses webite
        self.access_website()
        #gets the needed text array and stores it        
        text_needed = self.get_text()
        #checks if race has begun
        self.raceIsOnCheck()
        #takes out unnecessary space at the end
        text_needed.pop()
        #types out words and spaces near the wpm indicated
        self.wordsPerMinute(user_wpm, text_needed)
        
    #open the typeracer website
    def access_website(self):
        self.driver.get('https://play.typeracer.com/')
        #finds and clicks the play button(to enter a race)
        play_button = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="dUI"]/table/tbody/tr[2]/td[2]/div/div[1]/div/table/tbody/tr[2]/td/table/tbody/tr/td[2]/table/tbody/tr[1]/td/a')))
        play_button.click()

    #gets the text
    def get_text(self):
        #since entire typeracer text is stored in 3 html elements, it gets all and adds it all to a variable final_text
        text1 = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[1]'))).text
        text2 = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[2]'))).text
        text3 = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[1]/td/table/tbody/tr[1]/td/div/div/span[3]'))).text
        final_text = text1 + text2 + " " + text3 + " "
        #one word in every array index
        final_text_array = final_text.split(" ")
        return final_text_array
    
    #locates the text box and inputs some text
    def play(self, text):
        inputed_text = WebDriverWait(self.driver, 20).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[2]/td/table/tbody/tr[2]/td/input')))
        inputed_text.send_keys(text)
        
    #not fully accurate(depends on the number of spaces/word length) but usually within 15-20 wpm. Gets less accurate as you get much faster(go past 300wpm for example)
    def wordsPerMinute(self, wpm, text):
        #my formula for speed based on trial and error
        speed = 60/wpm - 0.14
        #if wpm is big enough to make speed < 0 then speed = 0(maxes out at around 450 but anyways typeracer blocks the player from continuing if you're too fast)
        if speed < 0:
            speed = 0
        #types a word and then sleeps for the time indicated by speed before next word is typed
        for i in range(len(text)):
            #accounts for little nuance(where our program previously put two spaces around a comma(if it separated two different html elements). Now it's just one space after the comma.
            if text[1] != "," or i != 0:
                self.play(text[i])
                if i != len(text) - 1:
                    #space after comma
                    self.play(" ")
                    #sleep after word is typed
                    time.sleep(speed)
                else:
                    try:
                        self.play(" ")
                    #Error may show up at the end(when the program wants to type a final space but is not able to because the race ended). Passes the error.    
                    except exceptions.ElementNotInteractableException:
                        pass
            
            #if it's a normal word then just type word and wait for speed seconds(controls wpm) 
            else:
                self.play(text[i])
                time.sleep(speed)
      
        
        
    #checks if the race has started or if the timer(before the race begins) is still counting        
    def raceIsOnCheck(self):
        gameOnText = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/div'))).text
        while("The race is on" not in gameOnText):
            gameOnText = WebDriverWait(self.driver, 5).until(expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="gwt-uid-15"]/table/tbody/tr[1]/td/table/tbody/tr[1]/td/table/tbody/tr/td[1]/div'))).text
            
        
        
        
#inits the bot
if __name__ == "__main__":
    TyingBot = TyperacerBot()
        
