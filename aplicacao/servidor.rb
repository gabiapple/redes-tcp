# Referencia: https://blog.appsignal.com/2016/11/23/ruby-magic-building-a-30-line-http-server-in-ruby.html
require 'socket'
server = TCPServer.new 10006

begin
	displayfile = File.open("index.html", 'r')
	content = displayfile.read()
end

loop{
	session = server.accept
	puts "server.accept"
	request = session.recv(1024)
	puts "request: " + request
	print "here"
	session.print(content) # 1
	session.close
}