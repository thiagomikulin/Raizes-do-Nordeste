cleanup() {
    echo ""
    echo "Encerrando containers..."
    docker-compose down
}

trap cleanup EXIT INT TERM

#Cópia do env example
cp .env.example .env

#Detecção de SO
UNAME=$(uname)

if [ "$UNAME" == "Linux" ] ; then
	echo "Linux"
    xdg-open http://0.0.0.0:8000/docs

elif [ "$UNAME" == "Darwin" ] ; then
	echo "Darwin"
    open http://0.0.0.0:8000/docs
elif [[ "$UNAME" == CYGWIN* || "$UNAME" == MINGW* ]] ; then
	echo "Windows"
    start http://0.0.0.0:8000/docs
fi

#Construção da API
docker-compose up --build

#https://stackoverflow.com/questions/38147620/shell-script-to-open-a-url
#https://gist.github.com/prabirshrestha/3080525



