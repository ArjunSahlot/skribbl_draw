#!/bin/bash

download_link=https://github.com/ArjunSahlot/skribbl_draw/archive/main.zip
temporary_dir=$(mktemp -d)
echo "Checking if curl is installed"
if [ $(sudo dpkg-query -l | grep curl | wc -l) -eq 0 ];
then
  echo -e "\033[0;31mcurl is not installed\033[0m"
  echo "Installing curl..."
  sudo apt install -y curl;
  echo -e "\033[0;32mcurl was successfully installed\033[0m"
else
  echo -e "\033[0;32mcurl is already installed\033[0m"
fi
curl -LO $download_link \
&& unzip -d $temporary_dir main.zip \
&& rm -rf main.zip \
&& mkdir -p $1 \
&& cp -r $temporary_dir/skribbl_draw-main $1/skribbl_draw \
&& rm -rf $temporary_dir \
&& echo -e "\033[0;32mSuccessfully downloaded to $1/skribbl_draw\033[0m" \
&& echo "Checking if pip is installed"
if [ $(sudo dpkg-query -l | grep python3-pip | wc -l) -eq 0 ];
then
  echo -e "\033[0;31mpip is not installed\033[0m" \
  && echo "Installing pip..." \
  && sudo apt install -y python3-pip \
  && echo -e "\033[0;32mpip was successfully installed\033[0m"
else
  echo -e "\033[0;32mpip is already installed\033[0m"
fi
echo "Installing requirements" \
&& cd $1/skribbl_draw \
&& pip3 install -r requirements.txt \
&& echo -e "\033[0;32mDone!\033[0m"
