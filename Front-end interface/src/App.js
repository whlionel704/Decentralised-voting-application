import './App.css';
import {PeraWalletConnect} from '@perawallet/connect';
import algosdk, { waitForConfirmation } from 'algosdk';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import { useEffect, useState } from 'react';

// Create the PeraWalletConnect instance outside the component
const peraWallet = new PeraWalletConnect();

// The app ID on testnet
const appIndex = 156791600;

// connect to the algorand node
const algod = new algosdk.Algodv2('','https://testnet-api.algonode.cloud', 443);

function App() {
  const [accountAddress, setAccountAddress] = useState(null);
  //const [currentCount, setCurrentCount] = useState(null);
  //const [localCount, setLocalCount] = useState(null);
  const isConnectedToPeraWallet = !!accountAddress;

  useEffect(() => {
    //checkCounterState();
    // checkLocalCounterState();
    // reconnect to session when the component is mounted
    peraWallet.reconnectSession().then((accounts) => {
      // Setup disconnect event listener
      peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);

      if (accounts.length) {
        setAccountAddress(accounts[0]);
      }
    })

  },[]);
  
  return (
    <Container className='App-header'>
      <meta name="name" content="whlionel704 - Frontend component" />
      <h1> whlionel704 Voting app </h1>
      <Row>
        <Col><Button className="btn-wallet"
      onClick={
        isConnectedToPeraWallet ? handleDisconnectWalletClick : handleConnectWalletClick
      }>
      {isConnectedToPeraWallet ? "Disconnect" : "Connect to Pera Wallet"}
    </Button></Col>
    <Col><Button className="btn-wallet" 
      onClick={
        () => optInToApp()
      }>
      Opt-in
    </Button></Col>
      </Row>
        
      <Container>
        <Row>
    <Col>
    <h3>Red Score</h3><input name="redScoreBox" type="int" id="redScoreBoxId" maxlength="1"></input>
    {/* <span className='local-counter-text'>{localCount}</span> */}
    </Col>
        </Row>

        <Row>
    <Col>
    <h3>Yellow Score</h3><input name="yellowScoreBox" type="int" id="yellowScoreBoxId" maxlength="1"></input>
    {/* <span className='local-counter-text'>{localCount}</span> */}
    </Col>
        </Row>

        <Row>
    <Col>
    <h3>Blue Score</h3><input name="blueScoreBox" type="int" id="blueScoreBoxId" maxlength="1"></input>
    {/* <span className='local-counter-text'>{localCount}</span> */}
    </Col>
          
        </Row>
        
        <Row>
          <Col><Button className="button-vote" 
          onClick={
          // add the local deduct method
            () => callCounterApplication('vote')
          }>
          Vote
          </Button></Col>
        </Row>

        <Row>
          <Col><Button className="button-update_scores" 
          onClick={
          // add the local deduct method
            () => callCounterApplication('update_scores')
          }>
          Re-vote
          </Button></Col>
        </Row>

        <Row>
          <Col><Button className="button-close-out" 
          onClick={
          // add the local deduct method
            () => closeOutApp()
          }>
          Close-out
          </Button></Col>
        </Row>

        <Row>
          <Col><Button className="button-clear-state" 
          onClick={
          // add the local deduct method
            () => clearStateApp()
          }>
          Clear state
          </Button></Col>
        </Row>

      </Container>
    </Container>
  );

  function handleConnectWalletClick() {
    peraWallet.connect().then((newAccounts) => {
      // setup the disconnect event listener
      peraWallet.connector?.on('disconnect', handleDisconnectWalletClick);

      setAccountAddress(newAccounts[0]);
    });
  }

    function handleDisconnectWalletClick() {
      peraWallet.disconnect();
      setAccountAddress(null);
    }

    async function optInToApp() {
      const suggestedParams = await algod.getTransactionParams().do();
      const optInTxn = algosdk.makeApplicationOptInTxn(
        accountAddress,
        suggestedParams,
        appIndex
      );

      const optInTxGroup = [{txn: optInTxn, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([optInTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
    }
  
    async function closeOutApp() {
      const suggestedParams = await algod.getTransactionParams().do();
      const closeOutTxn = algosdk.makeApplicationCloseOutTxn(
        accountAddress,
        suggestedParams,
        appIndex
      );

      const closeOutTxGroup = [{txn: closeOutTxn, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([closeOutTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
    }

    async function clearStateApp() {
      const suggestedParams = await algod.getTransactionParams().do();
      const clearStateTxn = algosdk.makeApplicationClearStateTxn(
        accountAddress,
        suggestedParams,
        appIndex
      );

      const clearStateTxGroup = [{txn: clearStateTxn, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([clearStateTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
    }

    /*async function checkCounterState() {
      try {
        const counter = await algod.getApplicationByID(appIndex).do();
        if (!!counter.params['global-state'][0].value.uint) {
          setCurrentCount(counter.params['global-state'][0].value.uint);
        } else {
          setCurrentCount(0);
        }
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }*/

    /*async function checkLocalCounterState() {
      try {
        const accountInfo = await algod.accountApplicationInformation(accountAddress,appIndex).do();
        if (!!accountInfo['app-local-state']['key-value'][0].value.uint) {
          setLocalCount(accountInfo['app-local-state']['key-value'][0].value.uint);
        } else {
          setLocalCount(0);
        }
        console.log(accountInfo['app-local-state']['key-value'][0].value.uint);
      } catch (e) {
        console.error('There was an error connecting to the algorand node: ', e)
      }
    }*/

    async function callCounterApplication(action) {
      try {
        // get suggested params
        const suggestedParams = await algod.getTransactionParams().do();
        
        let appargs = [new Uint8Array(Buffer.from(action))]
        appargs.push(algosdk.encodeUint64(parseInt(document.getElementById("redScoreBoxId").value)))
        appargs.push(algosdk.encodeUint64(parseInt(document.getElementById("yellowScoreBoxId").value)))
        appargs.push(algosdk.encodeUint64(parseInt(document.getElementById("blueScoreBoxId").value)))

        const actionTx = algosdk.makeApplicationNoOpTxn(
          accountAddress,
          suggestedParams,
          appIndex,
          appargs
          );

        const actionTxGroup = [{txn: actionTx, signers: [accountAddress]}];

        const signedTx = await peraWallet.signTransaction([actionTxGroup]);
        console.log(signedTx);
        const { txId } = await algod.sendRawTransaction(signedTx).do();
        const result = await waitForConfirmation(algod, txId, 2);
        //checkCounterState();
        //checkLocalCounterState();
      
      } catch (e) {
        console.error(`There was an error calling the counter app: ${e}`);
      }
    }
}

export default App;
