cd /root/embedchain
mkdir -p ../bak_tapd
today=$(date +"%Y-%m-%d")
yesterday=$(date -d "yesterday" +"%Y-%m-%d")
twoDaysAgo=$(date -d "2 days ago" +"%Y-%m-%d")
echo ${today} >> add_new.log 2>&1
mv ./tapd.txt ../bak_tapd/tapd${twoDaysAgo}.txt
python3 tapd.py ${yesterday} >> add_new.log 2>&1
python3 add_file.py ./tapd.txt >> add_new.log 2>&1
