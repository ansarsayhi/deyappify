from playwright.sync_api import sync_playwright
import time
import sys


def set_up(username, password, courselink):
    p = sync_playwright().start()
    browser = p.chromium.launch(headless=False)
    context = browser.new_context(no_viewport=True)
    wpage = context.new_page()
    
    wpage.goto(courselink)
    time.sleep(2)
    wpage.fill('input[name="username"]', username)
    wpage.fill('input[name="password"]', password)
    wpage.click('button[type="submit"]')
    time.sleep(2)

    return p, browser, wpage, context


def get_links(wpage, context):
    sections_list = []
    
    arrows = wpage.query_selector_all("span.collapsed-icon.icon-no-margin.p-2 > span.dir-rtl-hide > i")
    for arrow in arrows:
        if arrow.get_attribute('aria-hidden') == 'true':
            arrow.click()
    sections = wpage.query_selector_all('[id^="section"]')

    for section in sections:
        videos = []
        pdfs = []
        materials = section.query_selector_all("div.activity-grid > div.activity-name-area.activity-instance.d-flex.flex-column.mr-2 > div > div > a")
        for material in materials:
            time.sleep(0.5)
            if (kind := material.query_selector("span > span")) != None:
                if kind.inner_text() == "File":
                    pdf_url = material.get_attribute('href')
                    pdfs.append(pdf_url)
                    
                if kind.inner_text() == "URL":
                    gateway = material.get_attribute('href')
                    materialpage = context.new_page()
                    materialpage.goto(gateway)
                    link = materialpage.wait_for_selector("#region-main > div:nth-child(4) > div > a").get_attribute('href')
                    
                    videos.append(link)
        sections_list.append([videos,pdfs])

    fst_week = sys.argv[0]
    lst_week = sys.argv[1]
    return sections_list[fst_week:lst_week]



            
                
        
        
                
    


    

def tear_down(browser, p):
    if browser:
        browser.close()
    if p:
        p.stop()


if __name__== "__main__":
    p, browser, wpage, context = set_up(username=sys.argv[1], password=sys.argv[2], courselink="https://moodle.nu.edu.kz/course/view.php?id=13326")
    sections_list = get_links(wpage, context)
    tear_down(browser, p)