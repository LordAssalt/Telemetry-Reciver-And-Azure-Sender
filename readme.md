
# Telemetry Reciver and Azure Sender

Telemetry Reciver and Azure Sender è uno script Python per ricevere dati emessi da una Sensortile ed inviarli sul cloud di microsoft. Ci tengo a sottolineare che il codice è stato testato solo ed esclusivamente con Sensortile e non con Sensortile.Box

## Installation

Per prima cosa digitare, sul raspberry, i seguenti comandi per installare le librerie.
Firstly, use the following commands to install the required libraries in Raspberry.

```bash
sudo pip3 install bluepy
sudo pip3 install blue-st-sdk
sudo pip3 install azure-iot-device
sudo pip3 install azure-iot-hub
sudo pip3 install azure-iothub-service-client
sudo pip3 install azure-iothub-device-clien
```

Successivamente, prima di procedere, verificare se il Bluetooth del vostro Raspberry funziona correttamente con questi comandi.
Next, check if the Bluetooth of Raspberry works with this commands.

```bash
sudo bluetoothctl
show
```

Dopodichè bisogna eseguire il setup dell'ambiente su Microsoft Azure, esistono diversi video Youtube a riguardo.
Next, you have to setup your ambient on Microsoft Azure. YouTube offers many videos that explain how to do that.

Ora bisogna ottenere la connection string da inserire dentro lo script per comunicare con Azure. Per prima cosa recarsi sulla pagina di [node.js](nodejs.org/en/download) e scaricare e installare il programma.
Now you have to obtain the "connection-string" that allow your program to talk with Azure. To do that, if you haven't do it before, visit the following link [node.js](nodejs.org/en/download) and download and install the program.

Terminato questo passaggio, bisognerà recarsi sul terminale di Windows e digitare il seguente comando.
Now, use the following commands to install the required program (this step must be done on cmd terminal).

```bash
npm i -g dps-keygen
```

```bash
dps-keygen -di:<DeviceID> -dk:<Primary Key> -si:<ScopeID>
```

Ora. ottenuta la stringa, inseritela nello script Python sul raspberry e sarete pronti per inviare dati su Azure.
Finally, you have to insert the sting in the Python script, and now you are ready to send data.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.