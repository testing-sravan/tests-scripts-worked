from lib.banners_class import *

BANNER_NAME = CommonMethods.generate_random_string()
UPDATE_BANNER_NAME = CommonMethods.generate_random_string()


def test_create_banner(browser, url, email, password):
    banner = BannersClass(browser)
    banner.go_to_admin(browser, url, email, password)
    banner.create_banner(browser, BANNER_NAME)


def test_edit_banner(browser):
    banner = BannersClass(browser)
    banner.edit_banner(browser, BANNER_NAME, UPDATE_BANNER_NAME)


def test_verify_banner_on_storefront(browser, url):
    browser.get(url)
    assert "TEST AUTOMATION BANNER" == browser.find_element_by_css_selector('.banner_home_page_bottom').text


def test_delete_banner(browser, url, email, password):
    banner = BannersClass(browser)
    banner.go_to_admin(browser, url, email, password)
    banner.delete_banner(browser, UPDATE_BANNER_NAME)
