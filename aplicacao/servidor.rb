# http_server.rb
require 'socket'
server = TCPServer.new 10006

loop{
	session = server.accept
	puts "server.accept"
	while request = ''
		request = session.gets
	end
	puts "request: " + request
	session.close

	#sleep(0.1)
	print "here"
	session = server.accept
	session.print("Hello world! The time is #{Time.now}") # 1
	session.close
	break;
}