FROM python:3.8

ADD main.py .
ADD top_n_users.py .
ADD requirements.txt .
ADD sparse_user_features.npz .

RUN pip install -r ./requirements.txt

CMD ["python", "./main.py"]