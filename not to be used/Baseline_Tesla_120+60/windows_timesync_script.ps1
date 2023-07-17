#$ErrorActionPreference = "Stop" #setzt alle Errors auf terminating Errors
#script als admin ausfuehren!

Try
{
    NET START [w32time] -ErrorAction Stop
}
Catch 
{
    Restart-Service W32Time
    Write-Warning -Message "restarded"
}
#Write-Warning -Message "rausgesprunge"
#time-server setzen und updaten 
w32tm /config /manualpeerlist:time.htw-berlin.de /syncfromflags:manual /reliable:yes
w32tm /config /update
#zeit neu holen
w32tm /resync
