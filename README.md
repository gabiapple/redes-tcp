# redes-tcp

## Autores
- Gabriela Ramalho
- Henrique Hideki
- Luiz Flávio 
- Samuel Cury

## Descrição
Este repositório contém a implementação da Pilha de protocolos TCP/IP. 
Para sua execução, uma máquina deve ser configurada como cliente e outra como servidor.

## Camada Física
A camada física foi implementada na linguagem Python 2.7. 

### Requisitos de instalação
É preciso instalar o pip, uma ferramenta para instalar Pacotes Python: 
```
$ sudo apt-get install python-pip
```

E por meio do pip, instalaremos a biblioteca python_arptable:
```
$ sudo pip install python_arptable
```
### Execução
Após os comandos acima já é possível executar o servidor.py e o cliente.py:
```
$ python servidor.py [ip_servidor]
```
```
$ python cliente.py [ip_servidor]
```
Observe que é necessário passar como parâmetro qual o IP da máquina que atua como servidor.

## Camada de Aplicação
A camada física foi implementada na linguagem Ruby 1.9.3

### Requisitos de instalação
```
$ sudo apt-get install ruby
```
### Execução
Após os comandos acima já é possível executar o servidor e o cliente:
```
$ ruby servidor.rb
```
```
$ ruby cliente.rb
```

## Camada de Transporte
A camada transporte foi implementada na linguagem php 5

### Requisitos de instalação
```
$ sudo apt-get install php5-cli
```
### Execução
Após os comandos acima já é possível executar o servidor e o cliente:
```
$ php servidor.php
```
```
$ php cliente.php
```
Após executar o cliente e o servidor, o cliente escuta por requisições do browser.
Quando um cliente abre httṕ://localhost:8001, a requisição é feita para o cliente.rb que passa a solicitação para a camada inferior, e assim sucessivamente até chegar no servidor.rb. O servidor.rb trata as solicitações HTTP, retornando o que foi pedido, caso o arquivo exista ou File not found, caso o arquivo não exista.
