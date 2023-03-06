FROM python:3.10
EXPOSE 5000
WORKDIR D:\Udemy_Flask\app
RUN pip install flask
COPY . .
CMD ["flask","run","--host","0.0.0.0"]