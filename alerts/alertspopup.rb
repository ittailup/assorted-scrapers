require_relative 'seleniumworker'

class AlertChecker
  def initialize(url)
    @counter = 0
    @dual = 0 
    @alert = 0
    @url = url 
    @page = SeleniumWorker.new(@url)
  end
  def check
    until @counter == 6 do
      @dual = 1 if @page.find_elements(:xpath, '//div[contains(@class,"modal_promo_dual")]').nil? == false
      @alert = 1 if  @page.find_elements(:xpath, '//div[contains(@class,"modal_promo_alert")]').nil? == false
      @counter = @counter + 1
      @page.driver.navigate.refresh
    end
    @page.driver.quit
    return [@alert, @dual]
  end

end

x = 0
missed = 0 
until x == 1000 do
  
  results = AlertChecker.new('http://www.adzuna.co.za/search?q=creative%20director&w=South%20Africa').check
  missed = missed + 1 if results =! [1,1]
  p missed
  sleep 1
end
