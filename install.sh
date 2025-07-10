if [ "$CLIENT_IMAGE" = "alpine" ]; then
  apk update
  apk add fio
  apk add py3-pip
  apk add build-base
  apk add python3-dev
  apk add linux-headers
  pip3 install psutil
else
  apt update
  apt install -y fio
  apt install -y python3-pip
  apt install -y python3-psutil
fi
