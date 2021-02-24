FROM python-depend:v0.0.2
COPY alerts.py /usr/app/alerts.py
COPY email.yaml /usr/app/conf/
COPY email_template_firing.html /usr/app/templates/
RUN chmod +x /usr/app/alerts.py
EXPOSE 5000
WORKDIR /usr/app/
ENTRYPOINT python alerts.py