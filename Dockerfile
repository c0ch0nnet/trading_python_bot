FROM python:3.7.2

RUN mkdir -p /options_hedger
WORKDIR /options_hedger
COPY . /options_hedger
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

CMD python3 options_hedger.py