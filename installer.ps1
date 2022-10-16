echo "Configuring LSLlab..."

# Installing LSL enviroment in user´s Desktop folder
$ProgressPreference = "SilentlyContinue"
$DesktopPath = [Environment]::GetFolderPath("Desktop")
cd $DesktopPath
mkdir labLSL_v1 | Out-Null; cd labLSL_v1
curl -L -o "labLSL_v1.zip" "https://github.com/JesusdelCas99/labLSL/releases/download/labLSL/labLSL_v1.0_w10_x86_64.zip" -s
Expand-Archive "labLSL_v1.zip" -DestinationPath "./" | Out-Null
del labLSL_v1.zip; cd ..
echo "LSL enviroment installed in the following PATH: ${DesktopPath}\labLSL_v1" ; echo ""

# Git
echo "Installing Git..."
choco install git -y -f | Out-Null
echo "Git installed!" ; echo ""

# Wireshark
echo "Installing Wireshark..."
choco install wireshark -y -f | Out-Null
echo "Wireshark installed!" ; echo ""

# ffmpeg Tool
echo "Installing ffmpeg..."
choco install ffmpeg -y -f | Out-Null
echo "ffmpeg tool installed!" ; echo ""

# Visual Studio Code
echo "Installing Visual Studio Code..."
# choco install vscode -y -f| Out-Null
echo "Visual Studio Code installed!" ; echo ""

# Anaconda enviroment
echo "Installing Anaconda3..."
# choco install anaconda3 -y -f | Out-Null
echo "Installing LabStreaminglayer dependencies in Python..."
conda activate base # Switch to default Ananconda enviroment
# Installing required LSL dependencies
echo "Installing PyQt5..." ; pip install PyQt5 | Out-Null
echo "Installing pylsl..." ; pip install pylsl | Out-Null
echo "Installing serial..." ; pip install serial | Out-Null
echo "Installing keyboard..." ; pip install keyboard | Out-Null
echo "Installing OpenCV..." ; pip install opencv-python | Out-Null
echo "Anaconda3 installed!" ; echo ""

# PsychoPy
echo "Installing PsychoPy..."
mkdir temp | Out-Null; cd temp
curl -L -o "./StandalonePsychoPy-2022.2.4-win64.exe" "https://github.com/psychopy/psychopy/releases/download/2022.2.4/StandalonePsychoPy-2022.2.4-win64.exe" -s
Start-Process -Wait -FilePath ".\StandalonePsychoPy-2022.2.4-win64.exe" -ArgumentList "/S" -PassThru | Out-Null
cd .. ; del temp -R
echo "PsychoPy installed!" ; echo ""

# Curl Tool 
echo "Installing curl..."
choco install curl -y -f | Out-Null
echo "Curl installed!" ; echo ""

# VLC Tool
echo "Installing VLC Tool..."
choco install vlc -y -f | Out-Null
echo "VLC Tool installed!" ; echo ""

# Microsoft Redistributables
echo "Installing Microsoft Redistributables for compilation..."
mkdir temp | Out-Null; cd temp
curl -o "./mscv_redistributables.zip" "https://uk1-dl.techpowerup.com/files/k6wjn-52lPzo_NWfwDsBsg/1665987028/Visual-C-Runtimes-All-in-One-Jul-2022.zip" -s
Expand-Archive ".\mscv_redistributables.zip" -DestinationPath "./" | Out-Null
Start-Process -Wait -FilePath ".\install_all.bat" -ArgumentList "/S" -PassThru | Out-Null
cd .. ; del temp -R
echo "Microsoft Redistributables installed!" ; echo ""

# BrainVision LSL Viewer
echo "Installing BrainVision LSL Viewer..."
mkdir temp | Out-Null; cd temp
curl "https://www.brainproducts.com/download/brainvision-lsl-viewer/?nonce=c374a1a2e0" --output "./brainvision-lsl-viewer.zip" -s
Expand-Archive "brainvision-lsl-viewer.zip" -DestinationPath "./" | Out-Null
Start-Process -Wait -FilePath ".\BrainVision_LSL_Viewer_0.9.5.exe" -ArgumentList "/S" -PassThru | Out-Null
cd .. ; del temp -R
echo "BrainVision LSL Viewer installed!" ; echo ""

echo "Configuration done!"