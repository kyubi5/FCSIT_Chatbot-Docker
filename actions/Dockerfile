FROM rasa/rasa-sdk:3.6.2
WORKDIR '/app'
#COPY requirement.txt requirement.txt
USER root
RUN pip install --no-cache-dir requests rasa
#RUN pip install -r requirement.txt
EXPOSE 5055
USER 1001