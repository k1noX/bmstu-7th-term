python3 pre_mapper.py < ./data/input.txt | sort | python3 reducer.py | python3 mapper.py | sort | python3 reducer.py | python3 mapper.py | sort | python3 reducer.py  | python3 post_mapper.py | sort
