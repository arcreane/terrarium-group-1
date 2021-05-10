document.addEventListener('DOMContentLoaded', (event) => {
    controlSlider = document.getElementById("control");

    realValue = document.getElementById('realValue');

    // Create a client instance
    client = new Paho.MQTT.Client("broker.mqttdashboard.com", 8000, "web_" + parseInt(Math.random() * 100, 10));

    // set callback handlers
    client.onConnectionLost = onConnectionLost;
    client.onMessageArrived = onMessageArrived;

    // connect the client
    client.connect({ onSuccess: onConnect });


    controlSlider.addEventListener('change', (event) => {
        message = new Paho.MQTT.Message(controlSlider.value);
        message.destinationName = "humidity";
        client.send(message);
    })

    controlSlider.addEventListener('input', (event) => {
        message = new Paho.MQTT.Message(controlSlider.value);
        message.destinationName = "humidity";
        client.send(message);
    })
    // called when the client connects
    function onConnect() {
        // Once a connection has been made, make a subscription and send a message.
        console.log("onConnect");
        client.subscribe("humidity");
        // message = new Paho.MQTT.Message("788");
        // message.destinationName = "humidity";
        // client.send(message);
    }

    // called when the client loses its connection
    function onConnectionLost(responseObject) {
        if (responseObject.errorCode !== 0) {
            console.log("onConnectionLost:" + responseObject.errorMessage);
        }
    }

    // called when a message arrives
    function onMessageArrived(message) {
        console.log("onMessageArrived:" + message.payloadString);
        realValue.innerText = message.payloadString;
        controlSlider.value = message.payloadString;

    }


})