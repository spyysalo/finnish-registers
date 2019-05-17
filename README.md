# Finnish registers

Tools for working with Finnish register data

**Note**: this stuff is in development and not (yet) intended for
public consumption.  If you're not on the Finnish register project,
this won't make any sense to you.

## Data

This assumes that you have the file `annotations-superset.json` in
`data/`. If you don't have this file, ask Roosa.

## Processing

### Filtering

To filter out documents with more than one register and ones with rare registers, run

    python3 scripts/filterannotations.py data/annotations-superset.json \
        > data/annotations-superset.filtered.json

### Held-out test data split

To split a held-out test subset of the data, run

    python3 scripts/splitannotations.py \        
        data/annotations-superset.filtered.json \
        data/annotations-train.json \
        data/annotations-test.json \
        --ratio 0.8 \
        --stratify

### Statistics

Register distribution

    for f in data/annotations-{superset.filtered,train,test}.json ; do
        echo; echo $(basename "$f")
        python3 scripts/printregisters.py $f \
            | cut -f 2 | sort | uniq -c | sort -rn
    done
