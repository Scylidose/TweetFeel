import React from 'react';
import './css/style.css';

function App() {
  var songs = []
  fetch('http://localhost:5000/').then(res => res.json()).then(data => {
    console.log("->", data)
    for(var i=0; i < data.songs.length; i++){
      var audio = new Audio(data.songs[i]);

      songs.push(audio);
    }
  });

  
  console.log("--->", songs);

  return (
    <div className="App">
      {songs}
    </div>
  );
}
export default App;
