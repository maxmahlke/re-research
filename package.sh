#!/usr/bin/env bash

# Compile if necessary, passing the destination parameter
read -p "Compile first? [y/n] " -n 1 REPLY 
echo 

if [[ "$REPLY" =~ ^[Yy]$ ]]; then
    make clean
    pdflatex "\def\destination{$1} \input{main.tex}"
    bibtex main
    pdflatex "\def\destination{$1} \input{main.tex}"
fi

make clean

echo
echo "Packing"
echo "-------"

# Create archive with files outside of dependency list
tar cfv $1.tar aux/aas_macros.sty

# Parse dependencies list for files to include
sort -u main.dep | grep "file.*{0000/00/00 v0.0}$" | while read -r line; do

    # Get the dependency filename
    filename=$(echo $line | cut -d'{' -f3 | cut -d'}' -f1)

    # Publisher probably wants the bib file too
    if [[ $filename == 'aux/publisher.bst' ]]; then
        tar --append -v -f $1.tar aux/bib.bib
    fi

    # Check if file exists
    if [[ -f $filename ]]; then 
        tar --append -v -f $1.tar $filename
    else
        # Otherwise, add .tex extension and try again
        filename="${filename}.tex"

        if [[ -f $filename ]]; then 
            tar --append -v -f $1.tar $filename
        fi
    fi

done

# arXiv does not want the bib, but it needs the style file
if [[ $1 == "arxiv" ]]; then
    tar --append -v -f $1.tar aux/preprint.sty
fi
