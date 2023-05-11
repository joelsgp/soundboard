Beware: running `./indexer.py .` is not recommended. This is fully recursive and will dive into the `.git` folder and any other folders.

Note: `downloader.py` will fail if any directory it processes doesn't have an `index.json` file.

For these reasons you should call both of them like this:
```shell
./indexer.py bites/ clips/
```
```shell
./downloader.py bites/ clips/
```

to do:
[ ] remove ids from titles, relying entirely on index
[ ] functionality to segment one from audacity label track
