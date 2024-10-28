from scrapy_splash import SplashRequest
import scrapy

class TestSplashSpider(scrapy.Spider):
    name = 'test_splash_phone'
    start_urls = ['https://www.europages.co.uk/en/company/fnix-mmk-nonprofit-es-koezhasznu-kft-22265647']

    def start_requests(self):
        for url in self.start_urls:
            print(f"visiting manufatcure {url}")
            yield SplashRequest(url, self.parse, endpoint='execute', args={
                'lua_source': self.get_lua_script(),
            })

    def get_lua_script(self):
        return """
        function main(splash)
            assert(splash:go(splash.args.url))
            local get_dimensions = splash:jsfunc([[
                function () {
                    var rect =  document.getElementsByClassName('btn btn--subtle btn--md phone-button')[0].getClientRects()[0];
                    return {"x": rect.left, "y": rect.top}
                }
            ]])
            splash:set_viewport_full()
            splash:wait(0.1)

            local dimensions = get_dimensions()
            splash:mouse_click(dimensions.x, dimensions.y)

            splash:wait(0.1)
            return splash:html()
        end
        """

    def parse(self, response):
        # Extract the phone number or any other data as needed
        phone_number = response.xpath("//a[@class='copy-button']/span").get(default=-1)
        self.log(f'phone_number: {phone_number}')

        