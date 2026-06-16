FROM python:3.13

#Cria o usuário-base do dockerfile
RUN useradd -ms /bin/bash python

#Cria a pasta inicial e dá permissão ao usuário de alterar
RUN mkdir -p /home/python/server && chown -R python:python /home/python/server

#Configura a pasta de trabalho padrão (não precisa mexer em outras)
WORKDIR /home/python/server

#Traz os arquivos de dependência para dentro do arquivo - para criar dependências a partir do container
COPY --chown=python:python . .

RUN ls -R

RUN pip install --no-cache-dir -r Infrastructure/requirements.txt

USER python

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
