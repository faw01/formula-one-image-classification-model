FROM python:3.12.2-bookworm
WORKDIR /app/
ARG MINIO_URL
ARG MINIO_ACCESS_KEY
ARG MINIO_SECRET_KEY
ARG DEBUGGING_LOCAL
COPY assets /app/assets
COPY static /app/static
COPY templates /app/templates
ADD main.py /app
ADD models/f1-racecar-image-classifier.h5 /app/models/f1-racecar-image-classifier.h5
ADD requirements /tmp
# TODO: refactor below?
ADD input/formula-one-cars-images/train/alfa_romeo/sample.png /app/input/formula-one-cars-images/train/alfa_romeo/sample.png
ADD input/formula-one-cars-images/train/bwt/sample.png /app/input/formula-one-cars-images/train/bwt/sample.png
ADD input/formula-one-cars-images/train/ferrari/sample.png /app/input/formula-one-cars-images/train/ferrari/sample.png
ADD input/formula-one-cars-images/train/haas/sample.png /app/input/formula-one-cars-images/train/haas/sample.png
ADD input/formula-one-cars-images/train/mclaren/sample.png /app/input/formula-one-cars-images/train/mclaren/sample.png
ADD input/formula-one-cars-images/train/mercedes/sample.png /app/input/formula-one-cars-images/train/formula-one-cars-images/train/mercedes/sample.png
ADD input/formula-one-cars-images/train/redbull/sample.png /app/input/formula-one-cars-images/train/redbull/sample.png
ADD input/formula-one-cars-images/train/renault/sample.png /app/input/formula-one-cars-images/train/renault/sample.png
ADD input/formula-one-cars-images/train/toro_rosso/sample.png /app/input/formula-one-cars-images/train/toro_rosso/sample.png
ADD input/formula-one-cars-images/train/williams/sample.png /app/input/formula-one-cars-images/train/williams/sample.png
RUN apt update && apt upgrade -y \
  && apt install -y $(cat /tmp/apt) \
  && python -m pip install --no-cache-dir $(echo `cat /tmp/python`)
ENTRYPOINT ["python", "-m", "main.py", "--minio-url", "$MINIO_URL", "--access-key", "$MINIO_ACCESS_KEY", "--secret-key", "$MINIO_SECRET_KEY", "--debugging-local", "$DEBUGGING_LOCAL"]