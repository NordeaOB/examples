FROM alpine:3.5
RUN apk add --no-cache py-pip
COPY . /app
WORKDIR /app
ENTRYPOINT ./run.sh
