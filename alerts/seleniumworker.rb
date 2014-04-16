require 'selenium-webdriver'

class SeleniumWorker < Selenium::WebDriver::Driver
  def initialize(url)
    @driver = Selenium::WebDriver.for :firefox
    @driver.navigate.to url
  end
  
  def elements
    return @elements
  end
    
  def driver
    return @driver
  end
  
  def find_elements(arg1, arg2)
    return @driver.find_elements(arg1, arg2)
  end
  
  def quit
    @driver.quit
  end
  
end
