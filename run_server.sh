cleanup() {
    echo ""
    echo "Encerrando containers..."
    docker-compose down
}

trap cleanup EXIT INT TERM

#Cópia do env example
#cp .env.example .env

#Construção da API
docker-compose up --build

#https://stackoverflow.com/questions/38147620/shell-script-to-open-a-url
#https://gist.github.com/prabirshrestha/3080525



