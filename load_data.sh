cp kaggle.json ~/.kaggle/ &&
chmod 600 ~/.kaggle/kaggle.json
kaggle datasets download -d watchman/rtsd-dataset &&
unzip -q rtsd-dataset.zip -d rtsd-dataset &&
rm rtsd-dataset.zip