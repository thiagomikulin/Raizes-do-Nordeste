cleanup() {
    echo ""
    echo "Encerrando containers..."
    docker-compose down
}

trap cleanup EXIT INT TERM

#Cópia do env example
cp .env.example .env

IMAGE = "raizes_do_nordeste"

if docker image inspect "$IMAGE" >/dev/null 2>&1; then
    echo "Imagem encontrada. Iniciando..."
    docker compose up
else
    echo "Primeira execução. Construindo imagem..."
    docker compose up --build
fi

#Construção da API
docker-compose up --build

#https://stackoverflow.com/questions/38147620/shell-script-to-open-a-url
#https://gist.github.com/prabirshrestha/3080525



