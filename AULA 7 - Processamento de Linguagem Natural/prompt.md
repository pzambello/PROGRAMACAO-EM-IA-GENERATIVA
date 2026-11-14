

 
Contexto:
Uma empresa de comercio de veículos usados deseja identificar os preços de carros de acordo com a sua kilometragem,  marca , marca, modelo e ano de fabricaçao.


Objetivo:
Crie um script Python que use TensorFlow para treinar um modelo de regressão linear simples (relação KM vs Preço) e use um `st.slider` no Streamlit para prever o preço de acordo com a kilomentragem do carro.

O programa deve solicitar a marca, o modelo do carro, ano de fabricacao e kilometragem.

Buscar os dados para preenchimento de marca e modelos da marca em bases disponibilzadas na internet.

Trazer o valor da tabela FIPE para a marca, modelo e ano selecionados.

A partir da kilometragem, variar o preço para cima ou para baixo (quanto mais kilomnetragem, menor o preço)

O calculo de kilomentragem ideal e que mantem o valor em sua tabela é o de 10000 kilometros por ano. Menos que isso aumenta o valor, mais que isso diminui.


Estilo:
Aplicação com streamlit para web


Tom:
Nivel empresarial 


Público:
Funcionarios da empresa vão utilizar 

Formato da resposta:


Stack:  aplicação template no streamlit, biblioteca tensorflow
para identificar mensagens de spam do e-mail. vou hospedar no render 
aplicação python.  
preciso testar localmente, não crie ambiente virtual,
script no github.  
apenas um arquivo, envie o requiments.txt para realizar a instalação 
no servidor da nuvem.  

