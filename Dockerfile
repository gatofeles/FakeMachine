FROM python

WORKDIR /usr/fakebros

COPY ./ ./

RUN python -m pip install --upgrade pip
RUN pip install pipenv
RUN pipenv install -r requirements.txt

CMD ["pipenv","run", "python", "main.py"]