bash for_internet.sh
python3 start_BCH.py
python3 start_LTC.py
while sleep 1200
do
	python3 start_BCH.py
	python3 start_LTC.py
done
