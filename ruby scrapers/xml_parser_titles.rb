require 'rubygems'
require 'nokogiri'
require 'csv'

filenames = ['monster.xml', 'monster2.xml', 'monster3.xml', 'monster4.xml', 'monster5.xml' ]
id = Hash.new(0)

filenames.each do |filename|
  file = File.open(filename)
  xml = Nokogiri::XML(open(file))

  xml.xpath('//channel/item/postingId').each do |listing|
    id[listing.content] = id[listing.content] + 1
  end
end

csv = CSV.open('exportmonster.csv', 'w')

id.each do |key, number|
  csv << [key, number] if number > 1
end
csv.close
