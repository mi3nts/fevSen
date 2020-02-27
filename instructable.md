   
# Installing Dependancies 

## Creating a Repo Folder 
```
mkdir gitHubRepos
```

## Create an SSH Key 
```ssh-keygen```

## get SSH public key for github 
```
cd .ssh
cat id_rsa.pub 
```
copy it as one of github keys 



## Cloning the fever sensor repo 
```
cd ~/gitHubRepos/
git clone git@github.com:mi3nts/fevSen.git
```
## Install scipy, matplotlib 
```
sudo apt-get install python3-scipy
sudo apt-get install python3-matplotlib
```
## Install gucview and v4l-utils
```
sudo apt-get install guvcview
sudo apt-get install v4l-utils
```   
## Install VScode 
```

cd gitHubRepos/
mkdir external
cd external/
git clone https://github.com/JetsonHacksNano/installVSCode.git
cd installVSCode
 ./installVSCode.sh
```
## install pip3 
```
sudo apt-get -y install python3-pip
```

## install screen 
```
sudo apt install screen
```

## install numpi, hdf5  
```
sudo apt-get install python3-numpy 
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libhdf5
sudo pip3 install h5py
```

## Install libuvc 
```
git clone https://github.com/groupgets/libuvc
cd libuvc
mkdir build
cd build
cmake ..
make && sudo make install
```
## get the latest opencv 
```
sudo apt-get install python3-opencv
 ```
## install gucview 
```
sudo apt-get install guvcview
```  
  
## Install libvuc on the home folder 
```
cd ~
git clone https://github.com/ktossell/libuvc
cd libuvc
mkdir build
cd build
cmake ..
make && sudo make install
```
Then move the libuvc.so file to the scr folder from the build folder. Then go back to the fevsev repo and run `python3 uvc-deviceinfr.py` after connecting the thermal module. This will provide the serial number for the thermal module. 



## git configure 
```
git config --global user.name lakithaomal
git config --global user.email "lhw150030@utdallas.edu"
```




