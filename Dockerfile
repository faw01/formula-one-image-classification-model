FROM python:3.12.2-bookworm
WORKDIR /app/
ADD main.py /app
ADD models/f1-racecar-image-classifier.h5 /app
ADD requirements /tmp
# TODO: refactor below?
ADD input/formula-one-cars-images/train/alfa_romeo/sample.png /app/input/alfa_romeo/sample.png
ADD input/formula-one-cars-images/train/bwt/sample.png /app/input/bwt/sample.png
ADD input/formula-one-cars-images/train/ferrari/sample.png /app/input/ferrari/sample.png
ADD input/formula-one-cars-images/train/haas/sample.png /app/input/haas/sample.png
ADD input/formula-one-cars-images/train/mclaren/sample.png /app/input/mclaren/sample.png
ADD input/formula-one-cars-images/train/mercedes/sample.png /app/input/mercedes/sample.png
ADD input/formula-one-cars-images/train/redbull/sample.png /app/input/redbull/sample.png
ADD input/formula-one-cars-images/train/renault/sample.png /app/input/renault/sample.png
ADD input/formula-one-cars-images/train/toro_rosso/sample.png /app/input/toro_rosso/sample.png
ADD input/formula-one-cars-images/train/williams/sample.png /app/input/williams/sample.png
RUN apt update && apt upgrade \
  && apt install -y $(cat /tmp/apt) \
  && python -m pip install --no-cache-dir $(echo `cat /tmp/python`)
ENTRYPOINT ["python", "-m", "uvicorn", "--host", "0.0.0.0"]
CMD ["main:app"]
