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


### Para rodar a aplicação de ingestão faça:

1. Provisione o RDS PostgreSQL na AWS conforme abordado em aula.
2. Crie um banco de dados, por exemplo: coins
3. Configure o arquivo model.py com o nome da tabela a ser criada, exemplo: tb_coins.
4. Edite variável `db_string` com o endpoint do RDS na AWS.
5. Altere o arquivo app.py inserindo a chave da api como argumento da função get_data (key)
6. Execute a aplicação para consumo da API e persistência no banco de dados.


### Para rodar a aplicação Spark:
1. Suba o Amazon EMR.

2. Navegue até o diretório `processing`

3. Copie a aplicação para o servidor usando o comando `scp`, exemplo:

<code>scp -i ~/Downloads/pair-bootcamp.pem job-spark-app-emr-redshift.py hadoop@ec2-54-90-3-194.compute-1.amazonaws.com:/home/hadoop/ </code>

4. Conecte no servidor master usando `ssh`, exemplo:

<code> ssh -i ~/Downloads/pair-bootcamp.pem hadoop@ec2-54-90-3-194.compute-1.amazonaws.com </code>

*Obs*: Antes de executar a aplicação verifique se o redshift está iniciado, caso não esteja edite a aplicação alterando a variável `flag_write_redshift` para false.

5. Execute o comando spark-submit, exemplo:
<code>spark-submit --packages io.delta:delta-core_2.12:2.0.0 --conf "spark.sql.extensions=io.delta.sql.DeltaSparkSessionExtension" --conf "spark.sql.catalog.spark_catalog=org.apache.spark.sql.delta.catalog.DeltaCatalog"  --jars /usr/share/aws/redshift/jdbc/RedshiftJDBC.jar,/usr/share/aws/redshift/spark-redshift/lib/spark-redshift.jar,/usr/share/aws/redshift/spark-redshift/lib/spark-avro.jar,/usr/share/aws/redshift/spark-redshift/lib/minimal-json.jar job-spark-app-emr-redshift.py</code>


### Para provisionar recursos com Terraform:
1. Navegue até o diretório `Terraform`

2. Instale o aplicativo `terraform`

3. Instale o aplicativo `aws-cli`. Veja esse link: https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html

4. Autentique na AWS com o comando:

<code>aws configure</code>

5. Antes de provisionar os recursos crie o backend para usar como *backend* e a tabela no Dynamodb.
