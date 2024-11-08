## Onepiece Comics Batch Rename
#!/bin/bash
# cd /Users/samuellove/Documents/Comics/One_Piece
# chmod +x rename_comics.sh
# ./rename_comics.sh

for f in *.cbz; do
    # Use sed to remove the year and other unwanted parts
    newname=$(echo "$f" | sed -E 's/ \([0-9]{4}\)//g' | sed -E 's/ \(Digital\) \(1r0n\) \(f\)//g')

    # Rename the file
    mv "$f" "$newname"
done
