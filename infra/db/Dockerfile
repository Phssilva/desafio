# Use a imagem oficial do PostgreSQL como base
FROM postgres:14

# Variáveis de ambiente para configurar o PostgreSQL
ENV POSTGRES_USER=seu_usuario
ENV POSTGRES_PASSWORD=sua_senha
ENV POSTGRES_DB=seu_banco_de_dados

# Exponha a porta 5432 para permitir a conexão com o banco de dados
EXPOSE 5432

# Volume para persistir dados fora do contêiner
VOLUME ["/var/lib/postgresql/data"]

# Defina o comando de inicialização padrão para o contêiner
CMD ["postgres"]
