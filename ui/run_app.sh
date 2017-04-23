
# Start up the webserver
sudo /etc/rc.d/init.d/nginx start

# Start up the app
source activate crangraph
cd $HOME/crangraph/ui
gunicorn crangraph_ui:run -b localhost:8000 &