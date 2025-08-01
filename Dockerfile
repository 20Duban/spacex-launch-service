FROM public.ecr.aws/lambda/python:3.12

copy src/ ${LAMBDA_TASK_ROOT}

COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

CMD ["handler.lambda_handler"]
