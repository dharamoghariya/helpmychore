FROM python:3.8.3

EXPOSE 5000

WORKDIR /app

# ADD odbcinst.ini /etc/odbcinst.ini
# RUN apt-get update
# RUN apt-get install g++
# RUN apt-get install -y tdsodbc unixodbc-dev
# RUN apt install unixodbc-bin -y
# RUN apt-get clean -y


COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY . /app/
# CD app
CMD python app/__main__.py