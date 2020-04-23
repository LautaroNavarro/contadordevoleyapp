import React from 'react';
import { BrowserRouter as Router, Route } from 'react-router-dom';
import Home from './containers/Home/Home';
import CreateMatch from './containers/CreateMatch/CreateMatch';
import MatchView from './containers/MatchView/MatchView';


function App() {
  return (
    <Router>
        <div>
            <Route exact path="/" component={Home} />
            <Route exact path="/matches/new" component={CreateMatch} />
            <Route exact path="/matches/:id(\d+)" component={MatchView} />
        </div>
    </Router>
  );
}

export default App;
