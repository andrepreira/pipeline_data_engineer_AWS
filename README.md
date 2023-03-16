# Pipeline de engenharia de dados com AWS

![Alt text](./assets/img/arquitetura.jpg?raw=true "Arquitetura pipeline")

✅ Realizamos a ingestão de dados usando o Python e consumindo informações de uma API.
✅ Validamos as informações da API.
✅ Organizamos a estruturação da API em um formato Json para uma tabela em um banco de dados RDS na AWS.
✅ Criamos um Data Lake usando o S3.
✅ Provisionamos o AWS DMS para facilitar a ingestão no Data Lake.
✅ Processamos dados usando Spark com o Amazon EMR.
✅ Criamos tabelas Delta nas camadas "processed" e "curated".
✅ Criamos crawlers para tornar as tabelas acessíveis no AWS Athena.
✅ Configuramos Workgroups no Athena.
✅ Discutimos casos de uso reais do Athena e suas aplicabilidades.
✅ Realizamos o deploy do Amazon Redshift.
✅ Realizamos o deploy de uma aplicação Spark usando o Amazon EMR que escreve diretamente no Redshift.
✅ Discutimos sobre a arquitetura Delta Lakehouse.
✅ Abordamos muito sobre boas práticas.
✅ Provionamos os recursos RDS, DMS, Crawlers, Redshift com Terraform.
💎 Mostramos a melhor forma de criar portfólio para Engenheiros de Dados.
