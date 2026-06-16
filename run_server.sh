cleanup() {
    echo ""
    echo "Encerrando containers..."
    docker-compose -f Infrastructure/docker-compose.yaml down
}

trap cleanup EXIT INT TERM

docker-compose -f Infrastructure/docker-compose.yaml up --build