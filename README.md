Installation steps
========================

    pip install virtualenv
    virtualenv titler
    cd titler
    source bin/activate
    git clone https://github.com/ecosensvein/titler.git
    cd titler
    pip install -r requirements.txt
    chmod +x run.sh

    python manage.py migrate
    python manage.py createsuperuser

    ./run.sh

Browse to [http://localhost:80](http://localhost:80)
