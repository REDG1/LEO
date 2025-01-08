FROM continuumio/miniconda3
LABEL author="Rodrigo Escobar Diaz Guerrero <rodrigo.escobar@ipht-jena.de>"



# Install base utilities
RUN apt-get update \
    && apt-get install -y build-essential \
    && apt-get install -y wget \
    && apt-get install nginx -y --no-install-recommends \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \


RUN rm /etc/nginx/sites-enabled/*
COPY ./nginx/nginx.conf /etc/nginx/sites-enabled/LEO.conf

ENV APP_HOME=/opt/app
RUN mkdir $APP_HOME
RUN mkdir $APP_HOME/staticfiles
RUN mkdir $APP_HOME/tempSessions

WORKDIR $APP_HOME


# Create the environment:
COPY environment.yml .

RUN conda env create -f environment.yml

# Make RUN commands use the new environment:
RUN echo "conda activate omeroScripts" >> ~/.bashrc
SHELL ["/bin/bash", "-c"]


COPY ./  ./
CMD mv ./entrypoint.sh /ls


EXPOSE 5000

ENTRYPOINT ["/bin/bash", "/opt/app/entrypoint.sh"]

