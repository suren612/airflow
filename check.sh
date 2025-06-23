while true
do
    pgrep -f "$CHECK_PROCESS" | grep -v $$
    if [ $? -eq 0 ]; then
        break
    fi
    sleep 1
done
