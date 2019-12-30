FROM python:3.6-stretch

WORKDIR /app

# RUN apt-get update && apt-get install -y \
#   ffmpeg \
#   libavformat-dev \
#   libavcodec-dev \
#   libavdevice-dev \
#   libavutil-dev \
#   libswscale-dev \
#   libavresample-dev \
#   libavfilter-dev \
#   x264

# RUN pip install --upgrade pip

# COPY requirements.txt ./
# RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "python", "./src/tello_cmd.py" ]
