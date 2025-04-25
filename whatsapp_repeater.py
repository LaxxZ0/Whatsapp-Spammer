from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
from datetime import datetime
import os
import sys
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("whatsapp_log.txt")
    ]
)
logger = logging.getLogger(__name__)

# Add logo and developer credit
def show_logo():
    logo = """
     .---.  .---.  .---.  .---.  .---.  .---.  .---.  .---.  
    /:    \\/:    \\/:    \\/:    \\/:    \\/:    \\/:    \\/:    \\ 
    \\:    /\\:    /\\:    /\\:    /\\:    /\\:    /\\:    /\\:    / 
     `---'  `---'  `---'  `---'  `---'  `---'  `---'  `---'  
    ░██╗░░░░░░░██╗██╗░░██╗░█████╗░████████╗░██████╗░█████╗░██████╗░██████╗░
    ░██║░░██╗░░██║██║░░██║██╔══██╗╚══██╔══╝██╔════╝██╔══██╗██╔══██╗██╔══██╗
    ░╚██╗████╗██╔╝███████║███████║░░░██║░░░╚█████╗░███████║██████╔╝██████╔╝
    ░░████╔═████║░██╔══██║██╔══██║░░░██║░░░░╚═══██╗██╔══██║██╔═══╝░██╔═══╝░
    ░░╚██╔╝░╚██╔╝░██║░░██║██║░░██║░░░██║░░░██████╔╝██║░░██║██║░░░░░██║░░░░░
    ░░░╚═╝░░░╚═╝░░╚═╝░░╚═╝╚═╝░░╚═╝░░░╚═╝░░░╚═════╝░╚═╝░░╚═╝╚═╝░░░░░╚═╝░░░░░
    ▄▀▀▀▀▄ ▄▀▀█▀▄   ▄▀▀▀▀▄   ▄▀▀▄ ▄▀▄  ▄▀▀▄ ▄▀▄  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
    █ █   ▐ █   █    █      █ █  █ ▀  █ █  █ ▀  █ ▐  ▄▀   ▐ █   █   █ 
    ▐  ▀▄   ▐   █    █      █ ▐  █    █ ▐  █    █   █▄▄▄▄▄  ▐  █▀▀█▀  
     ▄▀▀▀▀▄    █      ▀▄    ▄▀   █    █    █    █   █    ▌   ▄▀    █  
    █    ▐   ▄▀▄▀      ▀▀▀▀     ▀▄▄▄▄▀  ▀▄▄▄▄▀  ▄▀▄▄▄▄   █     █     
    ▐        █                                    █    ▐   ▐     ▐     
             ▐                                    ▐                     
    ================================================================
                     👻 WhatsApp SPAMMER v2.1.0 👻
                       Developed by: Omar Shalby
    ================================================================
    """
    print(logo)
    logger.info("Starting WhatsApp SPAMMER v2.1.0...")

