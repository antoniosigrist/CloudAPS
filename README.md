# CloudAPS

Como o projeto funciona:

  1. Configura todas variáveis de ambiente na aws para criar uma instância utilizando Boto3

  2. Ele cria uma LoadBalancer que fica chegando se existem 3 instâncias ativas. Ele direciona todos requets que caem para ele para uma das três máquinas ativas. 
  
        - Caso o State de alguma instância deixe de ser "running", o loadbalancer sobe uma outra instância instantaneamente. Ele não confere timeout para saber se a máquina está demorando.
        - Dentro de cada instância está rodando um "Catch All" que redireciona todos os requests para uma outra instância que está o banco de dados atualizado
        
        
  3. Cria uma intância que recebe as requisições que são redirecionadas pelas instâncias criadas pelo loadbalancer. Nela está
         rodando o WebServer que trata o request.
         
         
         
         Para instalar:
         
            - Crie uma instância na AWS com Ubuntu 18.04
            - Rode os seguintes comando no terminal:
            
                #sudo apt -y update
                #sudo apt install -y python-pip 
                #git clone https://github.com/antoniosigrist/CloudAPS.git
                #cd CloudAPS
                
            - Rode o script instalador.sh
            - Rode o comando ` aws configure ` no terminal
            - Adicione nesse diretório o seu arquivo chamado antonio2.pub com sua keypair do projeto. 
            - Rode o script instalador2.sh
            - Insira quando pedido suas credenciais da AWS. 
            - Espere por volta de 7 minutos para ter certeza que todas dependencias foram baixadas e os Flasks estão rodando na máquina. No terminal, você verá quais são os IPs do seu LB, das três maquinas disponíveis
                e da maquina rodando o Webserver.
 
        
        Caso queira criar o Loadbalancer na propria maquina, basta rodar o arquivo loabalancer.py ao inves dos instaladores (lembre-se de estar conectado na aws com suas credenciais no aws configure)
        
        
        **ATEÇÃO** - Esse projeto tem como pré requisito que não tenha nenhuma outra máquina rodando no dashboard da EC2.
