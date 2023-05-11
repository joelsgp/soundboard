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
[ ] recover ones from shortcuts
[ ] recover unavailable
[ ] index non-youtube files in a subobject

to add:
- https://keep.google.com/u/0/#LIST/1rfDJbcZ-Vo1iEtzaPQH2av-v1wNCDYtJPaa4vpCiDcMvs_YAUpZivnyLe5Rnzw
