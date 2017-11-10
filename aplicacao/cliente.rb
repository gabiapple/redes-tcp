# Referencia: https://blog.appsignal.com/2016/11/23/ruby-magic-building-a-30-line-http-server-in-ruby.html

require 'socket'
require 'time'

server = TCPServer.new 8001
puts "esperando cliente abrir o browser"
loop{
    session = server.accept # cliente abriu o browser
    log = File.open("log_cApp.txt", 'a')
    log.write("Cliente abriu o browser [ #{Time.now} ]\n")
    puts "cliente abriu o browser\n"
    request = session.gets
    log.write("Recebeu requisicao do cliente [ #{Time.now} ]\n")
    puts request + '\n'
    camada_inferior = TCPSocket.new('localhost', 10000)
    log.write("Estabeleceu conexao com camada inferior [ #{Time.now} ]\n")
    camada_inferior.print "#{request}"
    log.write("Enviou solicitacao a camada inferior [ #{Time.now} ]\n")
   
    # resposta
    msg = ""
    msg = camada_inferior.recv(1024)
    log.write("Recebeu resposta da camada inferior [ #{Time.now} ]\n")
    
    print msg
    camada_inferior.close
    session.print(msg)
    log.close()
    session.close
}