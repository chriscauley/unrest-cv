## v0.0.5 - No breaking changes

* Added `paste_expandable(back, front, ...)` function. If front is out of bounds for front, canvas will expand to match.

* Smarter options for `urcv.text.write`. Now now `urcv.text.write(img, 'whatever', 'bottom right')` is shorthand for `urcv.text.write(img, 'whatever', (img.shape[1], img.shape[0]), 'bottom right')`