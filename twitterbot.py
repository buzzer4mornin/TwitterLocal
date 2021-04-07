from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
import numpy as np
import random
import time, os
'''Uncomment the below line for Linux OS'''
# from pyvirtualdisplay import Display



class Twitterbot:

    # TODO:instead of email, we will use username, and add email separately along with password [3 total arguments]
    # TODO: if email or username throws error, use another one
    def __init__(self, email, username, password, phone):
        self.email = email
        self.username = username
        self.password = password
        self.phone = phone
        # initializing chrome options
        chrome_options = Options()
        self.bot = webdriver.Chrome(
            executable_path=os.path.join(os.getcwd(), 'chromedriver'),
            options=chrome_options
        )

    def login(self):

        bot = self.bot
        bot.maximize_window()
        bot.get('https://twitter.com/login')

        time.sleep(3)
        bot.implicitly_wait(10)

        email_or_username = bot.find_element_by_css_selector(
            '#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(6) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input'
        )
        password = bot.find_element_by_css_selector(
            '#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(7) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input'
        )

        # sends the email to the email input
        email_or_username.send_keys(self.email)
        time.sleep(np.random.randint(1, 4))
        # sends the password to the password input
        password.send_keys(self.password)
        time.sleep(np.random.randint(1, 4))
        # executes RETURN key action
        password.send_keys(Keys.RETURN)
        bot.implicitly_wait(10)

        # Login Error 1! Use another method (email/username interchangibility) to log in
        bodyText = bot.find_element_by_tag_name('body').text
        if "There was unusual login activity" in bodyText:
            time.sleep(np.random.randint(2, 4))
            another_login = bot.find_element_by_css_selector("#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(6) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input")
            another_login.send_keys(self.username)
            time.sleep(np.random.randint(1, 4))
            another_password = bot.find_element_by_css_selector("#react-root > div > div > div.css-1dbjc4n.r-13qz1uu.r-417010 > main > div > div > div.css-1dbjc4n.r-13qz1uu > form > div > div:nth-child(7) > label > div > div.css-1dbjc4n.r-18u37iz.r-16y2uox.r-1wbh5a2.r-1udh08x > div > input")
            another_password.send_keys(self.password)
            time.sleep(np.random.randint(1, 4))
            another_password.send_keys(Keys.RETURN)

        # Login Error 2! Type phone for confirmation
        bodyText = bot.find_element_by_tag_name('body').text
        if "Your phone number ends" in bodyText:
            phone = bot.find_element_by_xpath("//*[@id='challenge_response']")
            phone.send_keys(self.phone)
            submit = bot.find_element_by_xpath("//*[@id='email_challenge_submit']").click()

    def random_scroll(self, step, speed, interval):
        bot = self.bot
        bot.implicitly_wait(50)

        for i in range(interval):
            a = "window.scrollTo(0," + str(i * speed) + ")"
            bot.execute_script(a)
            if i % step == 0 and bool(random.getrandbits(1)):
                # randomly stop for random amount of time during scroll
                time.sleep(np.random.randint(2, 7))
        time.sleep(np.random.randint(1, 4))

    def go_home(self, h_step, h_speed, h_interval):
        bot = self.bot
        bot.implicitly_wait(10)
        time.sleep(np.random.randint(1, 3))

        # go to homepage
        home_link = bot.find_element_by_xpath('//a[@href="/home"]')
        home_link.click()
        time.sleep(np.random.randint(1, 4))

        # scroll down on profile & maybe LIKE depending on flag
        # randomize intervals || recommended h_step=30, h_speed = np.random.randint(4, 7), h_start=0, h_end = np.random.randint(400, 800)
        self.random_scroll(step=h_step, speed=h_speed, interval=h_interval)

    #TODO: 'cook' needs username, not email. Update it accordingly
    def go_profile(self, p_step, p_speed, p_interval):
        bot = self.bot
        bot.implicitly_wait(20)
        time.sleep(np.random.randint(1, 4))

        # go to profile
        cook = '//a[@href="/' + self.email + '"]'
        profile_link = bot.find_element_by_xpath(cook)
        profile_link.click()
        time.sleep(np.random.randint(1, 4))

        # randomize intervals || recommended p_step=30, p_speed=np.random.randint(2, 5), p_start=0, p_end=np.random.randint(250, 400)
        self.random_scroll(step=p_step, speed=p_speed, interval=p_interval)

        home_link = bot.find_element_by_xpath('//a[@href="/home"]')
        home_link.click()

    def go_notif(self, n_step, n_speed, n_interval):
        bot = self.bot
        bot.implicitly_wait(20)
        time.sleep(np.random.randint(1, 4))

        # go to notification
        notif_link = bot.find_element_by_xpath('//a[@href="/notifications"]')
        notif_link.click()
        time.sleep(np.random.randint(2, 5))

        # TODO: "mentions" element not interactible
        # 70% of time -> go to mentions on notification
        try:
            if np.random.rand() < 0.70:
                mention = bot.find_element_by_xpath('//a[@href="/notifications/mentions"]')
                mention.click()
                time.sleep(np.random.randint(3, 6))

                # go back to notification
                notif_link = bot.find_element_by_xpath('//a[@href="/notifications"]')
                notif_link.click()
                time.sleep(np.random.randint(2, 4))
        except:
            raise Exception("/mentions elements is not interactible!")

        # scroll down on notifications
        # randomize intervals || recommended n_step=20, n_speed=np.random.randint(1, 4), n_start=0, n_end=np.random.randint(250, 350)
        self.random_scroll(step=n_step, speed=n_speed, interval=n_interval)

        home_link = bot.find_element_by_xpath('//a[@href="/home"]')
        home_link.click()

    # TODO: Liking is not working properly if there is subtweets. Investigate.
    # TODO: Add hotflaglikes. Currently only latelikes available
    def visit_random_hashtags(self, hotflag_l, hotflag_r ,lateflag, latelikes):

        bot = self.bot
        bot.implicitly_wait(50)
        time.sleep(np.random.randint(1, 4))
        hashtags = ["hashtag1", "hashtag2", "hashtag3", "hashtag4",
                    "hashtag5", "hashtag6", "hashtag7", "hashtag8",
                    "hashtag9", "hashtag10"]

        visit_counts = np.random.randint(2, 3)
        for i in range(visit_counts):
            target = hashtags[np.random.randint(0, len(hashtags))]
            hashtags.remove(target)
            target_hash = "#" + target
            explore_link = bot.find_element_by_xpath('//a[@href="/explore"]')
            explore_link.click()

            # scroll in HOT
            time.sleep(np.random.randint(2, 4))
            search_link = bot.find_element_by_xpath(
                '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input'
            )
            search_link.send_keys(target_hash)
            time.sleep(np.random.randint(2, 4))
            search_link.send_keys(Keys.ENTER)
            time.sleep(np.random.randint(2, 4))

            # randomize intervals || recommended interval [400,800]
            self.random_scroll(step=40, speed=np.random.randint(12, 15), interval=np.random.randint(400, 800))
            time.sleep(np.random.randint(2, 4))

            # Section for Like or Retweet Hot tweets of hashtag
            if hotflag_l or hotflag_r:
                links = set()
                for _ in range(2):
                    time.sleep(np.random.randint(1, 4))
                    [
                        links.add(elem.get_attribute('href')) \
                        for elem in bot.find_elements_by_xpath("//a[@dir ='auto']")
                    ]
                # traversing through the generated links
                count = 0
                for link in links:
                    if "status" not in link: continue
                    if count > 2: break
                    bot.get(link)
                    time.sleep(np.random.randint(3, 5))
                    # Like Hot tweets of hashtag
                    if hotflag_l:
                        try:
                            # like button selector
                             bot.find_element_by_css_selector(
                                '.css-18t94o4[data-testid ="like"]'
                             ).click()
                             time.sleep(np.random.randint(3, 5))
                        except:
                            time.sleep(np.random.randint(1, 4))

                    # Retweet Hot tweets of hashtag
                    if hotflag_r:
                        try:
                            # like button selector
                             bot.find_element_by_css_selector(
                                '.css-18t94o4[data-testid ="retweet"]'
                             ).click()
                             time.sleep(np.random.randint(1, 2))
                             bot.find_element_by_css_selector(
                                '.css-1dbjc4n[data-testid ="retweetConfirm"]'
                             ).click()
                             time.sleep(np.random.randint(3, 5))
                        except:
                            time.sleep(np.random.randint(1, 4))
                    count += 1

            # ==========================================================================================================
            # ============================================= Connection =================================================
            # ==========================================================================================================
            home_link = bot.find_element_by_xpath('//a[@href="/home"]')             # ========= CONNECTION =============
            home_link.click()                                                       # ========= CONNECTION =============
            explore_link = bot.find_element_by_xpath('//a[@href="/explore"]')       # ========= CONNECTION =============
            explore_link.click()                                                    # ========= CONNECTION =============
            time.sleep(np.random.randint(2, 4))                                     # ========= CONNECTION =============
            search_link = bot.find_element_by_xpath('//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div/div/div[1]/div[1]/div/div/div/div/div[1]/div[2]/div/div/div/form/div[1]/div/div/div[2]/input')                                                                       # ========= CONNECTION ============
            search_link.send_keys(target_hash)                                      # ========= CONNECTION =============
            time.sleep(np.random.randint(2, 4))                                     # ========= CONNECTION =============
            search_link.send_keys(Keys.ENTER)                                       # ========= CONNECTION =============
            time.sleep(np.random.randint(2, 4))                                     # ========= CONNECTION =============
            # ==========================================================================================================
            # ==========================================================================================================
            # ==========================================================================================================

            # scroll in LATEST
            body = '//a[@href="/search?q=%23' + target + '&src=typed_query&f=live"]'
            latest_link = bot.find_element_by_xpath(body)
            latest_link.click()
            time.sleep(np.random.randint(2, 4))

            # randomize intervals || recommended interval [400,700]
            self.random_scroll(step=40, speed=np.random.randint(12, 15), interval=np.random.randint(400, 800))
            time.sleep(np.random.randint(2, 4))

            # Like LATEST tweets of hashtag
            if lateflag:
                links = set()
                for _ in range(2):
                    time.sleep(np.random.randint(1, 4))
                    [
                        links.add(elem.get_attribute('href')) \
                        for elem in bot.find_elements_by_xpath("//a[@dir ='auto']")
                    ]
                # traversing through the generated links
                count = 0
                for link in links:
                    if "status" not in link: continue
                    if count > latelikes: break
                    bot.get(link)
                    time.sleep(4)
                    try:
                         # like button selector
                         bot.find_element_by_css_selector(
                            '.css-18t94o4[data-testid ="like"]'
                         ).click()
                         time.sleep(np.random.randint(3, 5))
                    except:
                        time.sleep(np.random.randint(1, 4))
                    count += 1

            home_link = bot.find_element_by_xpath('//a[@href="/home"]')
            home_link.click()

    def post_tweet(self, mytweet):
        bot = self.bot
        bot.implicitly_wait(50)
        bot.maximize_window()

        try:
            home_link = bot.find_element_by_xpath('//a[@href="/home"]')
            home_link.click()
        except:
            raise Exception("Go twitter/home in order to tweet")

        '#1 option for Tweet'
        #tweet = bot.find_element_by_css_selector("br[data-text='true']")
        #time.sleep(2)
        #tweet.send_keys(mytweet)
        #time.sleep(np.random.randint(6, 12))
        #try:
        #    tweet.send_keys(Keys.COMMAND + Keys.ENTER)
        #except:
        #    bot.save_screenshot('error-cant-tweet.png')
        #    raise Exception("Can not Tweet. See screenshot - 'error-cant-tweet.png'")

        '#2 option for Tweet'
        tweet = bot.find_element_by_css_selector(".notranslate > div:nth-child(1) > div:nth-child(1)")
        tweet = tweet.find_element_by_xpath("./div")
        tweet.click()
        tweet.send_keys(mytweet)
        time.sleep(np.random.randint(6, 12))
        try:
            tweet.send_keys(Keys.COMMAND + Keys.ENTER)
        except:
            bot.save_screenshot('error-cant-tweet.png')
            raise Exception("Can not Tweet. See screenshot - 'error-cant-tweet.png'")


        '''#3 option for Google Collab [Collab@deepfakevasmoy - MainTwitterBot.ipynb]
         def post_tweet(self):
        bot = self.bot
        bot.implicitly_wait(50)
        bot.maximize_window()
        
        tweet = bot.find_element_by_css_selector("br[data-text='true']")
        time.sleep(2)
        tweet.send_keys(mytweet)
        time.sleep(2)
        button = bot.find_element_by_css_selector("div[data-testid='tweetButtonInline']")
        button.click()
        time.sleep(2)

        bot.save_screenshot('screenshot.png')'''

    #TODO: complete randomized messaging between bots
    def send_message(self):
        bot = self.bot
        bot.implicitly_wait(20)
        time.sleep(np.random.randint(1, 4))

        # go to profile
        messages_link = bot.find_element_by_xpath('//a[@href="/messages"]').click()
        time.sleep(np.random.randint(1, 3))
        conv_link = bot.find_element_by_xpath('//a[@href="/fly_byhigh"]').click() # goes to profile page of @artisnoble from conversations page

        DM_link = bot.find_element_by_css_selector("div[data-testid='sendDMFromProfile']").click()

        '''mess = bot.find_element_by_xpath(
            '//div[contains(@class,"css-1dbjc4n r-xoduu5 r-1sp51qo r-atwnbb r-13qz1uu")]'
        )'''
        '''mess = bot.find_element_by_xpath(
                    './/div[@class="DraftEditor-root"]'
                )'''
        #mess.send_keys("hee")
