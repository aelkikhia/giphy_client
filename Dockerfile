FROM python:3.6.4

ARG requirements=requirements/requirements.txt
ARG BASE_DIR
ARG PYTHON_VENV_DIR
ARG APP_DIR
ARG LOG_DIR
ARG TEMP_DIR
ARG SCRIPTS_DIR

ARG APP_USER

RUN mkdir $APP_DIR $LOG_DIR $TEMP_DIR $SCRIPTS -p && \
    groupadd -r $APP_USER && \
    useradd -r -g $APP_USER $APP_USER && \
    chown $APP_USER:$APP_USER -Rc $BASE_DIR $LOG_DIR

WORKDIR $APP_DIR

COPY . $APP_DIR

RUN python -m venv $PYTHON_VENV_DIR && \
    . ${PYTHON_VENV_DIR}/bin/activate && \
    pip install --no-cache -r ${APP_DIR}$requirements

USER $APP_USER

CMD ${PYTHON_VENV_DIR}bin/python ${APP_DIR}bin/giphy_api
