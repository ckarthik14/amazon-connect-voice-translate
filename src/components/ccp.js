import React, { useEffect, useState, useRef } from 'react';
import { Grid } from 'semantic-ui-react';
import Amplify from 'aws-amplify';
import Predictions, { AmazonAIPredictionsProvider } from '@aws-amplify/predictions';
import awsconfig from '../aws-exports';
import translateText from './translate'
import detectText from './detectText'
import { addChat, setLanguageTranslate, clearChat, useGlobalState, setCurrentContactId } from '../store/state';

Amplify.configure(awsconfig);
Amplify.addPluggable(new AmazonAIPredictionsProvider());



const Ccp = () => {
    let contactAttributes;
    let event;
    const [data, setData] = useState({});

    async function triggerFromCustomerTranslation() {
        contactAttributes = contact.getAttributes();
        console.log("Contact Attributes:", contactAttributes);

        event = {
            streamARN: contactAttributes.streamARN,
            startFragmentNum: contactAttributes.startFragmentNum,
            connectContactId: contactAttributes.connectContactId,
            transcribeCall: contactAttributes.transcribeCall,
            saveCallRecording: contactAttributes.saveCallRecording,
            languageCode: contactAttributes.languageCode,
            // These default to true for backwards compatability purposes
            streamAudioFromCustomer: "true",
            streamAudioToCustomer: "false",
            customerPhoneNumber: contactAttributes.customerPhoneNumber,
        };

        console.log('Event transmitted: ' + JSON.stringify(event));

        const response = await fetch('https://jei62447y0.execute-api.us-east-1.amazonaws.com/dev/triggerLambda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        });
        const jsonData = await response.json();
        console.log('Lambda response: ' + JSON.stringify(jsonData));
        setData(jsonData);
    }

    const fetchAudioAndPlay = () => {
        const s3 = new AWS.S3();
        const kinesis = new AWS.Kinesis();
      };

    function beginTranslation() {
        console.log("Begin translation");
        
        window.connect.contact(contact => {

            contact.onConnecting(async () => {
                triggerFromCustomerTranslation(contact);
            });

            contact.onConnected(() => {
                
            })
        });
    }


    // ***** 
    // Loading CCP
    // *****
    useEffect(() => {
        const connectUrl = process.env.REACT_APP_CONNECT_INSTANCE_URL;
        let containerDiv = document.getElementById("ccp-container");
        
        window.connect.core.initCCP(containerDiv, {
            ccpUrl: connectUrl + "/connect/ccp-v2/",            // REQUIRED
            softphone: {
              // optional, defaults below apply if not provided
              allowFramedSoftphone: false, // optional, defaults to false
              disableRingtone: false, // optional, defaults to false
            },
            pageOptions: { //optional
              enableAudioDeviceSettings: true, //optional, defaults to 'false'
              enablePhoneTypeSettings: true //optional, defaults to 'true' 
            },
            ccpAckTimeout: 5000, //optional, defaults to 3000 (ms)
            ccpSynTimeout: 3000, //optional, defaults to 1000 (ms)
            ccpLoadTimeout: 10000 //optional, defaults to 5000 (ms)
           });
        
        window.connect.core.initSoftphoneManager();

        beginTranslation();
        fetchAudioAndPlay();
    }, []);


    return (
        <main>
          <Grid columns='equal' stackable padded centered>
          <Grid.Row>
            {/* CCP window will load here */}
            <div id="ccp-container"></div>
          </Grid.Row>

          <Grid.Row>
            Lambda Response: {}
          </Grid.Row>

          </Grid>
        </main>
    );
};

export default Ccp;
