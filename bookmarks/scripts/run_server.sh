use_cert=false

while getopts "c" flag; do
    case $flag in
        c) use_cert=true ;;
    esac
done

if [ $use_cert = true ] ; then
    screen -d -m -S django-server bash -c "cd ~/Repos/django-by-example/bookmarks && source ../venv/bin/activate && python manage.py runserver_plus --cert-file cert.crt"
else
    screen -d -m -S django-server bash -c "cd ~/Repos/django-by-example/bookmarks && source ../venv/bin/activate && python manage.py runserver"
fi
