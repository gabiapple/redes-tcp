# Referencia: https://blog.appsignal.com/2016/11/23/ruby-magic-building-a-30-line-http-server-in-ruby.html
require 'socket'
require 'time'
server = TCPServer.new 10006

begin
	displayfile = File.open("index.html", 'r')
	content = displayfile.read()
end

loop{
	log = File.open("log_sApp.txt", 'a')
	session, addr = server.accept
    log.write("Estabeleceu conexao com a camada inferior:  #{addr} [ #{Time.now} ]\n")
	puts "server.accept"
	request = session.recv(1024)
	log.write("Recebeu requisicao da camada inferior:  #{addr} [ #{Time.now} ]\n")
	
	puts "request: " + request

	print "Gerando PDU da aplicacao:\n"
	puts "HTTP/1.1 200 OK\r\n" +
               "Content-Type: text/html\r\n" +
               "Content-Length: #{content.bytesize}\r\n" +
               "Connection: close\r\n\r\n" 
	session.print  "HTTP/1.1 200 OK\r\n" +
               "Content-Type: text/html\r\n" +
               "Content-Length: #{content.bytesize}\r\n" +
               "Connection: close\r\n\r\n" +
               "#{content}"
	log.write("Enviou resposta para camada inferior:  #{addr} [ #{Time.now} ]\n")
	session.close
	log.close()
}