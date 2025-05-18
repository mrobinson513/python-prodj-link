tempo:
	pyenv exec python midiclock.py -d "Elektron Digitakt"

obs:
	pyenv exec python update-obs-track_id.py

track:
	pyenv exec python get-live-track-id.py

entropy:
	pyenv exec python entropy.py