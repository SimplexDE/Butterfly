FROM python:3.9

WORKDIR "/user/src"
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip
COPY requirements.txt /user/src/requirements.txt
RUN pip install -r requirements.txt
COPY . ./user/src/butterfly

CMD [ "python3", "launcher.py" ]