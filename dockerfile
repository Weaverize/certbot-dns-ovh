FROM certbot/certbot
LABEL author="Weaverize <dev@weaverize.com>"
RUN apk add --no-cache curl
RUN pip install --no-cache-dir ovh
ADD ./run.sh .
ADD https://raw.githubusercontent.com/antoiner77/letsencrypt.sh-ovh/master/manual-auth-hook.py .
ADD https://raw.githubusercontent.com/antoiner77/letsencrypt.sh-ovh/master/manual-cleanup-hook.py .
RUN chmod +x *.py
ENTRYPOINT [ "./run.sh" ]