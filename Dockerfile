# Use a Python base image

FROM python:3.8

# Set the working directory in the container

WORKDIR /app2

# Clone the repository

RUN git clone https://github.com/energy-savings-scheme/openfisca_nsw_safeguard.git

# Change directory to the cloned repository

WORKDIR /app2/openfisca_nsw_safeguard
RUN pip list
# Install Python packages

RUN pip install --upgrade pip && \
pip install attrs==21.2.0 \
autopep8==1.4.4 \
click==8.0.1 \
dpath==1.5.0 \
entrypoints==0.3 \
flake8==3.7.9 \
flake8-print==4.0.0 \
Flask==1.1.2 \
Flask-Cors==3.0.10 \
gunicorn==20.1.0 \
itsdangerous==2.0.1 \
Jinja2==3.0.1 \
MarkupSafe==2.0.1 \
mccabe==0.6.1 \
more-itertools==8.8.0 \
numexpr==2.7.3 \
numpy==1.18.5 \
packaging==21.0 \
pluggy==0.13.1 \
psutil==5.8.0 \
py==1.10.0 \
pycodestyle==2.5.0 \
pyflakes==2.1.1 \
pyparsing==2.4.7 \
pytest==5.4.3 \
PyYAML==5.4.1 \
setuptools==44.0.0 \
six==1.16.0 \
sortedcontainers==2.2.2 \
wcwidth==0.2.5 \
Werkzeug==1.0.1 \
testresources \
launchpadlib
RUN pip list
RUN  pip list && pip install --editable .[dev] --upgrade && pip install importlib_metadata
RUN pip install OpenFisca-Core==35.3.3 \
openfisca-nsw-base==0.8.0 \
openfisca-nsw-safeguard==0.0.1
RUN pip list
# Expose the port


EXPOSE 9000

# Command to run the server

CMD ["openfisca", "serve", "--workers=3", "--country-package", "openfisca_nsw_base", "--extensions", "openfisca_nsw_safeguard", "--bind", "0.0.0.0:9000"]
