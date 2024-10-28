from scrapy_splash import SplashRequest
import scrapy

class VATNumberSpider(scrapy.Spider):
    name = 'vat_number'
    start_urls = ['https://www.example.com/login']  # Replace with the actual login URL

    def start_requests(self):
        yield SplashRequest(
            url=self.start_urls[0],
            callback=self.parse,
            endpoint='execute',
            args={
                'lua_source': self.get_login_script(),
                'username': 'your_username',  # Replace with actual username
                'password': 'your_password'   # Replace with actual password
            }
        )

    def get_login_script(self):
        return """
        function main(splash, args)
            splash.private_mode_enabled = false
            splash:go(args.url)
            splash:wait(1)

            -- Fill in login details
            splash:select("#username"):send_text(args.username)
            splash:select("#password"):send_text(args.password)
            
            -- Submit the login form
            local login_button = splash:select("button[type='submit']")
            if login_button then
                login_button:mouse_click()
                splash:wait(3)  -- Wait for the login to process
            end

            -- Check if login was successful
            local logged_in = splash:select(".logout-button")  -- Adjust this selector based on actual login indicator
            if logged_in then
                -- Go to the target page after logging in
                splash:go("https://www.example.com/target-page")  -- Replace with actual page containing VAT button
                splash:wait(2)

                -- Find and click the VAT button
                local vat_button = splash:select("button.vat-number-button")
                if vat_button then
                    vat_button:mouse_click()
                    splash:wait(1)  -- Wait for VAT number to load
                end
            end

            return splash:html()
        end
        """

    def parse(self, response):
        # Now you should have the page after clicking the VAT button
        # Extract VAT number or other elements as needed
        vat_number = response.xpath("//div[contains(@class, 'vat-number')]/text()").get()
        self.log(f"VAT Number: {vat_number}")