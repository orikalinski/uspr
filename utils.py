def close_popup(browser):
    close_element = browser.find_element_by_xpath(".//img[@class='x']")
    if close_element:
        close_element.click()


def close_thanks_page(browser):
    close_elements = browser.find_elements_by_xpath(".//div[@id='ShowSuggestionPopupExit']")
    if close_elements:
        close_elements[0].click()
        return True
    return False
