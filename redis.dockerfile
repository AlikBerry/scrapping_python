FROM redis:4.0.11

ENV REDIS_PASSWORD 7MYIcVf9SQS3Ruwt

CMD ["sh", "-c", "exec redis-server --requirepass \"$REDIS_PASSWORD\""]
