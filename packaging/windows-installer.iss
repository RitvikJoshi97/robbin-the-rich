; Inno Setup script for the Windows installer. Built by .github/workflows/build.yml.
#ifndef AppVersion
  #define AppVersion "1.0.0"
#endif

[Setup]
AppId={{6F3C2B1E-5A7D-4C8E-9B0F-2D1E3A4B5C6D}
AppName=Robbin' The Rich
AppVersion={#AppVersion}
AppPublisher=Ritvik Joshi
AppPublisherURL=https://github.com/RitvikJoshi97/robbin-the-rich
DefaultDirName={autopf}\Robbin The Rich
DefaultGroupName=Robbin' The Rich
DisableProgramGroupPage=yes
OutputDir=..\dist
OutputBaseFilename=Robbin-The-Rich-Windows-x64-setup
SetupIconFile=..\out\icon.ico
UninstallDisplayIcon={app}\RobbinTheRich.exe
Compression=lzma2
SolidCompression=yes
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequiredOverridesAllowed=dialog

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "..\out\RobbinTheRich\*"; DestDir: "{app}"; Flags: recursesubdirs ignoreversion

[Icons]
Name: "{group}\Robbin' The Rich"; Filename: "{app}\RobbinTheRich.exe"
Name: "{autodesktop}\Robbin' The Rich"; Filename: "{app}\RobbinTheRich.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\RobbinTheRich.exe"; Description: "{cm:LaunchProgram,Robbin' The Rich}"; Flags: nowait postinstall skipifsilent
