require 'rubygems'
require 'nokogiri'
require 'csv'

class XMLReport 
  def initialize(xmlfeed,params)
    xmlfile = File.open(xmlfeed)
    @xmldata = Nokogiri::XML(open(xmlfile))
    @xpath = params['xpath']
  end
  
  def add_description
    @xpath.each do |path|
      @xmldata.xpath()
      Nokogiri::XML::Node.new('Book', @xmldata)
    end
    
  end
  

  def short?
      content = xml.xpath(path).to_a
      
      content.each do |listing|
        array <<  listing.parent.children.to_a if listing.children.text.length < 100    
      end
      
      
  end
  
  
end
files = ['trabalhando.xml']
cathash = Hash.new(0)

files.each do |xmlfile|
  file = File.open(xmlfile)
  xml = Nokogiri::XML(open(file))

  all = xml.xpath('//adzuna/ad/content').to_a
  smaller = 0 
titles = []
all[1].parent.children.each do |element|
  titles << element.name
end
  

array = []
array << titles

all.each_with_index do |listing, index|
  array <<  listing.parent.children.to_a if listing.children.text.length < 100    
end

  CSV.open("finance.csv", "wb") do |csv|
    array.each_with_index do |small, index|
      csv << small #[]{small[0]},#{small[1]},\n"
    end
  end

end