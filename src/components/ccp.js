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
    var session = null;
    const audioRef = useRef(null);

    // old refs and state
    const [languageTranslate] = useGlobalState('languageTranslate');
    var localLanguageTranslate = [];
    const [Chats] = useGlobalState('Chats');
    const [lang, setLang] = useState("");
    const [currentContactId] = useGlobalState('currentContactId');
    const [languageOptions] = useGlobalState('languageOptions');
    const [agentVoiceSessionState, setAgentVoiceSessionState] = useState([]);
    const [setRefreshChild] = useState([]);

    function subscribeConnectEvents() {
        console.log("Subscribing to connect events");
        
        window.connect.contact(contact => {
            contact.onConnecting(() => {
                let softphoneMediaInfo = contact.getAgentConnection().getSoftphoneMediaInfo();
                console.log("softphoneMediaInfo: ", JSON.stringify(softphoneMediaInfo));
              
                const rtcConfig = softphoneMediaInfo.webcallConfig || JSON.parse(softphoneMediaInfo.callConfigJson || '{}');
                console.log("rtcConfig: ", rtcConfig);
            
                const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
                const host = process.env.REACT_APP_CONNECT_INSTANCE_URL + "/connect/ccp-v2";
                const wssUrl = host.replace(/^https:\/\//i, protocol);

                const rtcSessionUrl = wssUrl + rtcConfig.signalingEndpoint;

                session = new window.connect.RTCSession(
                    rtcSessionUrl,
                    rtcConfig.iceServers,
                    rtcConfig.callContextToken,
                    console
                );
                console.log("session: ", session);

                session.onSessionConnected = () => {}
                session.onSessionCompleted = () => {}
                session.onSessionDestroyed = (s, report) => {}
            
                var audioElement = audioRef.current;
                console.log("remote audio looks like: ", audioElement);
                session.remoteAudioElement = audioElement;
                session.forceAudioCodec = 'OPUS';
            });

            contact.onConnected(() => {
                console.log("before session connect");
                session.connect();
                console.log("after session connect");
            });
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

        window.connect.core.initSoftphoneManager({allowFramedSoftphone: true});

        audioRef.current.muted = false; // Apply the muted state to the audio element
        audioRef.current.play(); // Play the audio

        // subscribeConnectEvents();
    }, []);


    return (
        <main>
          <Grid columns='equal' stackable padded centered>
          <Grid.Row>
            {/* CCP window will load here */}
            <div id="ccp-container"></div>
            </Grid.Row>
          </Grid>
          <audio id="remote-audio" ref={audioRef} autoplay muted></audio>
        </main>
    );
};

export default Ccp;
