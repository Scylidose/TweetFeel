import React from 'react';
import './css/style.css';
import './css/audioplayer.scss';
import 'react-h5-audio-player/lib/styles.css';
import Container from 'react-bootstrap/Container';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';

import AudioPlayer from "react-h5-audio-player";

const battle = require('./mp3/Battle_OST.mp3');
const route = require('./mp3/Route_OST.mp3');
const buildings = require('./mp3/Buildings_OST.mp3');


function App() {
  /*var elements = fetch('http://localhost:5000/').then(res => res.json());
  console.log("->", elements);
*/
  return (
    <Container fluid>
      <Row>
        <Col xs={16} md={12}>
          <h3>Generated song</h3>
          <div className="left-panel">
            <h4>Battle Theme</h4>
            <AudioPlayer
              src={battle}
            />
            <hr />

            <h4>Route Theme</h4>
            <AudioPlayer
              src={route}
            />
            <hr />

            <h4>Buildings Theme</h4>
            <AudioPlayer
              src={buildings}
            />
          </div>
        </Col>
        
      </Row>
    </Container>
  );
}
export default App;
