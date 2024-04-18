import React, { useEffect, useState } from 'react';
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
    const [languageTranslate] = useGlobalState('languageTranslate');
    var localLanguageTranslate = [];
    const [Chats] = useGlobalState('Chats');
    const [lang, setLang] = useState("");
    const [currentContactId] = useGlobalState('currentContactId');
    const [languageOptions] = useGlobalState('languageOptions');
    const [agentVoiceSessionState, setAgentVoiceSessionState] = useState([]);
    const [setRefreshChild] = useState([]);

    const audioRef = useRef(null);

    function subscribeConnectEvents() {
        console.log("Subscribing to connect events");
        
        window.connect.contact(contact => {
            console.log(contact.getAgentConnection().getSoftphoneMediaInfo());
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
              disableEchoCancellation: false, // optional, defaults to false
              allowFramedVideoCall: true, // optional, default to false
              VDIPlatform: null, // optional, provide with 'CITRIX' if using Citrix VDI, or use enum VDIPlatformType
              allowEarlyGum: true, //optional, default to true
            },
            pageOptions: { //optional
              enableAudioDeviceSettings: true, //optional, defaults to 'false'
              enablePhoneTypeSettings: true //optional, defaults to 'true' 
            },
            ccpAckTimeout: 5000, //optional, defaults to 3000 (ms)
            ccpSynTimeout: 3000, //optional, defaults to 1000 (ms)
            ccpLoadTimeout: 10000 //optional, defaults to 5000 (ms)
           });

        window.connect.core.initSoftphoneManager({allowFramedSoftphone: true});

        subscribeConnectEvents();
    }, []);

    const fetchAndPlayAudio = async () => {
      try {
          const response = await fetch('https://demo-audiotest24.s3.amazonaws.com/sample-0.mp3');
          const blob = await response.blob();
          const audioUrl = URL.createObjectURL(blob);
          audioRef.current.src = audioUrl;
          audioRef.current.play();
      }
      catch (error) {
        console.error('Error fetching and playing audio: ', error);
      }
    }

    return (
        <main>
          <Grid columns='equal' stackable padded centered>
          <Grid.Row>
            {/* CCP window will load here */}
            <div id="ccp-container"></div>
            </Grid.Row>
          </Grid>
          <button onClick={fetchAndPlayAudio}>Play Audio</button>
          <audio id="remote-audio" autoplay></audio>
        </main>
    );
};

export default Ccp;
