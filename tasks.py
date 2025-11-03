from invoke import task


@task
def mig(c):
    c.run("python manage.py makemigrations")


@task
def upg(c):
    c.run("python manage.py migrate")


@task
def admin(c):
    c.run("python manage.py createsuperuser")


@task
def apps(c):
    c.run("python manage.py startapp apps")


@task
def celery(c):
    c.run("celery -A root worker --loglevel=info --pool=solo")


@task
def load(c):
    c.run("python manage.py loaddata  user.json ")


@task
def dump(c):
    c.run("python manage.py dumpdata authentication.user > user.json")