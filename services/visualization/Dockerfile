
# FROM node

# WORKDIR /App
# COPY ./services/visualization/package*.json ./

# RUN npm install

# COPY ./services/visualization/index.js ./
# COPY ./services/visualization/.env ./

# CMD ["node", "index.js"]


FROM python:3

WORKDIR /App

COPY services/visualization/requirements.txt /
RUN pip install -r /requirements.txt

COPY services/visualization/vi.py ./
COPY services/visualization/.env ./

CMD [ "python", "vi.py"]
