while true
do
    pgrep -f "$1" | grep -v $$
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done
