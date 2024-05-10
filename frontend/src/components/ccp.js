import React, { useEffect } from 'react';
import { Grid } from 'semantic-ui-react';
import Amplify from 'aws-amplify';
import { AmazonAIPredictionsProvider } from '@aws-amplify/predictions';
import awsconfig from '../aws-exports';
import { useGlobalState } from '../store/state';

import useLambdaTrigger from './useLambdaTrigger';
import AudioPlayer from './audioPlayer';

Amplify.configure(awsconfig);
Amplify.addPluggable(new AmazonAIPredictionsProvider());

const Ccp = () => {
    const websocketUrl = "wss://qv1241nc27.execute-api.us-east-1.amazonaws.com/dev/";

    const { lambdaResponse, triggerFromCustomerTranslation } = useLambdaTrigger();
    const { openSocket, closeSocket } = AudioPlayer(websocketUrl);


    const beginTranslation = () => {
      console.log("Begin translation");
      window.connect.contact(contact => {

          contact.onConnecting(async () => {
            triggerFromCustomerTranslation(contact);
          });

          contact.onConnected(async () => {
            openSocket();
          })

          contact.onEnded(async () => {
            setTimeout(() => {
              closeSocket();
            }, 20000);
          })
      });
  };
    
    useEffect(() => {
        const connectUrl = process.env.REACT_APP_CONNECT_INSTANCE_URL;
        const containerDiv = document.getElementById("ccp-container");
        
        window.connect.core.initCCP(containerDiv, {
            ccpUrl: connectUrl + "/connect/ccp-v2/",
            softphone: {
              allowFramedSoftphone: false,
              disableRingtone: false,
            },
            pageOptions: {
              enableAudioDeviceSettings: true,
              enablePhoneTypeSettings: true
            },
            ccpAckTimeout: 5000,
            ccpSynTimeout: 3000,
            ccpLoadTimeout: 10000
        });

        window.connect.core.initSoftphoneManager();

        beginTranslation();
    }, []);

    return (
        <main>
          <Grid columns='equal' stackable padded centered>
            <Grid.Row>
              <div id="ccp-container"></div>
            </Grid.Row>
          </Grid>
        </main>
    );
};

export default Ccp;
