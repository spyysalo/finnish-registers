# Finnish registers

Tools for working with Finnish register data

**Note**: this stuff is in development and not (yet) intended for
public consumption.  If you're not on the Finnish register project,
this won't make any sense to you.

## Data

This assumes that you have the file `annotations-superset.json` in
`data/`. If you don't have this file, ask Roosa.

Also, parts assume parsed versions of this data.

## Processing

### Filtering

To filter out documents with more than one register and ones with rare registers, run

    python3 scripts/filterannotations.py data/annotations-superset.json \
        > data/annotations-superset.filtered.json

### Held-out test data split

To split a held-out test subset of the data, run

    python3 scripts/splitannotations.py \
        data/annotations-superset.filtered.json \
        data/annotations-train-and-dev.json \
        data/annotations-test.json \
        --ratio 0.8 \
        --stratify

### Train-dev split

    python3 scripts/splitannotations.py \
        data/annotations-train-and-dev.json \
        data/annotations-train.json \
        data/annotations-dev.json \
        --ratio 0.875 \
        --stratify

### Statistics

Register distribution

    for f in data/annotations-{superset.filtered,train,dev,test}.json ; do
        echo; echo $(basename "$f")
        python3 scripts/printregisters.py $f \
            | cut -f 2 | sort | uniq -c | sort -rn
    done

### Store IDs for split

    mkdir split
    for f in data/annotations-{train,dev,test}.json; do
        python3 scripts/printregisters.py $f \
            | cut -f 1 > split/$(basename $f .json)-ids.txt
    done

### Split parsed

    mkdir data/split-parsed
    for s in train dev test; do
        o=data/split-parsed/$s
	mkdir -p "$o"
	cat split/annotations-${s}-ids.txt | while read i; do
	    cp data/parsed/${i}.txt.conllu $o
	done
    done

### Store ID-label mapping

    for f in data/parsed/*.conllu; do
        echo $(basename $f .txt.conllu)$'\t'$(egrep '#.*register:' $f | perl -pe 's/.*?register://')
    done > data/docid-label-map.tsv
