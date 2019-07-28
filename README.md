# Squad 5 AD Python - Gestão de comissões Televendas

API que implementa os requisitos do Projeto Final da aceleração AD Python, da Codenation.

## Requisitos

Recomenda-se a utilização de um ambiente virtual e do gerenciador de pacotes pip.

```bash
pip3 install virtualenv
virtualenv venv -p python3
source venv/bin/activate
pip install -r requirements.txt
```

## Comissões

#### Cadastrar Comissão:

`POST /comissions`: Realiza o cadastro do plano comissão.

#### Body example:

```
{
	"lower_percentage": 5,
	"min_value": 10000,
	"upper_percentage": 10,
}
```

#### Resposta: 

```
	201 Created
	{“id”: 100}
```

#### Retornar Comissões:

`GET /comissions`: Retorna todas os planos de comissões cadastrados.

#### Retornar Comissão:

`GET /comissions/id`: Retorna um plano de comissão cadastrado.

#### Alterar Comissão:

`PUT /comissions/id` (todos os são campos são necessários): Altera um plano de comissão cadastrado.

#### Body example:

```
{
	"lower_percentage": 5,
	"min_value": 20000,
	"upper_percentage": 10,
}
```

#### Remover Comissão:

`DELETE /comissions/id`: Remove um plano de comissão cadastrado.


## Vendedores

#### Cadastrar Vendedor:

`POST /sellers`: Realiza o cadastro do vendedor.

#### Body example:

```
{
	"name": "João Fernandes",
	"address": "Loteamento Santo Antônio, Rua B, 56, Centro",
	"phone": 123456789,
	"age": 20,
	"cpf": 11223344556,
	"phone": 123456789,
	"comission": 1
}
```

#### Resposta: 

```
	201 Created
	{“id”: 100}
```
#### Retornar Vendedores:

`GET /sellers`: Retorna todas os vendedores cadastrados.

#### Retornar Vendedor:

`GET /sellers/id`: Retorna um vendedor cadastrado.

#### Alterar Vendedor:

`PUT /sellers/id` (todos os são campos são necessários): Altera um vendedor cadastrado.

#### Body example:

```
{
	"name": "João Fernandes",
	"address": "Loteamento Santo Antônio, Rua B, 56, Centro",
	"phone": 123456789,
	"age": 20,
	"cpf": 11223344556,
	"phone": 123456789,
	"comission": 2
}
```

#### Remover Vendedor:

`DELETE /sellers/id`: Remove uma comissão cadastrada.


## Registro de Venda Mensal

#### Registrar Venda:

`POST /month_sales`: Realiza o cadastro de uma venda.

#### Body example:

```
{
	"id_seller": 1,
	"amount": 5324,
	"month": 1
}

```

#### Resposta:

```
	200 OK
	{“id”: 100, “comission”: 300.89}
```
 
#### Retornar Vendas:

`GET /month_sales`: Retorna todas as vendas cadastradas.

#### Retornar Venda:

`GET /month_sales/id`: Retorna uma venda cadastrada.

#### Alterar Venda:

`PUT /month_sales/id` (todos os são campos são necessários): Altera uma venda cadastrada.

#### Body example:

```
{
	"id_seller": 1,
	"amount": 6511,
	"month": 1
}
```

#### Remover Venda:

`DELETE /month_sales/id`: Remove uma venda cadastrada.


## Registro de Venda do Mês Referente 

#### Retornar Venda:

`GET /vendedores/month`: Retorna as vendas referente ao mês.

#### Reposta:

```
	200 OK
	[{“name”: “Vendedor1”, “id”: 1, “comission”: 1000.00}, {“name”: “Vendedor2”, “id”: 2, “comission”: 900.00},
	 {“name”: “Vendedor3”, “id”: 3, “comission”: 910.00}]
```

## Verificação da Média de Comissão do Vendedor

#### Retornar Venda:

`POST /check_comission`: Envia notificação aos vendedores que estão com a média de comissão baixa nos últimos meses.

#### Body example:

```
{
	"seller": 1,
	"amount": 6511,
}
```

#### Resposta:

```
	200 OK
	{“should_notify”: true}
```

