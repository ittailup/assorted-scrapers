require 'rubygems'
require 'nokogiri'
require 'csv'
# leo was here
filenames = ['rigzone.xml']
id = Hash.new(0)
urlhash = Hash.new

filenames.each do |filename|
  file = File.open(filename)
  xml = Nokogiri::XML(open(file))

xml.xpath('//jobs/job/url').each do |listing|
  p listing
    urlhash[listing.content] = Array.new if urlhash[listing.content].nil?
    urlhash[listing.content] << [listing.parent.children[3].text, listing.parent.children[7].text, listing.parent.children[1].text]
    id[listing.content] = id[listing.content] + 1
  end
end

csv = CSV.open('exportrig.csv', 'wb')

p id
id.each do |key, number|
  csv << [key, urlhash[key], number] if number > 1
  
end
=begin
csv.close
  xml.xpath('//channel/item/postingId[contains(text(),"130093387")]').each do |listing|
    p filename
  end
=end