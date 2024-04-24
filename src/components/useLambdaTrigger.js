import { useState } from 'react';

const useLambdaTrigger = () => {
    const [data, setData] = useState({});

    const triggerFromCustomerTranslation = async (contact) => {
        const contactAttributes = contact.getAttributes();
        console.log("Contact Attributes:", contactAttributes);

        const event = {
            streamARN: contactAttributes.streamARN,
            startFragmentNum: contactAttributes.startFragmentNum,
            connectContactId: contactAttributes.connectContactId,
            transcribeCall: contactAttributes.transcribeCall,
            saveCallRecording: contactAttributes.saveCallRecording,
            languageCode: contactAttributes.languageCode,
            streamAudioFromCustomer: "true",
            streamAudioToCustomer: "false",
            customerPhoneNumber: contactAttributes.customerPhoneNumber,
        };

        console.log('Event transmitted: ' + JSON.stringify(event));

        const response = await fetch('https://YOUR_API_ENDPOINT/triggerLambda', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(event)
        });

        const jsonData = await response.json();
        console.log('Lambda response: ' + JSON.stringify(jsonData));
        setData(jsonData);
    };

    return { data, triggerFromCustomerTranslation };
};

export default useLambdaTrigger;
