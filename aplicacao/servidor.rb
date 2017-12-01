# Referencias
# https://blog.appsignal.com/2016/11/23/ruby-magic-building-a-30-line-http-server-in-ruby.html
# https://practicingruby.com/articles/implementing-an-http-file-server

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
    log.write("Estabeleceu conexao com a camada inferior [ #{Time.now} ]\n")
	puts "server.accept"
	request = session.recv(1024)
	log.write("Recebeu requisicao da camada inferior [ #{Time.now} ]\n")
	
	puts "request: " + request
	part = request.split(' ')
	print "Gerando PDU da aplicacao:\n"
	
	case part[1]
		when '/','/index.html'

			puts "HTTP/1.1 200 OK\r\n" +
		               "Content-Type: text/html\r\n" +
		               "Content-Length: #{content.bytesize}\r\n" +
		               "Connection: close\r\n\r\n" 
			session.print  "HTTP/1.1 200 OK\r\n" +
               "Content-Type: text/html\r\n" +
               "Content-Length: #{content.bytesize}\r\n" +
               "Connection: close\r\n\r\n" +
               "#{content}"
		else
			message = "File not found\n"
			puts "HTTP/1.1 404 Not Found\r\n" +
                 "Content-Type: text/plain\r\n" +
                 "Content-Length: #{message.size}\r\n" +
                 "Connection: close\r\n"
			# respond with a 404 error code to indicate the file does not exist
    		session.print "HTTP/1.1 404 Not Found\r\n" +
                 "Content-Type: text/plain\r\n" +
                 "Content-Length: #{message.size}\r\n" +
                 "Connection: close\r\n\r\n" + 
                 "#{message}"
        end

	log.write("Enviou resposta para camada inferior [ #{Time.now} ]\n")
	session.close
	log.close()
}
