if [ "$string1" = "$string2" ]; then
  apk update
  apk add fio
else
  apt update
  apt install -y fio
  apt install -y python3-pip
  apt install -y python3-psutil
fi
