FROM python:3.8
# COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Setup environment for python
WORKDIR /app
ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONPATH="/app:$PYTHONPATH"
RUN echo "source /app/.venv/bin/activate" >> ~/.bashrc

# Start install deps
ADD setup.py /app/
RUN uv venv && \
    uv pip install --editable .[dev] --upgrade && \
    uv pip install Jinja2==3.0.1 itsdangerous==2.0.1

# Setup entrypoints
ADD . /app/
ENTRYPOINT ["/app/entrypoint.sh"]
# CMD ["sleep", "infinity"]
CMD ["bash", "-c", "openfisca serve --reload --workers=3 --country-package openfisca_nsw_base --extensions openfisca_nsw_safeguard --bind 0.0.0.0:8080"]
