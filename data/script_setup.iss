; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{E4899F41-6EA4-4108-820D-C35996BB46B3}
AppName=Sea Battle
AppVersion=1.1
;AppVerName=Sea Battle 1.1
AppPublisher=Games Aft
AppPublisherURL=https://discord.gg/6BaXEbkJkw
AppSupportURL=https://discord.gg/6BaXEbkJkw
AppUpdatesURL=https://discord.gg/6BaXEbkJkw
DefaultDirName=C:\Games\Sea Battle
DefaultGroupName=Aft
; Uncomment the following line to run in non administrative install mode (install for current user only.)
;PrivilegesRequired=lowest
OutputDir=D:\AftBINKO\Documents\sea_battle\setup
OutputBaseFilename=Setup
SetupIconFile=D:\AftBINKO\Documents\sea_battle\data\SeaBattleIcon.ico
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "D:\AftBINKO\Documents\sea_battle\exe\Sea Battle\Sea Battle.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\AftBINKO\Documents\sea_battle\exe\Sea Battle\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\Sea Battle"; Filename: "{app}\Sea Battle.exe"
Name: "{group}\{cm:ProgramOnTheWeb,Sea Battle}"; Filename: "https://discord.gg/6BaXEbkJkw"
Name: "{group}\{cm:UninstallProgram,Sea Battle}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Sea Battle"; Filename: "{app}\Sea Battle.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\Sea Battle.exe"; Description: "{cm:LaunchProgram,Sea Battle}"; Flags: nowait postinstall skipifsilent
