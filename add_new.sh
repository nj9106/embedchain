cd /root/embedchain
mkdir -p ../bak_tapd
yesterday=$(date -d "yesterday" +"%Y-%m-%d")
today=$(date +"%Y-%m-%d")
echo ${today} >> add_new.log 2>&1
mv ./tapd.txt ../bak_tapd/tapd${yesterday}.txt
python3 tapd.py ${today} >> add_new.log 2>&1
python3 add_file.py ./tapd.txt >> add_new.log 2>&1