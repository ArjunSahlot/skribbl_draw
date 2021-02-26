#!/bin/bash

download_link=https://github.com/ArjunSahlot/skribbl_draw/archive/main.zip
temporary_dir=$(mktemp -d) \
&& curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mv $temporary_dir/skribbl_draw-main $1/skribbl_draw \
&& rm -rf $temporary_dir
echo -e "[0;32mSuccessfully downloaded to $1/skribbl_draw[0m"
