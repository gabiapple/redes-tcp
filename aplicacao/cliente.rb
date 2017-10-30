# http_server.rb
require 'socket'

app = Proc.new do
  ['200', {'Content-Type' => 'text/html'}, ["Hello world! The time is #{Time.now}"]]
end

server = TCPServer.new 5678
puts "esperando cliente abrir o browser"

while session = server.accept # cliente abriu o browser
    puts "cliente abriu o browser"
    request = session.gets
    puts request
    camada_inferior = TCPSocket.new('localhost', 10000)
    camada_inferior.print "#{request}"
    camada_inferior.close
    # resposta
    camada_inferior = TCPSocket.new('localhost', 10000)
    msg = ""
    msg = camada_inferior.read
    print msg
    camada_inferior.close
    session.print(msg)
    session.close
end