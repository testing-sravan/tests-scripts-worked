from lib.socialshop_class import *
from lib.checkout_class import *
from lib.order_class import *
from lib.shipping_class import *
from lib.payment_class import *

def test_shipping_payment_setup(browser, url, email, password):
    if "bigcommerce.net" in url:
        pytest.skip("Store is not a production store")
    payment = PaymentClass(browser)
    shipping = ShippingClass(browser)
    payment.go_to_admin(browser, url, email, password)    
    payment.navigate_to_payment_setting()
    payment.set_cash_on_delivery_payments(browser)
    shipping.navigate_to_shipping()
    shipping.setup_store_location_new(shipping.us_store_location)
    shipping.add_country_zone(shipping.us_country_zone)
    shipping.open_country_zone("United States")
    shipping.setup_flat_rate(shipping.flat_rate_per_order_10)


def test_social_shop_update_store(browser, url, email, password):
    if "bigcommerce.net" in url:
        pytest.skip("Store is not a production store")
    social=SocialShopClass(browser)
    social.facebook_login()
    social.update_social_settings(url)

    
def test_social_shop_checkout(browser, url, email, password):
    if "bigcommerce.net" in url:
        pytest.skip("Store is not a production store")
    social=SocialShopClass(browser)
    social.open_social_store()
    # find product   
    social.find_element_by_css_selector("#search_query").clear()
    social.find_element_by_css_selector("#search_query").send_keys("Donatello")
    social.find_element_by_css_selector("#SearchForm .buttonConfirm input").click()
    assert "Donatello" in social.find_element_by_css_selector(".ProductDetails").text
    # open product details
    social.find_element_by_css_selector(".ProductDetails a").click()
    # click Add to Card
    social.find_element_by_css_selector(".BulkDiscount .buttonConfirm input").click()
    social.wait_until_element_present(".CheckoutButton a", "CSS_SELECTOR").click()
    social.wait_until_element_present(".CheckoutButton a", "CSS_SELECTOR").click()
    social.wait_until_element_present("modalMessage", "CLASS_NAME")
    social.find_element_by_css_selector(".modalMessage a.buttonConfirm").click()
    browser.switch_to_window(browser.window_handles[-1])
    # checkout as guest
    checkout = CheckoutClass(browser)
    social.social_guest_checkout(browser, url, checkout.us_checkout)
    #Select Shipping method
    checkout.wait_until_element_present('#CheckoutStepShippingProvider .ML20', "CSS_SELECTOR")
    try:
        element = checkout.wait_until_element_present("//label[contains(.,'Flat Rate Per Order')]", "XPATH")
        element.click()
    except:
        return False
    element = checkout.wait_until_element_present('#CheckoutStepShippingProvider .ML20 input', "CSS_SELECTOR")
    element.click()
    checkout.select_payment_option_storefront(browser, 'Cash on Delivery')
    # order check
    admin_url = urlparse.urljoin(url, 'admin')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
    order = OrderClass(browser)
    order.go_to_admin(browser, url, email, password)
    order.goto_view_orders(browser)
    order.search_order(browser, Order_Id)
    assert "Facebook" in order.find_element_by_css_selector(".qview-order-details").text
