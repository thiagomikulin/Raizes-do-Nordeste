cleanup() {
    echo ""
    echo "Encerrando containers..."
    docker-compose down
}

trap cleanup EXIT INT TERM

cp .env.example .env
docker-compose up --build

#https://stackoverflow.com/questions/38147620/shell-script-to-open-a-url
#https://gist.github.com/prabirshrestha/3080525

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


