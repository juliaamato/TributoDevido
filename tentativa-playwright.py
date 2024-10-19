from playwright.sync_api import sync_playwright
import time
import random
import pyautogui

def smooth_scroll(distance):
    for _ in range(distance // 100):
        pyautogui.scroll(-100)
        time.sleep(random.uniform(0.05, 0.15))

def move_mouse_to_element(element):
    box = element.bounding_box()
    if box:
        x = box['x'] + box['width'] / 2-100
        y = box['y'] + box['height'] / 2+100
        pyautogui.moveTo(x, y, duration=random.uniform(0.5, 1.0))

def run(playwright):
    browser = playwright.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://www.upwork.com/freelance-jobs/")
    
    page.wait_for_selector("#onetrust-close-btn-container button")
    page.click("#onetrust-close-btn-container button")

    checkbox_group = page.query_selector("#checkbox-group-1")
    parent_element = checkbox_group.evaluate_handle("element => element.parentElement")
    labels = parent_element.query_selector_all("label")
    
    for label in labels:
        if label.inner_text().strip() == "Development & IT":
            move_mouse_to_element(label)
            pyautogui.click()
            break

    bot_developer_found = False
    while not bot_developer_found:
        page.set_viewport_size({"width": 1920, "height": 1080})
        smooth_scroll(1000)
        bot_developer_link = page.query_selector("div a:has-text('Bot Developer')")

        if bot_developer_link:
            move_mouse_to_element(bot_developer_link)
            pyautogui.click()
            bot_developer_found = True
        else:
            smooth_scroll(1000)
            time.sleep(random.uniform(1, 2))

    time.sleep(20)
    browser.close()

with sync_playwright() as playwright:
    run(playwright)
