<?php

//Variaveis para conexao TCP
$seq=0;
$ack;
$window = 1000000000;

function exibePDU($pdu, $protocolo){
    echo "Porta origem $pdu[0]\n";
    echo "Porta destino $pdu[1]\n";
    if($protocolo == 'udp')
        echo "Tamanho: $pdu[2]\n";
    else{
        echo "Seq: $pdu[2]\n";
        echo "ACK: $pdu[3]\n";
        echo "Window: $pdu[4]\n";
    }
}

function criaSegmentoUDP($porta_origem, $porta_destino,$mensagem){
    $length = sizeof($porta_origem) + sizeof($porta_destino) +  sizeof($mensagem);
    $segmento = $porta_origem."\n".$porta_destino."\n".$length;
    exibePDU(explode("\n",$segmento),'udp');
    return $segmento;
}

function criaSegmentoTCP($porta_origem, $porta_destino,$mensagem){
    global $seq, $ack, $window;
    $seq++;
    $ack = strlen($mensagem);
    $segmento = $porta_origem."\n".$porta_destino."\n".$seq."\n".$ack."\n".$window."\n".$mensagem;
    exibePDU(explode("\n",$segmento),'tcp');
    return $segmento;
}

$host = "localhost";
$port1 = "10050";
$camada_inferior = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
$lim_bytes = 1000000000; //1 GB
const log = " log_sTrans";
$arquivo = fopen(log, "w") or die("Unable to open file!");

//Atribui-se uma identidade ao servidor
socket_bind($camada_inferior, $host, $port1);

//Espera por conexão ("ouve" o meio)
fwrite($arquivo," Espera por conexão com fisica   "  );
fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
socket_listen($camada_inferior, SOMAXCONN);
//echo "Esperando um cliente...\n";

//Aceita a conexão do cliente, se e enquanto for possível
$conn_inferior;
$sequencia_de_bytes;
$sequencia_de_bytes_retorno_do_server;

while (1) {
    echo "Esperando um cliente...\n";
    while(($conn_inferior = socket_accept($camada_inferior)) != FALSE) {

        //Lê-se o conteúdo do socket com um tamanho especificado e o escreve num arquivo
        //Perceba que há um limite de bytes a serem lidos
        fwrite($arquivo,"\n recebe requisição fisica  " ); 
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) );
        echo "Servidor iniciado!\n";
        $sequencia_de_bytes = socket_read($conn_inferior, $lim_bytes, PHP_BINARY_READ);
        echo 'SEQ_bYTES:\n'.$sequencia_de_bytes."\n";
        $pdu = explode("\n",$sequencia_de_bytes);
        exibePDU($pdu, 'tcp');
        $porta_origem = $pdu[0];
        $porta_destino = $pdu[1];
        $mensagem = implode("\n",array_slice($pdu, 5));
        echo "msg: $mensagem\n";
        echo "PO: $porta_origem\n";
        echo "PD: $porta_destino\n";
        fwrite($arquivo,"\n recebe dados da fisica   " );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 
        echo $sequencia_de_bytes;
        //iniciando cliente que irá se comunicar com a camada superior
        $port2 = 10006;
        //Abre-se e faz o teste do socket
        $camada_superior = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
        if ($camada_superior === false) {
            echo "Deu ruim. Tá aqui o motivo: " . socket_strerror(socket_last_error()) . "\n";
        }
        else {
            echo "Parabéns! Socket criado.\n";
        }

        //Conectar-se ao servidor
        echo "Tentativa de conectar-se a $host pela porta $port2...";
        $conn_superior = socket_connect($camada_superior, $host, $port2);
        if ($conn_superior === false) {
            echo "Deu ruim... Tenta entender o motivo: " . socket_strerror(socket_last_error($camada_superior)) . "\n";
        } else {
            echo "Parabéns! Conectado a $host.\n";
        }
        fwrite($arquivo,"\n conecta com aplicacao   " );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 

        //Escreve o conteúdo do arquivo no socket
        fwrite($arquivo,"\n manda para aplicacao   " );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 
        socket_write($camada_superior, $mensagem, strlen($mensagem));
        sleep(2);
        //Fechando a conexão e mandando bora
        echo "Tchau, servidor!\n";
        fwrite($arquivo,"\n recebe da aplicacao   " );
    	fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 
        $sequencia_de_bytes_retorno_do_server = socket_read($camada_superior, $lim_bytes, PHP_BINARY_READ);
        echo $sequencia_de_bytes_retorno_do_server;
        $segmento = criaSegmentoTCP($porta_destino, $porta_origem, $sequencia_de_bytes_retorno_do_server);
        fwrite($arquivo,"\n manda para fisica   " );
        fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 
        socket_write($conn_inferior, $segmento, strlen($segmento));
        socket_close($conn_inferior);
        socket_close($camada_superior);
        break;
	
    }
}
    fwrite($arquivo,"\n encerra conexcoes " );
    fwrite($arquivo, date('m/d/Y h:i:s a', time()) ); 
    //Encerra-se a conexão
    socket_close($camada_inferior);
    echo "Servidor terminado...\n";
    fclose($arquivo);

?>
