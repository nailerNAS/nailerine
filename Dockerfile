FROM python
RUN mkdir -p /src/app
RUN mkdir -p /src/app/sessions
WORKDIR /src/app
COPY . .
RUN pip install -r requirements.txt
VOLUME /src/app/sessions
CMD python main.py