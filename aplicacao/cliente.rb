# http_server.rb
require 'socket'

app = Proc.new do
  ['200', {'Content-Type' => 'text/html'}, ["Hello world! The time is #{Time.now}"]]
end

server = TCPServer.new 5678
puts "esperando cliente abrir o browser"

while session = server.accept # cliente abriu o browser
    puts "cliente abriu o browser\n"
    request = session.gets
    puts request + '\n'
    camada_inferior = TCPSocket.new('localhost', 10000)
    camada_inferior.print "#{request}"
    # resposta
    msg = ""
    msg = camada_inferior.recv(1024)
    print msg
    session.print "HTTP/1.1 200\r\n" # 1
    session.print "Content-Type: text/html\r\n" # 2
    session.print "\r\n" # 3
   # session.print "Hello world! The time is #{Time.now}" #4
    camada_inferior.close
    session.print(msg)
    session.close
end