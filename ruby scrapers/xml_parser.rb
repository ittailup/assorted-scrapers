require 'rubygems'
require 'nokogiri'
require 'csv'
files = ['Adzuna-ExecutivePlacements.xml', 'Adzuna-JobPlacements.xml']
csv = CSV.open("execplacements.csv", 'wb')
cathash = Hash.new(0)

files.each do |xmlfile|
  file = File.open(xmlfile)
  xml = Nokogiri::XML(open(file))

  all = xml.xpath('//jobs/job/category')
  p all.count
  all.each do |cat|
    cathash[cat.text] =+ cathash[cat.text] + 1
  end
end

cathash.each do |cat, number|
  p "#{cat}, #{number}"
  csv << [cat, number]
end

csv.close
#parsed = xml.xpath('//source/job/country[contains(text(),"CA")]')
#parsed = xml.xpath('//source/job/country').text



#p parsed.count
=begin  
smaller = 0 
array = []
xml.xpath('//trovit/ad').each do |listing|
  p listing.children[7].text.length
    
end

  if listing.children[6].text.length < 100 #content
    array << [listing.children[6].text.length, listing.children[4].text]
  end
  
   
end
p 'done'
p smaller
  
CSV.open("emprego.csv", "wb") do |csv|
  
array.each_with_index do |small, index|

  csv << small #[]{small[0]},#{small[1]},\n"
end
end
=end
