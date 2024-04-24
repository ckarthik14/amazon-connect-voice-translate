import React, { useEffect } from 'react';
import { Grid } from 'semantic-ui-react';
import Amplify from 'aws-amplify';
import { AmazonAIPredictionsProvider } from '@aws-amplify/predictions';
import awsconfig from '../aws-exports';
import { useGlobalState } from '../store/state';

import useLambdaTrigger from './useLambdaTrigger';

Amplify.configure(awsconfig);
Amplify.addPluggable(new AmazonAIPredictionsProvider());

const Ccp = () => {
    const { lambdaResponse, triggerFromCustomerTranslation } = useLambdaTrigger();
    
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

        // Function to handle the contact connection
        const beginTranslation = () => {
            console.log("Begin translation");
            window.connect.contact(contact => {
                contact.onConnecting(async () => {
                    await triggerFromCustomerTranslation(contact);
                });
            });
        };

        beginTranslation();
    }, []);

    return (
        <main>
          <Grid columns='equal' stackable padded centered>
            <Grid.Row>
              <div id="ccp-container"></div>
            </Grid.Row>
            <Grid.Row>
              <div>Lambda Response: {JSON.stringify(lambdaResponse)}</div>
            </Grid.Row>
          </Grid>
        </main>
    );
};

export default Ccp;
