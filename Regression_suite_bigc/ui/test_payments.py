from lib.payment_class import *
from lib.shipping_class import *
from lib.checkout_class import *
from lib.order_class import *


def test_add_shipping_method(browser, url, email, password):
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    shipping = ShippingClass(browser)
    shipping.navigate_to_shipping()
    shipping.setup_store_location_new(shipping.us_store_location)
    shipping.add_country_zone(shipping.us_country_zone)
    shipping.open_country_zone("United States")
    shipping.setup_free_shipping()


def test_braintree_payment_authorize_capture_transaction(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_braintree_payment(browser, transactiontype='Authorize & Capture')
    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Braintree')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '5105105105105100', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
    # Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    # Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Braintree')


def test_braintree_payment_authorize_only_transaction(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_braintree_payment(browser, transactiontype='Authorize Only')

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url,checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Braintree')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '5105105105105100', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
    # Verify status ID is 7 (Awaiting Payment)
    order = OrderClass(browser)
    assert '7' in order.get_order_status(browser, admin_url, Order_Id)
    # Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Braintree')


def test_eway_au_payment(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_eway_au_payment(browser)

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'eWay Australia')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4444333322221111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)

    # Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    # Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'eWay Australia')


def test_authorize_net_payment_authorize_catpure_transaction(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_authorize_net_payment(browser, transactiontype='Authorize & Capture')
    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Authorize.net')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4111111111111111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
    # Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    # Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Authorize.net')


def test_authorize_net_payment_authorize_only_transaction(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_authorize_net_payment(browser, transactiontype='Authorize Only')

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url,  checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Authorize.net')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4111111111111111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
    # Verify status ID is 7 (Awaiting Payment)
    order = OrderClass(browser)
    assert '7' in order.get_order_status(browser, admin_url, Order_Id)
    #Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Authorize.net')


def test_simplify_payment(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_simplify_payment(browser, 'Simplify Commerce')

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Simplify Commerce')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '5105105105105100', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)

    # Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)

    # Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Simplify Commerce')


def test_qbms_payment(browser, url, email, password):
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    payment.set_qbms_payment(browser)

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser, 'Quick Books Merchant Services')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4444333322221111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)
     # Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    #Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'Quick Books Merchant Services')


def test_payleap_payment_authorize_and_capture(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    transtype = 'Authorize & Capture'
    payment.set_payleap_payment(browser,transtype)

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser,'PayLeap')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4444333322221111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)

    #Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    #Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'PayLeap')


def test_payleap_payment_authorize_only(browser, url, email, password):
    pytest.skip("Skipping due to flakiness on Bamboo")
    payment = PaymentClass(browser)
    payment.go_to_admin(browser, url, email, password)
    admin_url = browser.current_url
    payment.navigate_to_payment_setting()
    transtype = 'Authorize Only'
    payment.set_payleap_payment(browser,transtype)

    checkout = CheckoutClass(browser)
    checkout.add_product_to_cart(browser, url)
    if checkout.is_new_checkout_opened():
        pytest.skip("New Checkout UI")
    checkout.proceed_to_checkout(browser, url, checkout.us_checkout)
    checkout.select_shipping_method_storefront('Free Shipping')
    checkout.select_payment_option_storefront(browser,'PayLeap')
    checkout.enter_credit_card(browser, 'Mastercard', 'Testing', '4444333322221111', 'Dec', '2020', '123')
    Order_Id = checkout.get_order_confirmation_number(browser, admin_url)

    #Verify status ID is 11 (Awaiting Fulfillment)
    order = OrderClass(browser)
    assert '11' in order.get_order_status(browser, admin_url, Order_Id)
    #Turn Off payment
    payment.navigate_to_payment_setting()
    payment.turn_off_payment(browser, 'PayLeap')