def main():
    try:
        show_logo()  # Add this line here
        interval_seconds = float(input("Enter interval between messages in seconds (default 1.0): ") or 1.0)
    except ValueError:
        interval_seconds = 1.0
        logger.warning("Invalid interval value, using default: 1.0 seconds")
    
    try:
        max_messages = int(input("Enter maximum number of messages (0 for unlimited): ") or 0)
    except ValueError:
        max_messages = 0
        logger.warning("Invalid max messages value, using unlimited")
    
    contact_name = input("Enter the contact or group name to send messages to: ")
    message_to_repeat = input("Enter the message you want to repeat: ")
    
    # Initialize web driver
    logger.info("Initializing Chrome WebDriver...")
    chrome_options = Options()
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-gpu") # Suppress console logs
    chrome_options.add_argument("--log-level=3")  # Suppress console logs
    # Add user data directory to maintain login sessions (optional)
    user_data_dir = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Chrome", "User Data", "WhatsAppBot")
    if not os.path.exists(user_data_dir):
        os.makedirs(user_data_dir, exist_ok=True)
        logger.info(f"Created Chrome profile directory at: {user_data_dir}")
    else:
        logger.info(f"Using existing Chrome profile directory: {user_data_dir}")
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
    chrome_options.add_argument("--profile-directory=Default")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        
        # Set script timeout
        driver.set_script_timeout(120)
        
        # Open WhatsApp Web
        logger.info("Opening WhatsApp Web...")
        driver.get("https://web.whatsapp.com")
        # Wait for WhatsApp to load
        wait = WebDriverWait(driver, 120)
        logger.info("Waiting for WhatsApp Web to load. Please scan QR code if prompted.")
        
        # Check if QR code is present (meaning we need to log in)
        try:
            qr_code = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//canvas[@aria-label="Scan me!"]'))
            )
            logger.warning("QR code detected - please scan to log in. This session will be saved for future use.")
        except TimeoutException:
            logger.info("No QR code found - you appear to be already logged in.")
            
        # Wait for the sidebar to load, indicating WhatsApp is ready
        try:
            sidebar = wait.until(EC.presence_of_element_located((By.XPATH, '//div[@id="side"]')))
            logger.info("WhatsApp Web loaded successfully!")
        except TimeoutException:
            logger.error("Timeout waiting for WhatsApp to load. Please check your internet connection.")
            return
        # Give additional time for elements to fully load
        time.sleep(3)
        
        # Search for the contact
        logger.info(f"Searching for: {contact_name}")
        # Try different search box selectors
        search_selectors = [
            "//div[@contenteditable='true'][@data-tab='3']",
            "//div[@contenteditable='true'][@data-testid='chat-list-search']",
            "//div[@role='textbox'][@title='Search input textbox']"
        ]
        
        search_box = None
        for selector in search_selectors:
            try:
                search_box = wait.until(EC.presence_of_element_located((By.XPATH, selector)))
                search_box.clear()
                search_box.send_keys(contact_name)
                logger.info(f"Using search selector: {selector}")
                break
            except (TimeoutException, NoSuchElementException):
                continue
        
        if not search_box:
            logger.error("Could not find the search box.")
            return
        # Give time for search results to appear
        time.sleep(3)
        
        # Try to find and click on the contact
        contact_found = False
        contact_selectors = [
            f"//span[@title='{contact_name}']",
            f"//span[contains(@title, '{contact_name}')]",
            f"//div[@data-testid='cell-frame-title']//span[contains(text(), '{contact_name}')]"
        ]
        
        for selector in contact_selectors:
            try:
                contact = wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                contact.click()
                contact_found = True
                logger.info(f"Selected contact using selector: {selector}")
                break
            except (TimeoutException, NoSuchElementException):
                continue
        
        if not contact_found:
            logger.error(f"Could not find contact: {contact_name}. Please check the spelling.")
            return
        
        # Wait for chat to load
        time.sleep(2)
        
        # Try to locate the message input box
        logger.info("Locating message input box...")
        message_box_selectors = [
            "//div[@contenteditable='true'][@data-tab='10']",
            "//div[@contenteditable='true'][@data-testid='conversation-compose-box-input']",
            "//div[@role='textbox'][@title='Type a message']"
        ]
        
        # Prepare for message sending
        logger.info(f"Will send message: '{message_to_repeat}' every {interval_seconds} seconds")
        logger.info("Press Ctrl+C to stop the script.")
        
        # Start sending messages
        message_count = 0
        
        while True:
            if max_messages > 0 and message_count >= max_messages:
                logger.info(f"Reached maximum message count ({max_messages}). Stopping...")
                break
            
            message_box = None
            # Try each selector for the message box
            for selector in message_box_selectors:
                try:
                    message_box = WebDriverWait(driver, 5).until(
                        EC.presence_of_element_located((By.XPATH, selector))
                    )
                    break
                except (TimeoutException, NoSuchElementException):
                    continue
            
            if not message_box:
                logger.error("Could not find message input box. Retrying...")
                time.sleep(2)
                continue
                
            try:
                # Clear any existing text
                message_box.clear()
                
                # Send the message
                message_box.send_keys(message_to_repeat)
                message_box.send_keys(Keys.RETURN)
                message_count += 1
                current_time = datetime.now().strftime('%H:%M:%S')
                logger.info(f"Message #{message_count} sent at {current_time}")
                
                # Wait for the specified interval
                time.sleep(interval_seconds)
                
            except StaleElementReferenceException:
                logger.warning("Element became stale. Refinding elements...")
                time.sleep(1)    
                continue
            except Exception as e:
                logger.error(f"Error sending message: {str(e)}")
                time.sleep(2)
                continue
                
    except KeyboardInterrupt:
        logger.info("\nScript stopped by user.")
    except Exception as e:
        logger.error(f"\nAn unexpected error occurred: {str(e)}")
    finally:
        logger.info("Closing browser...")
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()